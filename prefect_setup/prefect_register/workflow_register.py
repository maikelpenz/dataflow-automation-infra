import argparse
from workflow_helpers import WorkflowHelpers

parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, required=False, default=False)
parser.add_argument("--prefect_register_token_secret_name", type=str, required=False, default=False)

args, unknown = parser.parse_known_args()
env = args.env
prefect_register_token_secret_name = args.prefect_register_token_secret_name

# Instantiante Workflow Helpers
workflow_helpers = WorkflowHelpers()
# Register Workflow
workflow_helpers.register_workflow(prefect_register_token_secret_name, env)
