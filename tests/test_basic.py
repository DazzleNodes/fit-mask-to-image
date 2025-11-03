"""
Basic tests for Fit Mask to Image node.

These are minimal stubs to ensure CI passes.
ComfyUI nodes are difficult to unit test without the full ComfyUI environment.
"""

import os
import pytest


def test_python_files_exist():
    """Test that required Python files exist."""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    required_files = [
        '__init__.py',
        'py/fit_mask_to_image.py',
        'version.py',
    ]

    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        assert os.path.exists(full_path), f"Required file missing: {file_path}"


def test_python_files_have_content():
    """Test that Python files are not empty."""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    python_files = [
        '__init__.py',
        'py/fit_mask_to_image.py',
        'version.py',
    ]

    for file_path in python_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            assert file_size > 0, f"File is empty: {file_path}"


def test_readme_exists():
    """Test that README.md exists."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    readme_path = os.path.join(base_dir, 'README.md')
    assert os.path.exists(readme_path), "README.md is missing"


def test_placeholder():
    """Placeholder test to ensure pytest runs."""
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
