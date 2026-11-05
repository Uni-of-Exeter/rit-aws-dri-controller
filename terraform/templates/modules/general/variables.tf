{% for nom, value in context["parameters"].items() %}
variable "{{ nom }}" {
  type        = string
  default     = "{{ value }}"
}
{% endfor %}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
}