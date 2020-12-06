data "aws_caller_identity" "target_account" {}

resource "aws_ecs_task_definition" "dataflow_automation_prefect_agent" {
  family                   = "${var.env}_dataflow_automation_prefect_agent"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  task_role_arn            = aws_iam_role.prefect_agent_ecs_task_role.arn
  execution_role_arn       = aws_iam_role.prefect_agent_ecs_task_execution_role.arn
  tags                     = {}
  container_definitions = jsonencode(
    [
      {
        name : "${var.env}_dataflow_automation_prefect_agent"
        container_name : "${var.env}_dataflow_automation_prefect_agent"
        cpu         = 256
        image       = "${data.aws_caller_identity.target_account.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.env}_dataflow_automation_agent"
        essential   = true
        mountPoints = []
        volumesFrom = []
        memoryReservation : 512,
        logConfiguration : {
          "logDriver" : "awslogs",
          "options" : {
            "awslogs-region" : var.aws_region,
            "awslogs-group" : "${var.env}_dataflow_automation_agent",
            "awslogs-stream-prefix" : "agent_status",
          },
        },
      }
  ])
}
