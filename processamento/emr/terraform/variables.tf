variable "aws_access_key_id" {
  description = "AWS ACCESS KEY ID Credential"
  type        = string
  sensitive   = true
}
variable "aws_secret_access_key" {
  description = "AWS SECRET ACCESS KEY Credential"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "aws region"
  default     = "us-east-2"
}

variable "account_id" {
  default = 521738873930
}

variable "environment" {
  default = "dev"
}

variable "prefix" {
  description = "objects prefix"
  default     = "lrfaws"
}

variable "cluster_name" {
  description = "name of EMR cluster"
  default     = "lrfaws-education-cluster"
}

variable "lambdas" {
  type = map(string)
  default = {
    "testlambda1" = "testlambda1.zip",
    "testlambda2" = "testlambda2.zip",
    "testlambda3" = "testlambda3.zip",
    "testlambda4" = "testlambda4.zip"
  }
}

# Prefix configuration and project common tags
locals {
  prefix = var.prefix
  common_tags = {
    Environment = "dev"
    Project     = "aws-glue-eks-emr"
  }
}