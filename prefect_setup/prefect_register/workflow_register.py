import argparse
from workflow_helpers import WorkflowHelpers

parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, required=False, default=False)
parser.add_argument("--prefect_workflow_register_token", type=str, required=False, default=False)
parser.add_argument("--prefect_execution_environment", type=str, required=False, default=False)
parser.add_argument("--workflow_cpu_configuration", type=int, required=False, default=False)
parser.add_argument("--workflow_memory_configuration", type=int, required=False, default=False)

args, unknown = parser.parse_known_args()
environment = args.env
prefect_workflow_register_token = args.prefect_workflow_register_token
prefect_execution_environment = args.prefect_execution_environment
workflow_cpu_configuration = args.workflow_cpu_configuration
workflow_memory_configuration = args.workflow_memory_configuration

# Instantiante Workflow Helpers
workflow_helpers = WorkflowHelpers()

# Register Workflow
workflow_helpers.register_workflow(
    environment,
    prefect_execution_environment,
    prefect_workflow_register_token,
    workflow_cpu_configuration,
    workflow_memory_configuration,
)
