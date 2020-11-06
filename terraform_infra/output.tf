output "agent_ecs_cluster_name" {
  value = aws_ecs_cluster.dataflow_automation_prefect_agent.name
}

output "agent_ecs_task_role_arn" {
  value = aws_iam_role.prefect_agent_ecs_task_role.arn
}

output "agent_ecs_task_execution_role_arn" {
  value = aws_iam_role.prefect_agent_ecs_task_execution_role.arn
}

output "vpc_public_subnets" {
  value = join("|", module.vpc.public_subnets)
}


