resource "aws_ecs_service" "dataflow_automation_prefect_agent" {
  cluster             = aws_ecs_cluster.dataflow_automation_prefect_agent.id
  desired_count       = 1
  launch_type         = "FARGATE"
  name                = "${var.env}_dataflow_automation_prefect_agent"
  scheduling_strategy = "REPLICA"
  task_definition     = aws_ecs_task_definition.dataflow_automation_prefect_agent.arn

  network_configuration {
    subnets          = module.vpc.public_subnets
    assign_public_ip = true
    security_groups  = [aws_security_group.dataflow_automation_prefect_agent.id]
  }
}
