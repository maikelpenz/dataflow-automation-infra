import argparse
import os

from helpers import get_prefect_token

from prefect.client import Client


def create_prefect_project(environment: str):
    client = Client(api_token=get_prefect_token(secret_name="prefectagenttoken"))
    client.create_project(project_name=f"{environment}_dataflow_automation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", type=str, required=False, default=False)

    args, unknown = parser.parse_known_args()
    environment = args.environment

    create_prefect_project(environment)
