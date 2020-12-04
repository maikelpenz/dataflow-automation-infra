resource "aws_ecr_repository" "dataflow_automation_agent" {
  name = "${var.env}_dataflow_automation_agent"

  image_scanning_configuration {
    scan_on_push = true
  }
}
