provider "aws" {
  region = "${var.aws_region}"
}

terraform {
  backend "s3" {
    region = "ap-southeast-2" # dataflow-automation-infra-artifacts
  }
}

# https://zoph.me/posts/2020-03-08-github-actions/
# https://github.com/z0ph/aws_managed_policies/tree/master/automation/tf-fargate
