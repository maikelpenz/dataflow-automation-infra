# import os
# from unittest import mock

# from prefect_setup.prefect_agent import start_agent

# from prefect.utilities.exceptions import AuthorizationError
# import pytest

# # Fixtures
# @pytest.fixture
# def fargate_agent_definition():
#     return start_agent.get_agent_definition(
#         "ecs_fargate",
#         subnets="123",
#         aws_region="ap-southeast-2",
#         environment="dev",
#         agent_cpu="2",
#         agent_memory="1024",
#         cluster_name="unit-test-cluster",
#         task_role_arn="arn::aws::unit-test-task-role",
#         execution_role_arn="arn::aws::unit-test-execution-role",
#     )


# # Tests
# def test_get_agent_definition_fargate_fields(fargate_agent_definition):
#     assert fargate_agent_definition.__dict__.get("task_run_kwargs").get("networkConfiguration").get(
#         "awsvpcConfiguration"
#     ).get("subnets") == ["123"]
#     assert (
#         fargate_agent_definition.__dict__.get("container_definitions_kwargs")
#         .get("logConfiguration")
#         .get("options")
#         .get("awslogs-region")
#         == "ap-southeast-2"
#     )
#     assert (
#         fargate_agent_definition.__dict__.get("container_definitions_kwargs")
#         .get("logConfiguration")
#         .get("options")
#         .get("awslogs-group")
#         == "dev_dataflow_automation_agent"
#     )
#     assert fargate_agent_definition.__dict__.get("labels") == ["dev_dataflow_automation"]
#     assert fargate_agent_definition.__dict__.get("task_definition_kwargs").get("cpu") == "2"
#     assert fargate_agent_definition.__dict__.get("task_definition_kwargs").get("memory") == "1024"
#     assert (
#         fargate_agent_definition.__dict__.get("task_run_kwargs").get("cluster")
#         == "unit-test-cluster"
#     )
#     assert (
#         fargate_agent_definition.__dict__.get("task_definition_kwargs").get("taskRoleArn")
#         == "arn::aws::unit-test-task-role"
#     )
#     assert (
#         fargate_agent_definition.__dict__.get("task_definition_kwargs").get("executionRoleArn")
#         == "arn::aws::unit-test-execution-role"
#     )


# def test_get_agent_definition_invalid_agent_type():
#     test_agent_type = "Fargateson"  # < this type is not valid
#     with pytest.raises(ValueError, match=f"'{test_agent_type}' is not a valid agent type"):
#         start_agent.get_agent_definition(test_agent_type)


# def test_start_agent_invalid_token(fargate_agent_definition):
#     test_token_name = "MyPrefectPytestToken"  # < this token is not valid
#     with mock.patch.dict(os.environ, {"PREFECT__CLOUD__AGENT__AUTH_TOKEN": test_token_name}):
#         with pytest.raises(
#             AuthorizationError,
#             match=f"Invalid API token provided. Check that the secret"
#             f" '{test_token_name}' is set on AWS",
#         ):
#             start_agent.start_agent(fargate_agent_definition, test_token_name)
