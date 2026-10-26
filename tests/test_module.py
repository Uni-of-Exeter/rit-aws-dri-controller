from pathlib import Path

from rit_aws_dri_controller.modules.generator import (
    ModuleGenerator,
)


def test_data_module_creation(
    tmp_path,
):

    templates = (
        tmp_path /
        "templates"
    )

    impls = (
        tmp_path /
        "implementations"
    )

    data = templates / "data"

    data.mkdir(
        parents=True
    )

    (
        data /
        "main.tf.j2"
    ).write_text(
        'resource "aws_s3_bucket" "{{ name }}" {}'
    )

    generator = ModuleGenerator(
        template_root=str(
            templates
        ),
        implementation_root=str(
            impls
        ),
    )

    generator.create_module(
        "data",
        "lakehouse",
    )

    created = (
        impls /
        "data" /
        "lakehouse" /
        "main.tf"
    )

    assert created.exists()