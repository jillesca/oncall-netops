#!/bin/bash


required_vars=(
    OPENAI_API_KEY
    PYATS_API_SERVER
    LANGSMITH_TRACING
    LANGSMITH_API_KEY
    LANGSMITH_ENDPOINT
    LANGGRAPH_API_PORT
    LANGGRAPH_API_ENDPOINT
    LANGGRAPH_ASSISTANT_ID
    HTTP_CLIENT_OPENAPI_FILE
    GRAFANA_TO_LANGGRAPH_PROXY_PORT
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error, Environment Variable: $var is not set."
        exit 1
    fi
done

echo "# All required environment variables are set."
