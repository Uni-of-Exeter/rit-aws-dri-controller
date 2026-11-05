{% for module in stack.modules %}
module "{{ module.name }}" {
  source = "../../modules/implementations/{{ module.type }}"

{% for k, v in module.params.items() %}
  {{ k }} = {{ v }}
{% endfor %}
}
{% endfor %}