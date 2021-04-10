FROM prefecthq/prefect

# Install required libraries
RUN pip3 install boto3

# Copy required agent startup files
COPY start_agent.py /prefect_setup/start_agent.py
RUN touch /prefect_setup/__init__.py

# Agent Configuration variables
ARG agent_type_arg=None
ENV agent_type_env=$agent_type_arg

ARG cluster_name_arg=None
ENV cluster_name_env=$cluster_name_arg

ARG aws_region_arg=None
ENV aws_region_env=$aws_region_arg

ARG agent_cpu_arg=None
ENV agent_cpu_env=$agent_cpu_arg

ARG agent_memory_arg=None
ENV agent_memory_env=$agent_memory_arg

ARG agent_memory_arg=None
ENV agent_memory_env=$agent_memory_arg

ARG task_role_arn_arg=None
ENV task_role_arn_env=$task_role_arn_arg

ARG execution_role_arn_arg=None
ENV execution_role_arn_env=$execution_role_arn_arg

ARG subnets_arg=None
ENV subnets_env=$subnets_arg

ARG environment_arg=None
ENV environment_env=$environment_arg

ARG prefect_agent_token_arg=None
ENV prefect_agent_token_env=$prefect_agent_token_arg

# Set to start the agent when image comes up 
ENTRYPOINT python3 /prefect_setup/start_agent.py \
    --agent_type=$agent_type_env \
    --cluster_name=$cluster_name_env \
    --aws_region=$aws_region_env \
    --agent_cpu=$agent_cpu_env \
    --agent_memory=$agent_memory_env \
    --task_role_arn=$task_role_arn_env \
    --execution_role_arn=$execution_role_arn_env \
    --subnets=$subnets_env \
    --environment=$environment_env \
    --prefect_agent_token=$prefect_agent_token_env