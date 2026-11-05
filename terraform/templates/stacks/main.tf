{% for module in stack.modules %}
module "{{ module.name }}" {
  source = "../../modules/implementations/{{ module.type }}"

{% for param in module.parameters %}
  {{ param.name }} = {{ param.value }}
{% endfor %}
}
{% endfor %}