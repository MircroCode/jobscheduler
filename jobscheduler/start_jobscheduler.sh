#!/usr/bin/env bash
SCRIPT_NAME=$0
CUR_DIR=`dirname ${SCRIPT_NAME}`
nohup python ${CUR_DIR}/jobscheduler.py &
echo "job scheduler has started! see log at /tmp/jobscheduler."