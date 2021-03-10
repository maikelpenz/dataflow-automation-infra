import logging
import os
import sys
from typing import Tuple

sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from botocore.exceptions import ClientError
from prefect import Client
from prefect.storage import Docker
from prefect.run_configs import ECSRun

from prefect_helpers import PrefectHelpers
from aws_conn_helpers import AwsConnHelpers

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class WorkflowHelpers:
    def __init__(self) -> None:
        self.aws_conn_helpers = AwsConnHelpers()
        self.prefect_helpers = PrefectHelpers()

    def create_workflow_ecr_repository(self, flow_name: str) -> None:
        """
        Create ECR repository for flow

        Parameters:
            flow_name [string] -- Name of the workflow being pushing
        """
        try:
            # Check if repository already exists
            self.aws_conn_helpers.describe_ecr_repositories(repository_names=[flow_name])
        except ClientError:
            # If the repository doesn't exist
            try:
                # Create the ECR repository
                self.aws_conn_helpers.create_ecr_repository(repository_name=flow_name)
            except ClientError as e:
                raise e
            else:
                print(f"ECR repository for workflow '{flow_name}' created !")
        else:
            print(f"ECR repository for workflow '{flow_name}' already exists !")

    def import_flow(self) -> object:
        """
        Import flow
        """
        return __import__("flow")

    def set_workflow_properties(
        self,
        environment: str,
        prefect_execution_environment: str,
        workflow_cpu_configuration: int,
        workflow_memory_configuration: int,
    ) -> Tuple:
        """
        Construct the Workflow object with its properties

        Parameters:
            environment [string] -- environment the workflow should be pushed to
            prefect_execution_environment [string] -- e.g: ecs_fargate, kubernetes
            workflow_cpu_configuration [int] -- e.g: 256,512,1024,2048,4096
            workflow_memory_configuration [int] -- e.g: 512,30720
        """
        (
            account_id,
            aws_region,
            subnets,
            execution_role_arn,
            task_role_arn,
        ) = self.prefect_helpers.get_prefect_aws_infrastructure(environment)

        # import flow
        flow_module = self.import_flow()

        flow_name = f"{environment}_{flow_module.flow.name}"
        flow_module.flow.name = flow_name

        if prefect_execution_environment == "ecs_fargate":
            flow_module.flow.storage = Docker(
                registry_url=f"{account_id}.dkr.ecr.{aws_region}.amazonaws.com",
                image_name=flow_name,
                image_tag="latest",
                python_dependencies=["boto3"],
                env_vars={"PYTHONPATH": "/opt/prefect/flows"},
            )

            flow_module.flow.run_config = ECSRun(
                run_task_kwargs={
                    "cluster": f"{environment}_dataflow_automation_workflows",
                },
                execution_role_arn=execution_role_arn,
                labels=[f"{environment}_dataflow_automation"],
                cpu=workflow_cpu_configuration,
                memory=workflow_memory_configuration,
            )

        return flow_module, flow_name

    def register_workflow(
        self,
        environment: str,
        prefect_execution_environment: str,
        prefect_register_token_secret_name: str,
        workflow_cpu_configuration: int,
        workflow_memory_configuration: int,
    ) -> None:
        """
        Registers the workflow to Prefect Cloud

        Parameters:
            environment [string] -- environment the workflow should be pushed to
            prefect_execution_environment [string] -- e.g: ecs_fargate, kubernetes
            prefect_register_token_secret_name [string]
                -- name of aws secrets manager secret where prefect register token is stored
            workflow_cpu_configuration [int] -- e.g: 256,512,1024,2048,4096
            workflow_memory_configuration [int] -- e.g: 512,30720
        """

        # set flow properties
        flow_module, flow_name = self.set_workflow_properties(
            environment,
            prefect_execution_environment,
            workflow_cpu_configuration,
            workflow_memory_configuration,
        )

        # Authenticate to ECR as the registration process pushes the image to AWS
        self.aws_conn_helpers.ecr_authenticate()

        # Create ECR repository
        self.create_workflow_ecr_repository(flow_name=flow_name)

        # get prefect workflow register API token
        prefect_api_token = self.prefect_helpers.get_prefect_token(
            secret_name=prefect_register_token_secret_name
        )

        try:
            # Instantiate the prefect client
            prefect_client = Client(api_token=prefect_api_token)

            # Register the Workflow
            prefect_client.register(
                flow=flow_module.flow, project_name=f"{environment}_dataflow_automation"
            )
        except Exception as e:
            raise e
        else:
            logging.info(f"Workflow '{flow_name}' registered successfully!")
