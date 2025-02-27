import os
import io
from PIL import Image as PILImage
from langgraph.graph import StateGraph
from graph_state_shemas import AgentState


def set_env(var: str):
    env_value = os.environ.get(var)
    os.environ[var] = env_value


def save_report(state: AgentState):
    with open("resolution_report.md", "w", encoding="utf-8") as f:
        f.write(state["resolution_log"])


def save_workflow(graph: StateGraph):
    # Show the workflow
    image_data = graph.get_graph().draw_mermaid_png()
    image = PILImage.open(io.BytesIO(image_data))
    image.save("workflow_diagram.png")
