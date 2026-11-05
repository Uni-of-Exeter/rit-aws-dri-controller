{% for nom, value in context["parameters"].items() %}
variable "{{ nom }}" {
  type        = string
{% if value is string %}
  default     = "{{ value }}"
{% endif %}
}
{% endfor %}