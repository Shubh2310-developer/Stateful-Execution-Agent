variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = "string"
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name of the application"
  type        = "string"
  default     = "stateful-execution-agent"
}

variable "db_username" {
  description = "Username for the databases"
  type        = "string"
  sensitive   = true
}

variable "db_password" {
  description = "Password for the databases"
  type        = "string"
  sensitive   = true
}
