resource "aws_ecs_cluster" "dataflow_automation_prefect_agent" {
  name = "${var.env}_dataflow_automation_prefect_agent"
  capacity_providers = [
    "FARGATE"
  ]
}
