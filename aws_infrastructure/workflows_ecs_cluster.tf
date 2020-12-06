resource "aws_ecs_cluster" "dataflow_automation_workflows" {
  name = "${var.env}_dataflow_automation_workflows"
  capacity_providers = [
    "FARGATE"
  ]
}
