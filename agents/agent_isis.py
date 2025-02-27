from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.pyats.pyats_isis_tools import (
    get_isis_neighbors,
    get_isis_interface_information,
    get_isis_interface_events,
)
from tools.pyats.pyats_interface_status_tools import (
    get_interface_running_config,
)

AGENT_ISIS_PROMPT = """You are an expert in ISIS protocol operations. Your focus is on examining ISIS configurations and network topology. You have access to a set of tools to connect to network devices and retrieve information about the network. Execute the tools to get the information you need to answer the requests. You decide tool or tools to use. 

You must only use the data (ip, interface name, description, status, etc.) provided by the tools as input for your response or input for the next tool to use. You must not make up any information or make assumptions.



Always review the configuration of the device to review if ISIS was intended to be used.

Once you have all the information you need, you must answer the request in a concise and professional manner. This information will be used by a network engineer to take actions on the network.
"""

LLM_MODEL = "gpt-4o-mini"
tools = [
    get_isis_neighbors,
    get_isis_interface_information,
    get_isis_interface_events,
    get_interface_running_config,
]
model = ChatOpenAI(model=LLM_MODEL, temperature=0)


def agent_isis():
    return create_react_agent(model, tools=tools, prompt=AGENT_ISIS_PROMPT)


if __name__ == "__main__":
    inputs = {
        "messages": [
            (
                "user",
                "I think ISIS is not working on device cat8000v-0, can you check?",
            )
        ]
    }

    graph = agent_isis()

    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
