from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.pyats.pyats_routing_tools import (
    get_vrf_present,
    get_interfaces_under_vrf,
    get_routing_routes,
)

AGENT_ROUTING = """You are a network tech lead that is specialized in the analysis of routing of network devices. You have access to a set of tools to connect to network devices and retrieve information about the network. Execute the tools to get the information you need to answer the requests. You decide tool or tools to use. 

You must only use the data (ip, interface name, description, status, etc.) provided by the tools as input for your response or input for the next tool to use. You must not make up any information or make assumptions.


Once you have all the information you need, you must answer the request in a concise and professional manner. This information will be used by a network engineer to take actions on the network.
"""

LLM_MODEL = "gpt-4o-mini"
tools = [
    get_vrf_present,
    get_interfaces_under_vrf,
    get_routing_routes,
]
model = ChatOpenAI(model=LLM_MODEL, temperature=0)


def agent_routing():
    return create_react_agent(model, tools=tools, prompt=AGENT_ROUTING)


if __name__ == "__main__":
    inputs = {
        "messages": [
            (
                "user",
                "Can you check the routes present on device cat8000v-0? I'm suspecting there is a problem with the routing.",
            )
        ]
    }

    graph = agent_routing()

    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
