from prefect_setup.prefect_project import prefect_project_setup

from prefect.utilities.exceptions import AuthorizationError
import pytest


def test_create_prefect_project_invalid_token(mocker):
    """
    Test create prefect project with invalid token
    """
    environment = "test"
    test_token_name = "MyPrefectPytestToken"  # < this token is not valid

    mocker.patch(
        "prefect_setup.prefect_project.prefect_project_setup.get_prefect_token",
        return_value=test_token_name,
    )

    with pytest.raises(
        AuthorizationError,
        match=f"Invalid API token provided. Check that the secret"
        f" '{test_token_name}' is set on AWS",
    ):
        prefect_project_setup.create_prefect_project(environment, test_token_name)
