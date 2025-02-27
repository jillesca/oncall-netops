#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the PYTHONPATH to the root directory of the project
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Print the PYTHONPATH for debugging
echo "# PYTHONPATH is set to: $PYTHONPATH"