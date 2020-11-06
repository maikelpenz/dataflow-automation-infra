resource "aws_security_group" "dataflow_automation_prefect_agent" {
  name        = "${var.env}_dataflow_automation_prefect_agent"
  description = "ecs cluster security group"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
