{% extends "../terraform.tfvars.j2" %}
{% block header %}
aws_region   = "eu-west-2"
project_name = "project_name"
environment  = "production"
{% endblock %}
