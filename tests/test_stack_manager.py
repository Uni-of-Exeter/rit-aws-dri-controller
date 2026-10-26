from rit_aws_dri_controller.stacks.manager import StackManager

def test_manager_init():
    m = StackManager()
    assert m is not None
