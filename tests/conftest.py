"""
Pytest configuration to prevent root module collection.

This prevents pytest from attempting to import the root __init__.py which
contains ComfyUI-specific relative imports that aren't needed for our tests.
"""

import sys
import os

# Add the parent directory to sys.path for any test imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Explicitly tell pytest to ignore these directories and files during collection
collect_ignore = [
    "__init__.py",
    "py",
    "web",
    "examples",
    "docs",
    "private",
    ".vscode",
    ".git",
    ".github",
    "scripts",
]
