#!/bin/bash
set -e

# Validate P_VALUE
if [ -z "$P_VALUE" ]; then
    echo "Error: P_VALUE environment variable not set"
    exit 1
fi

# Set weights
export USER_SERVICE_V1_WEIGHT=$P_VALUE
export USER_SERVICE_V2_WEIGHT=$((100 - P_VALUE))