resource "aws_cloudwatch_log_group" "dataflow_automation_workflows" {
  name = "${var.env}_dataflow_automation_workflows"
}
