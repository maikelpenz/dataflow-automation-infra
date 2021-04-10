from prefect_setup.prefect_register.aws_conn_helpers import AwsConnHelpers
import pytest

ENVIRONMENT = "test"
aws_conn_helpers = AwsConnHelpers()


def test_create_ecr_repository_no_credentials():
    """
    Validate it fails to connect to AWS and not on other parts of the function
    """
    repository_name = "MyRepository"
    with pytest.raises(Exception, match="Unable to locate credentials"):
        aws_conn_helpers.create_ecr_repository(repository_name)


def test_describe_ecr_repositories_no_credentials():
    """
    Validate it fails to connect to AWS and not on other parts of the function
    """
    with pytest.raises(Exception, match="Unable to locate credentials"):
        aws_conn_helpers.describe_ecr_repositories([ENVIRONMENT])


def test_get_subnets_no_credentials():
    """
    Validate it fails to connect to AWS and not on other parts of the function
    """
    with pytest.raises(Exception, match="Unable to locate credentials"):
        aws_conn_helpers.get_subnets(ENVIRONMENT)


def test_get_iam_roles_no_credentials():
    """
    Validate it fails to connect to AWS and not on other parts of the function
    """
    with pytest.raises(Exception, match="Unable to locate credentials"):
        aws_conn_helpers.get_iam_roles(ENVIRONMENT)


def test_get_aws_creds_no_credentials():
    """
    Validate it fails to connect to AWS and not on other parts of the function
    """
    with pytest.raises(Exception, match="Unable to locate credentials"):
        aws_conn_helpers.get_aws_creds()


def test_ecr_authenticate_no_credentials():
    """
    Validate it fails to connect to AWS and not on other parts of the function
    """
    with pytest.raises(Exception, match="Unable to locate credentials"):
        aws_conn_helpers.ecr_authenticate()
