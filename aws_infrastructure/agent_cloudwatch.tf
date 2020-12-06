resource "aws_cloudwatch_log_group" "dataflow_automation_agent" {
  name = "${var.env}_dataflow_automation_agent"
}
