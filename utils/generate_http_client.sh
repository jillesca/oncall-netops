#!/bin/bash

HTTP_CLIENT_OPENAPI_FILE=${HTTP_CLIENT_OPENAPI_FILE}

if [ "${HTTP_CLIENT_OPENAPI_FILE}" = "openapi.json" ]; then
    echo "Filename conflict: 'openapi.json' cannot be used as it conflicts with the Langgraph API validator. Please choose another name for your openapi file."
    exit 1
fi

if [ ! -f "${PWD}/${HTTP_CLIENT_OPENAPI_FILE}" ]; then
    echo "Can't find the openapi file used for code generation (missing: ${HTTP_CLIENT_OPENAPI_FILE})."
    exit 1
fi

echo "# Generating the HTTP client"

DOCKER=$(command -v docker 2> /dev/null || echo podman)

$DOCKER run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i /local/"${HTTP_CLIENT_OPENAPI_FILE}" \
    -g python \
    -o /local/pyats_client \
    --package-name pyats_client

echo "# Installing the HTTP client"
uv add ./pyats_client

echo "# Checking the installed package"
uv pip list | grep pyats-client

echo "# Done generating the HTTP client"