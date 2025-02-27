from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools.pyats.pyats_health_tools import (
    get_health_memory,
    get_health_cpu,
)

AGENT_DEVICE_HEALTH = """You are a network tech lead that is specialized in the analysis of health of network devices. You have access to a set of tools to connect to network devices and retrieve information about the network. Execute the tools to get the information you need to answer the requests. You decide tool or tools to use. 

You must only use the data (ip, interface name, description, status, etc.) provided by the tools as input for your response or input for the next tool to use. You must not make up any information or make assumptions.


Once you have all the information you need, you must answer the request in a concise and professional manner. This information will be used by a network engineer to take actions on the network.
"""

LLM_MODEL = "gpt-4o-mini"
tools = [
    get_health_memory,
    get_health_cpu,
]
model = ChatOpenAI(model=LLM_MODEL, temperature=0)


def agent_device_health():
    return create_react_agent(model, tools=tools, prompt=AGENT_DEVICE_HEALTH)


if __name__ == "__main__":
    inputs = {
        "messages": [
            (
                "user",
                "Can you check the device cat8000v-0 is healthy?",
            )
        ]
    }

    graph = agent_device_health()

    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
