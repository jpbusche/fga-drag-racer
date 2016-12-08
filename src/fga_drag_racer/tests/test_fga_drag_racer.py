import pytest
import fga_drag_racer


def test_project_defines_author_and_version():
    assert hasattr(fga_drag_racer, '__author__')
    assert hasattr(fga_drag_racer, '__version__')
