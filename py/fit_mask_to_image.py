"""
Fit Mask to Image Node - Automatically resize masks to match image dimensions.

This node replicates the functionality of a 10-node workflow that:
1. Extracts dimensions from source image
2. Converts mask to image format
3. Scales mask to match source dimensions (nearest-exact)
4. Converts back to mask using red channel (intermediate)
5. Merges original RGB with scaled mask as alpha channel
6. Extracts alpha channel as final fitted mask
7. Optionally applies mask to latent for inpainting
"""

import torch
import torch.nn.functional as F
from typing import Tuple, Optional, Dict, Any


class FitMaskToImage:
    """
    Automatically resizes masks to match image dimensions.

    Combines mask scaling, channel conversion, and optional latent masking
    into a single node to simplify inpainting workflows.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # Source image for dimension reference
                "mask": ("MASK",),    # Mask to fix dimensions
            },
            "optional": {
                "latent": ("LATENT",),  # Optional latent for inpainting
            }
        }

    RETURN_TYPES = ("MASK", "IMAGE", "STRING", "LATENT")
    RETURN_NAMES = ("fixed_mask", "preview_image", "info", "masked_latent")
    FUNCTION = "fix_mask_dimensions"
    CATEGORY = "DazzleNodes"
    DESCRIPTION = "Fixes dimension mismatches between masks and images for inpainting workflows"

    def fix_mask_dimensions(
        self,
        image: torch.Tensor,
        mask: torch.Tensor,
        latent: Optional[Dict[str, Any]] = None
    ) -> Tuple[torch.Tensor, torch.Tensor, str, Optional[Dict[str, Any]]]:
        """
        Main processing function that replicates the 10-node workflow.

        Args:
            image: Source image [B, H, W, C] for dimension reference
            mask: Mask to fix [B, H, W] or [B, H, W, 1]
            latent: Optional latent dict with "samples" key

        Returns:
            fixed_mask: Final mask from alpha channel [B, H, W]
            preview_image: RGB+alpha merged image [B, H, W, 4]
            info: Dimension and processing information
            masked_latent: Latent with mask applied (or None)
        """

        # Step 1: Extract dimensions from source image (ImpactImageInfo equivalent)
        target_height, target_width = self._extract_dimensions(image)
        original_height, original_width = self._get_mask_dimensions(mask)

        # Step 2: Convert mask to image format (MaskToImage equivalent)
        mask_as_image = self._mask_to_image(mask)

        # Step 3: Scale mask-image to match source dimensions (ImageScale equivalent)
        scaled_mask_image = self._scale_image(
            mask_as_image,
            target_width,
            target_height,
            method="nearest-exact"
        )

        # Step 4: Convert scaled image to mask using red channel (ImageToMask with red)
        intermediate_mask = self._image_to_mask(scaled_mask_image, channel="red")

        # Step 5: Merge original RGB + scaled mask as alpha (MergeImageChannels)
        preview_image = self._merge_channels(image, intermediate_mask)

        # Step 6: Extract alpha channel as final mask (ImageToMask with alpha)
        fixed_mask = self._image_to_mask(preview_image, channel="alpha")

        # Step 7: Apply mask to latent if provided (SetLatentNoiseMask equivalent)
        masked_latent = None
        if latent is not None:
            masked_latent = self._apply_mask_to_latent(latent, fixed_mask)

        # Generate info string
        info = self._generate_info(
            original_width, original_height,
            target_width, target_height,
            has_latent=latent is not None
        )

        return (fixed_mask, preview_image, info, masked_latent)

    def _extract_dimensions(self, image: torch.Tensor) -> Tuple[int, int]:
        """Extract height and width from image tensor (ImpactImageInfo equivalent)."""
        if len(image.shape) != 4:
            raise ValueError(f"Expected 4D image tensor [B,H,W,C], got shape {image.shape}")

        batch, height, width, channels = image.shape
        return height, width

    def _get_mask_dimensions(self, mask: torch.Tensor) -> Tuple[int, int]:
        """Get current mask dimensions."""
        if len(mask.shape) == 4:
            # [B, H, W, 1]
            return mask.shape[1], mask.shape[2]
        elif len(mask.shape) == 3:
            # [B, H, W]
            return mask.shape[1], mask.shape[2]
        elif len(mask.shape) == 2:
            # [H, W]
            return mask.shape[0], mask.shape[1]
        else:
            raise ValueError(f"Unexpected mask shape: {mask.shape}")

    def _mask_to_image(self, mask: torch.Tensor) -> torch.Tensor:
        """
        Convert mask to image format (MaskToImage equivalent).

        Mask: [B, H, W] -> Image: [B, H, W, 1] (grayscale)
        """
        if len(mask.shape) == 2:
            # [H, W] -> [1, H, W, 1]
            mask = mask.unsqueeze(0).unsqueeze(-1)
        elif len(mask.shape) == 3:
            # [B, H, W] -> [B, H, W, 1]
            mask = mask.unsqueeze(-1)
        elif len(mask.shape) == 4:
            # Already [B, H, W, 1]
            pass
        else:
            raise ValueError(f"Unexpected mask shape: {mask.shape}")

        # Ensure values in [0, 1] range
        mask = torch.clamp(mask, 0.0, 1.0)

        return mask

    def _scale_image(
        self,
        image: torch.Tensor,
        target_width: int,
        target_height: int,
        method: str = "nearest-exact"
    ) -> torch.Tensor:
        """
        Scale image to target dimensions (ImageScale equivalent).

        Args:
            image: [B, H, W, C]
            target_width: Target width
            target_height: Target height
            method: Interpolation method
        """
        batch, current_height, current_width, channels = image.shape

        # Check if scaling needed
        if current_height == target_height and current_width == target_width:
            return image

        # PyTorch interpolate expects [B, C, H, W]
        image = image.permute(0, 3, 1, 2)

        # Scale
        scaled = F.interpolate(
            image,
            size=(target_height, target_width),
            mode="nearest-exact" if method == "nearest-exact" else method,
            align_corners=None if method == "nearest-exact" else False
        )

        # Convert back to [B, H, W, C]
        scaled = scaled.permute(0, 2, 3, 1)

        return scaled

    def _image_to_mask(self, image: torch.Tensor, channel: str = "red") -> torch.Tensor:
        """
        Convert image to mask using specified channel (ImageToMask equivalent).

        Args:
            image: [B, H, W, C]
            channel: "red", "green", "blue", or "alpha"
        """
        channel_map = {
            "red": 0,
            "green": 1,
            "blue": 2,
            "alpha": 3
        }

        if channel not in channel_map:
            raise ValueError(f"Invalid channel: {channel}. Must be one of {list(channel_map.keys())}")

        channel_idx = channel_map[channel]

        # Handle grayscale images (only 1 channel)
        if image.shape[3] == 1:
            mask = image[:, :, :, 0]
        elif image.shape[3] > channel_idx:
            mask = image[:, :, :, channel_idx]
        else:
            raise ValueError(f"Image has {image.shape[3]} channels, cannot extract {channel} (index {channel_idx})")

        # Ensure values in [0, 1] range
        mask = torch.clamp(mask, 0.0, 1.0)

        return mask

    def _merge_channels(self, image: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """
        Merge RGB from image with mask as alpha channel (MergeImageChannels equivalent).

        Args:
            image: Source RGB image [B, H, W, C]
            mask: Mask to use as alpha [B, H, W]

        Returns:
            RGBA image [B, H, W, 4]
        """
        batch, height, width, channels = image.shape

        # Ensure mask matches image dimensions
        if mask.shape[1:] != (height, width):
            raise ValueError(f"Mask dimensions {mask.shape[1:]} don't match image {(height, width)}")

        # Expand mask to [B, H, W, 1]
        mask_expanded = mask.unsqueeze(-1)

        if channels == 3:
            # RGB image - add alpha channel
            rgba = torch.cat([image, mask_expanded], dim=-1)
        elif channels == 4:
            # Already RGBA - replace alpha with mask
            rgba = torch.cat([image[:, :, :, :3], mask_expanded], dim=-1)
        else:
            # Grayscale or other format - replicate to RGB and add alpha
            rgb = image.repeat(1, 1, 1, 3)[:, :, :, :3]  # Ensure exactly 3 channels
            rgba = torch.cat([rgb, mask_expanded], dim=-1)

        return rgba

    def _apply_mask_to_latent(
        self,
        latent: Dict[str, Any],
        mask: torch.Tensor
    ) -> Dict[str, Any]:
        """
        Apply mask to latent for inpainting (SetLatentNoiseMask equivalent).

        Args:
            latent: Dict with "samples" key [B, C, H_latent, W_latent]
            mask: Mask to apply [B, H, W]

        Returns:
            New latent dict with "noise_mask" added
        """
        if "samples" not in latent:
            raise ValueError("Invalid latent format: missing 'samples' key")

        samples = latent["samples"]

        # Latent dimensions are typically 1/8 of image dimensions (VAE downscale)
        latent_height = samples.shape[2]
        latent_width = samples.shape[3]

        # Scale mask to latent dimensions
        mask_for_latent = self._scale_mask_for_latent(mask, latent_height, latent_width)

        # Create new latent dict with mask applied
        masked_latent = latent.copy()
        masked_latent["noise_mask"] = mask_for_latent

        return masked_latent

    def _scale_mask_for_latent(
        self,
        mask: torch.Tensor,
        target_height: int,
        target_width: int
    ) -> torch.Tensor:
        """Scale mask to latent dimensions."""
        current_height, current_width = mask.shape[1], mask.shape[2]

        if current_height == target_height and current_width == target_width:
            return mask

        # PyTorch interpolate expects [B, C, H, W]
        mask_4d = mask.unsqueeze(1)  # Add channel dimension

        scaled = F.interpolate(
            mask_4d,
            size=(target_height, target_width),
            mode="nearest-exact"
        )

        # Remove channel dimension
        scaled = scaled.squeeze(1)

        return scaled

    def _generate_info(
        self,
        original_width: int,
        original_height: int,
        target_width: int,
        target_height: int,
        has_latent: bool = False
    ) -> str:
        """Generate informative string about dimension fix."""
        scale_w = target_width / original_width if original_width > 0 else 1.0
        scale_h = target_height / original_height if original_height > 0 else 1.0

        info_lines = [
            "== Fit Mask to Image ==",
            f"Mask:  {original_width}×{original_height}",
            f"Image: {target_width}×{target_height}",
            f"Scale: {scale_w:.2f}x × {scale_h:.2f}x",
        ]

        if original_height == target_height and original_width == target_width:
            info_lines.append("Status: No scaling needed")
        else:
            info_lines.append("Status: Scaled successfully")

        if has_latent:
            info_lines.append("Latent: Mask applied")

        return "\n".join(info_lines)


# Node registration
NODE_CLASS_MAPPINGS = {
    "FitMaskToImage": FitMaskToImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FitMaskToImage": "Fit Mask to Image",
}
