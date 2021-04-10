from prefect_setup.prefect_project import prefect_project_setup

from prefect.utilities.exceptions import AuthorizationError
import pytest


def test_create_prefect_project_invalid_token(mocker):
    """
    Test create prefect project with invalid token
    """
    environment = "test"

    with pytest.raises(
        AuthorizationError,
        match="Invalid API token provided. Check that the secret "
        "PREFECT_AGENT_TOKEN is set on the Github repository configuration",
    ):
        prefect_project_setup.create_prefect_project(environment, "InvalidToken")
