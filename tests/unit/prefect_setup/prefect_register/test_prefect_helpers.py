from prefect_setup.prefect_register.prefect_helpers import PrefectHelpers

import pytest

FLOW_NAME = "my-ecr-workflow"
ENVIRONMENT = "test"
prefect_helpers = PrefectHelpers()


def test_get_prefect_token_successful(mocker):
    """
    Test if we can successfully retrieve the token
    """
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.get_secrets_manager_value",
        return_value={
            "SecretString": '{"MyPrefectPytestToken":"tHiSiStHeValuE"}',
        },
    )
    assert prefect_helpers.get_prefect_token("MyPrefectPytestToken") == "tHiSiStHeValuE"


def test_get_prefect_token_failed(mocker):
    """
    Test if we cannot successfully retrieve the token
    """
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.get_secrets_manager_value",
        return_value="tHiSiStHeValuE",
    )
    with pytest.raises(Exception, match="Invalid secret value"):
        prefect_helpers.get_prefect_token("MyPrefectPytestToken")


def test_get_prefect_aws_infrastructure(mocker):
    """
    Test get prefect AWS infrastructure to register workflow
    """
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.get_subnets",
        return_value="subnets",
    )
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.get_iam_roles",
        return_value=("iam_role1", "iam_role2"),
    )
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.get_aws_creds",
        return_value=("account_id", "aws_region"),
    )
    assert (
        "account_id",
        "aws_region",
        "subnets",
        "iam_role1",
        "iam_role2",
    ) == prefect_helpers.get_prefect_aws_infrastructure(ENVIRONMENT)
