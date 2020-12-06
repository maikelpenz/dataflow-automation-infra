provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    region = "ap-southeast-2"
  }
}
