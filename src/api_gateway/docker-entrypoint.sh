#!/bin/bash
set -e

# Replace environment variables in kong.yml.template
envsubst < /etc/kong/kong.yml.template > /etc/kong/kong.yml

# Prepare Kong prefix directory
kong prepare -p /usr/local/kong

# Start Kong
exec kong start --nginx-conf /usr/local/kong/nginx.conf --vv