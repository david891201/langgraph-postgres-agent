#!/bin/sh

# Set paths using basic syntax
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export PYTHONPATH=.

START_PATH="${APP_HOME}/src/main.py"
CONF_PATH="conf/job.conf"

# Create logs directory
mkdir -p logs

# Run Python script with arguments
python ${START_PATH} --config ${CONF_PATH} $@