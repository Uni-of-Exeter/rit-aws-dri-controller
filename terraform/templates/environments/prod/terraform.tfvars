{% extends "environments/terraform.tfvars" %}
{% block header %}
aws_region   = "eu-west-2"
project_name = "project_name"
environment  = "production"
{% endblock %}
