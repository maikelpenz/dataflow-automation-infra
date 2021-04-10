from datetime import datetime

import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from utils import is_resource_available, ResourceCheckStatus
from prefect_setup.prefect_register.prefect_helpers import PrefectHelpers

import boto3
from prefect import Client
import pytest

ECS_CLIENT = boto3.client("ecs")
ENV = "test"
PREFECT_HELPERS = PrefectHelpers()


def set_prefect_agent_status(status: str):
    """
    Brings the prefect agent up and down on ECS

    Parameters:
        status [str] -- active/inactive
    """
    agent_status = {"active": 1, "inactive": 0}

    ECS_CLIENT.update_service(
        cluster=f"{ENV}_dataflow_automation_prefect_agent",
        service=f"{ENV}_dataflow_automation_prefect_agent",
        desiredCount=agent_status.get(status),
    )


def is_agent_up_ecs():
    """
    Check if the agent is up on ECS
    """
    ecs_cluster = f"{ENV}_dataflow_automation_prefect_agent"
    tasks = ECS_CLIENT.list_tasks(cluster=ecs_cluster)
    if len(tasks.get("taskArns")) == 0:
        return ResourceCheckStatus.RETRY
    elif len(tasks.get("taskArns")) == 1:
        response = ECS_CLIENT.describe_tasks(
            cluster=ecs_cluster,
            tasks=[
                tasks.get("taskArns")[0],
            ],
        )
        if response.get("tasks")[0].get("containers")[0].get("lastStatus") == "RUNNING":
            return ResourceCheckStatus.FINISHED
        else:
            return ResourceCheckStatus.RETRY


def is_agent_up_prefect_cloud(pytestconfig):
    """
    Check if the agent is up on Prefect Cloud
    """

    # get prefect agent API token
    prefect_agent_token = pytestconfig.getoption("prefect_agent_token")

    # Instantiate the prefect client
    prefect_client = Client(api_token=prefect_agent_token)

    # query prefect cloud agents
    query = """
        query RunningFlows {
        agent {
                labels,
                last_queried
            }
        }
    """

    agents = prefect_client.graphql(query=query)["data"]["agent"]
    environment_agent_info = [
        item for item in agents if f"{ENV}_dataflow_automation" in item["labels"]
    ]
    if len(environment_agent_info) == 0:
        # agent doesn't even appear on prefect cloud yet
        return ResourceCheckStatus.RETRY
    else:
        last_queried_time = environment_agent_info[0]["last_queried"]

        # date
        last_queried_time = datetime.strptime(last_queried_time, "%Y-%m-%dT%H:%M:%S.%f%z")

        difference = datetime.utcnow().replace(tzinfo=None) - last_queried_time.replace(tzinfo=None)

        # If the agent has been queried recently (meaning it is up)
        if int(difference.total_seconds()) < 15:
            return ResourceCheckStatus.FINISHED
        else:
            # agent appears on prefect cloud but doesn't seem to be up
            return ResourceCheckStatus.RETRY


def test_prefect_agent_successfully(pytestconfig):
    """
    Test that we can successfully bring the prefect agent up
    """

    # Enable ECS agent
    set_prefect_agent_status("active")

    # Define function to wait for agent to be up on ECS
    def check_ecs_agent_status():
        return is_agent_up_ecs()

    # Wait for agent to be up on ECS
    is_resource_available(
        check_function=check_ecs_agent_status,
        wait_time_sec=60,
        backoff_rate=1,
        max_attempts=3,
    )

    # Define function to wait for agent to be up on Prefect Cloud
    def check_prefect_cloud_agent_status(pytestconfig):
        return is_agent_up_prefect_cloud(pytestconfig)

    # Wait for agent to be up on Prefect Cloud
    is_resource_available(
        check_function=check_prefect_cloud_agent_status,
        wait_time_sec=60,
        backoff_rate=1,
        max_attempts=3,
    )

    # Disable ECS agent
    set_prefect_agent_status("inactive")
