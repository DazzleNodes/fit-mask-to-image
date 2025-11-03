"""
ComfyUI Fit Mask to Image - Custom Node
Automatically resizes masks to match image dimensions.
"""

from .py.fit_mask_to_image import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from .version import __version__

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Display version info on load
print(f"[FitMaskToImage] Loaded v{__version__}")
