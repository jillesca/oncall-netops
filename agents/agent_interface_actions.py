from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.pyats.pyats_interface_oper_tools import (
    shut_interface,
    unshut_interface,
)
from tools.pyats.pyats_interface_status_tools import (
    verify_interface_state_up,
)
from tools.pyats.pyats_interface_status_tools import (
    get_interfaces_status,
)


AGENT_INTERFACE_ACTIONS = """You are a network tech lead that is specialized in operating interfaces of network devices. You have access to a set of tools to connect to network devices and perform actions on the interfaces. You decide tool or tools to use. 

Validate the interface name given to you is real, use the gget_interfaces_status tool to check if the interface exists. This is a mandatory step.

You will be given a list of interfaces and the action to be performed on them. You must use the tools to perform the action on the interfaces.

Once you have the correct device name, perform the action asked on the interfaces and always verify your work with the verify_interface_state_up tool.
"""

LLM_MODEL = "gpt-4o-mini"
tools = [
    shut_interface,
    unshut_interface,
    verify_interface_state_up,
    get_interfaces_status,
]
model = ChatOpenAI(model=LLM_MODEL, temperature=0)


def agent_interface_actions():
    return create_react_agent(
        model, tools=tools, prompt=AGENT_INTERFACE_ACTIONS
    )


if __name__ == "__main__":
    inputs = {
        "messages": [
            # (
            #     "user",
            #     "Can you shut the interface GigabitEthernet4 on device cat8000v-0?",
            # ),
            (
                "user",
                "Can you unshut the interface GigabitEthernet4 on device cat8000v-0?",
            ),
        ]
    }

    graph = agent_interface_actions()

    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
