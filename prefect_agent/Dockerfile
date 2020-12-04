FROM prefecthq/prefect

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

COPY start_agent.sh /usr/local/start_agent.sh
COPY helpers.py /usr/local/helpers.py
COPY start_agent.py /usr/local/start_agent.py

ENTRYPOINT /usr/local/start_agent.sh \
    $cluster_name_env \
    $aws_region_env \ 
    $agent_cpu_env \
    $agent_memory_env \
    $task_role_arn_env \
    $execution_role_arn_env \
    $subnets_env \
    $environment_env