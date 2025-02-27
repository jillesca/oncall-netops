import os
from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from agents.prompts import (
    ORCHESTRATOR_INSTRUCTIONS,
    NODE_SYNTHESIZER_INSTRUCTIONS,
    NODE_ROOT_CAUSE_ANALYZER_INSTRUCTIONS,
)
from graph_state_shemas import AgentState, Tasks, Task, RcaAgentSchema
from utils.utils import set_env, save_report, save_workflow
from agents.agent_isis import agent_isis
from agents.agent_network_interface import agent_network_interface
from agents.agent_log_analyzer import agent_log_analyzer
from agents.agent_routing import agent_routing
from agents.agent_device_health import agent_device_health
from agents.agent_coordinator import (
    agent_coordinator,
    AGENT_COORDINATOR_PROMPT,
)
from agents.agent_interface_actions import agent_interface_actions


LLM_MODEL = "gpt-4o-mini"
llm = ChatOpenAI(model=LLM_MODEL, temperature=0)


def get_list_of_specialists() -> str:
    """Extracts and returns a comma-separated list of agent names from the Task class."""
    return ", ".join(Task.__annotations__["agent"].__args__)


def node_coordinator(state: AgentState):
    coordinator = agent_coordinator()

    resolution_log = f"Previous Investigation: {state.get('resolution_log', 'NO_PREVIOUS_INVESTIGATION_EXIST')}"
    tasks_performed = f"Previous Tasks Performed: {state.get('completed_tasks', 'NO_PREVIOUS_TASKS_PERFORMED')}"
    alert_received = state.get("incident_description", "")
    user_request = state.get("user_request", "")
    request = {
        "messages": [
            SystemMessage(content=AGENT_COORDINATOR_PROMPT),
            HumanMessage(
                content=f"Alert_received: {alert_received}\n\nUser_request: {user_request}\n\n{resolution_log}\n\n{tasks_performed}"
            ),
        ]
    }
    task_result = coordinator.invoke(request, debug=True)
    structured_response = task_result.get("structured_response", {})

    incident_description = structured_response.get("incident_description", "")
    user_request = structured_response.get("user_request", "")
    device = structured_response.get("device", "")
    more_info = structured_response.get("more_info", False)

    return {
        "incident_description": incident_description,
        "user_request": user_request,
        "device": device,
        "more_info": more_info,
        "resolution_log": "",
    }


# Nodes
def node_orchestrator(state: AgentState):
    """Orchestrator that generates a plan for resolving network issues"""
    orchestrator_structured_llm = llm.with_structured_output(Tasks)
    list_of_specialists = get_list_of_specialists()
    system_message = ORCHESTRATOR_INSTRUCTIONS.format(
        specialists=list_of_specialists,
    )
    device = state.get("device", "None")
    user_request = state.get("user_request", "None")
    rca_analysis = state.get("rca_analysis", "None")
    alert_received = state.get("incident_description", "None")
    task_plan = orchestrator_structured_llm.invoke(
        [
            SystemMessage(content=system_message),
            HumanMessage(
                content=f"Monitoring Alert Received: {alert_received}\n\nUser Request if any: {user_request}\n\nDevice Involved: {device}\n\nAdditional information requested by the RCA agent if any: {rca_analysis}"
            ),
        ],
    )
    return {"tasks": task_plan.tasks}


def node_network_agents(state: Task):
    """Worker resolves a task related to the network issue"""
    agent = None
    match state["task"].agent:
        case "agent_isis":
            agent = agent_isis()
        case "agent_network_interface":
            agent = agent_network_interface()
        case "agent_log_analyzer":
            agent = agent_log_analyzer()
        case "agent_routing":
            agent = agent_routing()
        case "agent_device_health":
            agent = agent_device_health()
        case "agent_interface_actions":
            agent = agent_interface_actions()
    request = {
        "messages": [
            (
                "user",
                f"Incident description: {state['task'].incident}\n\nTask required: {state['task'].description}\n\nDevice involved: {state['task'].device}",
            ),
        ]
    }
    task_result = agent.invoke(request, config={"max_retries": 5}, debug=True)
    return {"completed_tasks": [task_result["messages"][-1].content]}


