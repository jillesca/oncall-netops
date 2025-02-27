import operator
from typing import Union
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.managed import IsLastStep, RemainingSteps
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

StructuredResponse = Union[dict, BaseModel]


# Schema for structured output to use in planning
class Task(BaseModel):
    agent: Literal[
        "agent_isis",
        "agent_routing",
        "agent_network_interface",
        "agent_log_analyzer",
        "agent_device_health",
        "agent_interface_actions",
    ] = Field(
        description="ID of the Agent to be used for this task.",
        default="None",
    )
    description: str = Field(
        description="Context, goal, expectations, and focus areas for this task.",
    )
    device: str = Field(
        description="Device or devices name to be used for this task.",
    )
    incident: str = Field(
        description="Original incident that triggered this task.",
    )


class Tasks(BaseModel):
    tasks: List[Task] = Field(
        description="Tasks of the investigation.",
    )


# Updated Graph state for network issue resolution
class AgentState(TypedDict):
    incident_description: str
    tasks: Tasks
    completed_tasks: Annotated[list, operator.add]
    resolution_log: str
    user_request: str = Field(
        description="User request that triggered this task.",
        default=None,
    )
    device: str = Field(
        description="Device or devices name to be used for this task.",
        default="",
    )
    more_info: bool = Field(
        description="If you need more information from the agent(s), return True, otherwise return False.",
        default=False,
    )
    rca_analysis: str = Field(
        description="Root cause analysis of the incident, or additional information required to the agent(s) to be used for the RCA.",
        default="",
    )


class AgentCoordinatorSchema(TypedDict):
    incident_description: str = Field(
        description="Incident description or human request to be used for this task.",
        default="",
    )
    device: str = Field(
        description="Field exclusive for Device or devices name to be used for this task. Don't include any other data in this field.",
        default="None",
    )


class RcaAgentSchema(TypedDict):
    more_info: bool = Field(
        description="If you need more information from the agent(s), return True, otherwise return False.",
        default=False,
    )
    rca_analysis: str = Field(
        description="Root cause analysis of the incident, or additional information required to the agent(s) to be used for the RCA. If more information is required, Be clear what additional information the agent must provide.",
        default="",
    )


class AgentCoordinatorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    remaining_steps: RemainingSteps
    structured_response: StructuredResponse
    is_last_step: IsLastStep = Field(
        description="If you have finsih your job calling tools, return True, otherwise return False.",
        default=False,
    )
