{% for nom, value in context["parameters"].items() %}
variable "{{ nom }}" {
  type        = {{ context["types"][nom] }}
{% if value is string %}
  default     = "{{ value }}"
{% elif value is iterable %}
  default     = {{ value|replace("'", "\"") }}
{% endif %}
}
{% endfor %}