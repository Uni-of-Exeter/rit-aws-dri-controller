from rit_aws_dri_controller.stacks.renderer import StackRenderer


def test_renderer_init():
    assert StackRenderer() is not None
