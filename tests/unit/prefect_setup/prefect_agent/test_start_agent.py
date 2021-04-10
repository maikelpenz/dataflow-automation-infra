import os
from unittest import mock

from prefect_setup.prefect_agent import start_agent

from prefect.agent.ecs.agent import ECSAgent
from prefect.utilities.exceptions import AuthorizationError
import pytest

# Fixtures
@pytest.fixture
def ecs_fargate_agent_definition(mocker):
    mocker.patch(
        "prefect_setup.prefect_agent.start_agent._get_ecs_fargate_agent_definition",
        return_value=ECSAgent(
            region_name="ap-southeast-2",
            cluster="unit-test-cluster",
            labels=["test_dataflow_automation"],
            run_task_kwargs_path="tests/unit/prefect_setup/prefect_agent/agent_conf_mock.yaml",
        ),
    )
    return start_agent.get_agent_definition("ecs_fargate")


def test_get_agent_definition_invalid_agent_type():
    test_agent_type = "Fargateson"  # < this type is not valid
    with pytest.raises(ValueError, match=f"'{test_agent_type}' is not a valid agent type"):
        start_agent.get_agent_definition(test_agent_type)


def test_start_agent_invalid_token(ecs_fargate_agent_definition):
    test_token_name = "MyPrefectPytestToken"  # < this token is not valid
    with mock.patch.dict(os.environ, {"PREFECT__CLOUD__AGENT__AUTH_TOKEN": test_token_name}):
        with pytest.raises(
            AuthorizationError,
            match="Invalid API token provided. Check that the secret "
            "PREFECT_AGENT_TOKEN is set on the Github repository configuration",
        ):
            start_agent.start_agent(ecs_fargate_agent_definition, test_token_name)
