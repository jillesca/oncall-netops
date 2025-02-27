from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.pyats.pyats_interface_status_tools import (
    get_interface_detailed_status,
    get_interface_information,
    get_interface_admin_status,
    verify_interface_state_up,
    get_interface_running_config,
    get_interfaces_status,
    get_interfaces_status_and_description,
    get_interface_events,
)

AGENT_NETWORK_INTERFACE_PROMPT = """You are a network tech lead that is specialized in the interfaces of network devices. You have access to a set of tools to connect to network devices and retrieve information about the network. Execute the tools to get the information you need to answer the requests. You decide tool or tools to use. 

You must only use the data (ip, interface name, description, status, etc.) provided by the tools as input for your response or input for the next tool to use. You must not make up any information or make assumptions.

Always use the get_interfaces_status tool to get the name of the interfaces on a device. This is the only valid way to get the name of the interfaces on a device. You don't have to use all names for your analysis, but you must use the get_interfaces_status tool to get the name of the interfaces on a device.


Always review the configuration of the device to understand if the interface was intended to be used and is relevant for the incident description.

Once you have all the information you need, you must answer the request in a concise and professional manner. This information will be used by a network engineer to take actions on the network.
"""

LLM_MODEL = "gpt-4o-mini"
tools = [
    get_interface_detailed_status,
    get_interface_information,
    get_interface_admin_status,
    verify_interface_state_up,
    get_interface_running_config,
    get_interfaces_status,
    get_interfaces_status_and_description,
    get_interface_events,
]
model = ChatOpenAI(model=LLM_MODEL, temperature=0)


def agent_network_interface():
    return create_react_agent(
        model, tools=tools, prompt=AGENT_NETWORK_INTERFACE_PROMPT
    )


if __name__ == "__main__":
    inputs = {
        "messages": [
            (
                "user",
                "Can you check the interfaces on device cat8000v-0 are working correctly?",
            )
        ]
    }

    graph = agent_network_interface()

    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
