variable "tf_artifacts_bucket" {
  description = "Artifacts Bucket Name"
}

variable "aws_region" {
  description = "AWS Region"
}

variable "env" {
  description = "Environment"
}

variable "prefect_agent_up" {
  description = "Defines if the prefect agent will be up or down in this environment"
}
