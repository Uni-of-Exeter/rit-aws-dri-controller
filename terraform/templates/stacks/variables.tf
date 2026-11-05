variable "aws_region" {
  type = string
}

variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "client" {
  type = string
  default = "research-it"
  description = "Client code or identifier that facilitates billing - maps to default tags"
}