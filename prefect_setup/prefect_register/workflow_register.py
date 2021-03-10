import argparse
from workflow_helpers import WorkflowHelpers

parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, required=False, default=False)
parser.add_argument("--prefect_register_token_secret_name", type=str, required=False, default=False)
parser.add_argument("--prefect_execution_environment", type=str, required=False, default=False)
parser.add_argument("--workflow_cpu_configuration", type=int, required=False, default=False)
parser.add_argument("--workflow_memory_configuration", type=int, required=False, default=False)

args, unknown = parser.parse_known_args()
environment = args.env
prefect_register_token_secret_name = args.prefect_register_token_secret_name
prefect_execution_environment = args.prefect_execution_environment
workflow_cpu_configuration = args.workflow_cpu_configuration
workflow_memory_configuration = args.workflow_memory_configuration

# Instantiante Workflow Helpers
workflow_helpers = WorkflowHelpers()

# Register Workflow
workflow_helpers.register_workflow(
    environment,
    prefect_execution_environment,
    prefect_register_token_secret_name,
    workflow_cpu_configuration,
    workflow_memory_configuration,
)
