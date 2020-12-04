from prefect import Client
from prefect.environments import FargateTaskEnvironment
from prefect.environments.storage import Docker

from workflows.imu_ahrs_data_loss import data_loss_check
from .ecr_authentication import ecr_authenticate

# Get Workflow object
flow_module = data_loss_check.flow

flow_module.environment = FargateTaskEnvironment(
    requiresCompatibilities=["FARGATE"],
    region="ap-southeast-2",
    labels=["dev_dataflow_automation"],
    taskDefinition="dev_data_loss_check",
    family="dev_data_loss_check",
    cpu="512",
    memory="3072",
    networkMode="awsvpc",
    networkConfiguration={
        "awsvpcConfiguration": {
            "assignPublicIp": "ENABLED",
            "subnets": [
                "subnet-05c3fcfce9275d195",
                "subnet-02410b882477eea13",
                "subnet-05d07984082846a2b",
            ],
            "securityGroups": [],
        }
    },
    containerDefinitions=[
        {
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-region": "ap-southeast-2",
                    "awslogs-group": "dev_dataflow_automation_workflows",
                    "awslogs-stream-prefix": "dev_data_loss_check",
                },
            }
        }
    ],
    executionRoleArn="arn:aws:iam::844814218183:role/dev_prefect_workflow_ecs_task_execution_role",
    taskRoleArn="arn:aws:iam::844814218183:role/dev_prefect_workflow_ecs_task_role",
    cluster="dev_dataflow_automation_workflows",
)

# Set the flow storage. Where to get the code from
flow_module.storage = Docker(
    registry_url="844814218183.dkr.ecr.ap-southeast-2.amazonaws.com",
    image_name="dev_data_loss_check",
    image_tag="latest",
    python_dependencies=["boto3"],
    env_vars={"PYTHONPATH": "/opt/prefect/flows"},
)

# Authenticate to ECR as the registration process pushes the image to AWS
ecr_authenticate()

# Instantiate the prefect client
prefect_client = Client(api_token="<token>")

# Register the Workflow
prefect_client.register(flow=flow_module, project_name="dev_dataflow_automation")