def node_root_cause_analyzer(state: AgentState):
    """Root cause analysis"""
    device = state["device"]
    completed_tasks = state["completed_tasks"]
    user_request = state.get("user_request", "")
    incident = state.get("incident_description", "")
    analysis_performed = "\n\n---\n\n".join(completed_tasks)
    rca_structured_llm = llm.with_structured_output(RcaAgentSchema)
    rca = rca_structured_llm.invoke(
        [
            SystemMessage(content=NODE_ROOT_CAUSE_ANALYZER_INSTRUCTIONS),
            HumanMessage(
                content=f"Indicent: {incident}\n\nDevice(s) Involved: {device}\n\nUser Request: {user_request}\n\nFinding from the agents: {analysis_performed}"
            ),
        ]
    )
    return {
        "more_info": rca["more_info"],
        "rca_analysis": rca["rca_analysis"],
    }


def node_report_generator(state: AgentState):
    """Synthesize full report from tasks"""
    completed_tasks = state["completed_tasks"]
    incident = state["incident_description"]
    device = state["device"]
    user_request = state.get("user_request", "")
    rca_analysis = state.get("rca_analysis", "")
    analysis_performed = "\n\n---\n\n".join(completed_tasks)
    resolution_log = llm.invoke(
        [
            SystemMessage(content=NODE_SYNTHESIZER_INSTRUCTIONS),
            HumanMessage(
                content=f"Indicent: {incident}\n\nDevice(s) Involved: {device}\n\nUser Request: {user_request}\n\nFinding from the agents: {analysis_performed}\n\nRoot Cause Analysis: {rca_analysis}"
            ),
        ],
        config={"max_retries": 5},
    )
    completed_tasks.clear()
    return {
        "resolution_log": resolution_log.content,
        "tasks": Tasks(tasks=[]),
        "completed_tasks": completed_tasks,
        "device": "None",
        "more_info": False,
        "incident_description": "",
        "user_request": "",
        "rca_analysis": "",
    }


def edge_assign_workers(state: AgentState):
    """Assign a worker to each section in the plan"""
    tasks: Tasks = state["tasks"]
    return [Send("node_network_agents", {"task": task}) for task in tasks]


def continue_or_ask_for_more_info(state: AgentState):
    if state["more_info"]:
        return "more_info"
    else:
        return "continue"


orchestrator_worker_builder = StateGraph(AgentState)

orchestrator_worker_builder.add_node("node_coordinator", node_coordinator)
orchestrator_worker_builder.add_node("node_orchestrator", node_orchestrator)
orchestrator_worker_builder.add_node(
    "node_root_cause_analyzer", node_root_cause_analyzer
)
orchestrator_worker_builder.add_node(
    "node_network_agents", node_network_agents
)
orchestrator_worker_builder.add_node(
    "node_report_generator", node_report_generator
)

orchestrator_worker_builder.add_edge(START, "node_coordinator")
orchestrator_worker_builder.add_edge("node_coordinator", "node_orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "node_orchestrator", edge_assign_workers, ["node_network_agents"]
)

orchestrator_worker_builder.add_edge(
    "node_network_agents", "node_root_cause_analyzer"
)
orchestrator_worker_builder.add_conditional_edges(
    "node_root_cause_analyzer",
    continue_or_ask_for_more_info,
    {
        "continue": "node_report_generator",
        "more_info": "node_orchestrator",
    },
)
orchestrator_worker_builder.add_edge("node_report_generator", END)


# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()

orchestrator_worker = orchestrator_worker_builder.compile(
    checkpointer=within_thread_memory,
)

# Show the workflow
save_workflow(graph=orchestrator_worker)

if __name__ == "__main__":
    orchestrator_worker = orchestrator_worker_builder.compile()

    state = orchestrator_worker.invoke(
        {
            "incident_description": "Can you check the interfaces on device cat8000v-0 are working correctly, I'm afraid ISIS is not working"
        }
    )

    save_report(state=state)
