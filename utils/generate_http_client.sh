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

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i /local/"${HTTP_CLIENT_OPENAPI_FILE}" \
    -g python \
    -o /local/pyats_client \
    --package-name pyats_client

echo "# Installing the HTTP client"
cd pyats_client
pip install .

echo "# Checking the installed package"
pip list | grep pyats-client
cd -

echo "# Done generating the HTTP client"