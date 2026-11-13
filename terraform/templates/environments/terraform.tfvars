# This file serves sensible starting values. For each stack you'll want to extend these!

{% block header %}
aws_region   = "eu-west-2"
project_name = "defproj"
environment  = "dev"
{% endblock %}

{% block networks %}
# --- Networking ---
vpc_cidr            = "10.0.0.0/16"
public_subnet_cidr  = "10.0.1.0/24"
private_subnet_cidr = "10.0.2.0/24"

# University of Exeter CIDR blocks — restrict SSH to campus network
# Replace with actual University CIDR ranges
university_cidr_blocks = ["192.168.0.0/16"]
{% endblock %}

