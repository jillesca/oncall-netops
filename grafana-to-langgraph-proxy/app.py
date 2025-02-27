import os
import logging
import httpx
from fastapi import FastAPI, Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

app = FastAPI()


def get_assistant_id():
    return os.getenv("LANGGRAPH_ASSISTANT_ID", "oncall-netops")


def get_langgraph_api_endpoint():
    return os.getenv(
        "LANGGRAPH_API_ENDPOINT", "http://host.docker.internal:56000/runs"
    )


def construct_langgraph_data(grafana_data):
    title = grafana_data.get("title", "")
    message = grafana_data.get("message", "")
    return {
        "assistant_id": get_assistant_id(),
        "input": {
            "incident_description": {
                "title": title,
                "message": message,
                "alerts": [
                    {
                        "device": alert.get("labels", {}).get("device", ""),
                        "alertname": alert.get("labels", {}).get(
                            "alertname", ""
                        ),
                        "annotations": alert.get("annotations", {}),
                        "startsat": alert.get("startsAt", ""),
                        "dashboardurl": alert.get("dashboardURL", ""),
                    }
                    for alert in grafana_data.get("alerts", [])
                ],
            }
        },
        "on_completion": "keep",
        "on_disconnect": "continue",
        "after_seconds": 1,
    }


@app.post("/webhook")
async def handle_webhook(request: Request):
    grafana_data = await request.json()
    logger.info("Received webhook: %s", grafana_data)

    alert_status = grafana_data.get("status", "")
    if alert_status == "firing":
        langgraph_data = construct_langgraph_data(grafana_data)
        logger.info("Constructed LangGraph data: %s", langgraph_data)

        langgraph_api_endpoint = get_langgraph_api_endpoint()

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.post(
                    langgraph_api_endpoint,
                    json=langgraph_data,
                    headers={
                        "Accept": "*/*",
                        "Content-Type": "application/json",
                    },
                )
            response.raise_for_status()
            logger.info(
                "Received response from LangGraph API: %s", response.json()
            )
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error occurred: %s", e)
        except httpx.RequestError as e:
            logger.error("Request error occurred: %s", e)
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)

    return {"status": "success"}
