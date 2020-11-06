#!/bin/sh -l

# Install prefect every time the container starts to get the latest version
pip3 install --user prefect
pip3 install --user boto3

cluster_name=$1
aws_region=$2
agent_cpu=$3
agent_memory=$4
task_role_arn=$5
execution_role_arn=$6
subnets=$7
environment=$8

python3 /usr/local/start_agent.py \
 --cluster_name=$cluster_name \
 --aws_region=$aws_region \
 --agent_cpu=$agent_cpu \
 --agent_memory=$agent_memory \
 --task_role_arn=$task_role_arn \
 --execution_role_arn=$execution_role_arn \
 --subnets=$subnets \
 --environment=$environment