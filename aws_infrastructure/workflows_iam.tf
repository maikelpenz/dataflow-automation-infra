# Workflow ECS Task Role.

resource "aws_iam_role" "prefect_workflow_ecs_task_role" {
  name = "${var.env}_prefect_workflow_ecs_task_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ecs-tasks.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "prefect_workflow_ecs_task_policy" {
  name   = "${var.env}_prefect_workflow_ecs_task_policy"
  policy = data.template_file.prefect_workflow_ecs_task_policy.rendered
}

data "template_file" "prefect_workflow_ecs_task_policy" {
  template = file("${path.module}/policies/prefect_workflow_ecs_task_policy.json")
}

resource "aws_iam_role_policy_attachment" "prefect_workflow_ecs_task_role_attachment" {
  role       = aws_iam_role.prefect_workflow_ecs_task_role.name
  policy_arn = aws_iam_policy.prefect_workflow_ecs_task_policy.arn
}

# Workflow ECS Task Execution Role.

resource "aws_iam_role" "prefect_workflow_ecs_task_execution_role" {
  name = "${var.env}_prefect_workflow_ecs_task_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ecs-tasks.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "prefect_workflow_ecs_task_execution_policy" {
  name   = "${var.env}_prefect_workflow_ecs_task_execution_policy"
  policy = data.template_file.prefect_workflow_ecs_task_execution_policy.rendered
}

data "template_file" "prefect_workflow_ecs_task_execution_policy" {
  template = file("${path.module}/policies/prefect_workflow_ecs_task_execution_policy.json")
}

resource "aws_iam_role_policy_attachment" "prefect_workflow_ecs_task_execution_role_attachment" {
  role       = aws_iam_role.prefect_workflow_ecs_task_execution_role.name
  policy_arn = aws_iam_policy.prefect_workflow_ecs_task_execution_policy.arn
}
