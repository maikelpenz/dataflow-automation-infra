from prefect_setup.prefect_register.workflow_helpers import WorkflowHelpers

from botocore.exceptions import ClientError
import pytest

FLOW_NAME = "my-ecr-workflow"
workflow_helpers = WorkflowHelpers()


def test_create_workflow_ecr_repository_already_exists(mocker, capsys):
    """
    Test that it won't create the ecr repository because it already exists
    """
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.describe_ecr_repositories",
        return_value=True,
    )
    workflow_helpers.create_workflow_ecr_repository(FLOW_NAME)
    out, _ = capsys.readouterr()
    assert out.replace("\n", "") == f"ECR repository for workflow '{FLOW_NAME}' already exists !"


def test_create_workflow_ecr_repository_success(mocker, capsys):
    """
    Test that it can create the ecr repository
    """
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.describe_ecr_repositories",
        side_effect=ClientError({"Error": {"Code": ""}}, ""),
    )
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.create_ecr_repository",
        return_value=True,
    )
    workflow_helpers.create_workflow_ecr_repository(FLOW_NAME)
    out, _ = capsys.readouterr()
    assert out.replace("\n", "") == f"ECR repository for workflow '{FLOW_NAME}' created !"


def test_create_workflow_ecr_repository_fail(mocker):
    """
    Test that it cannot the ecr repository and a ClientError is thrown
    """
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.describe_ecr_repositories",
        side_effect=ClientError({"Error": {"Code": ""}}, ""),
    )
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.create_ecr_repository",
        side_effect=ClientError({"Error": {"Code": ""}}, ""),
    )
    with pytest.raises(ClientError):
        workflow_helpers.create_workflow_ecr_repository(FLOW_NAME)


def test_set_workflow_properties(mocker):
    """
    Test setting the workflow environment
    """
    environment = "test"
    execution_environment = "ecs_fargate"

    mocker.patch(
        "prefect_helpers.PrefectHelpers.get_prefect_aws_infrastructure",
        return_value=(1, 2, 3),
    )
    mocker.patch("prefect_setup.prefect_register.workflow_helpers.WorkflowHelpers.import_flow")

    flow_module, _ = workflow_helpers.set_workflow_properties(environment, execution_environment)

    # assert flow_module.flow.environment.labels == {f"{environment}_dataflow_automation"}
    # assert flow_module.flow.environment.launch_type == "FARGATE"


def test_register_workflow(mocker):
    """
    Test registering a workflow
    """
    mocker.patch(
        "prefect_setup.prefect_register.workflow_helpers.WorkflowHelpers.set_workflow_properties",
        return_value=(None, None),
    )
    mocker.patch(
        "aws_conn_helpers.AwsConnHelpers.ecr_authenticate",
        return_value=None,
    )
    mocker.patch(
        "prefect_setup.prefect_register.workflow_helpers.WorkflowHelpers.create_workflow_ecr_repository",
        return_value=None,
    )
    mocker.patch(
        "prefect_helpers.PrefectHelpers.get_prefect_token",
        return_value="PrefectToken",
    )
    with pytest.raises(Exception, match="'NoneType' object has no attribute 'flow'"):
        workflow_helpers.register_workflow("test", "ecs_fargate", "PrefectTokenSecret")
