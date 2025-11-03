# Changelog

All notable changes to ComfyUI ImageMask Fix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2025-11-01

### Added
- Initial release of Fit Mask to Image node
- Automatic mask dimension fixing to match source images
- Multiple output formats:
  - Fixed mask (from alpha channel)
  - Preview image (RGB+alpha merged)
  - Info string (dimension details)
  - Intermediate mask (debug, from red channel)
  - Masked latent (for inpainting)
- Support for optional LATENT input/output
- Nearest-exact scaling for mask quality preservation
- Debug info output showing dimension changes
- Replaces 10-node workflow with single node

### Technical Details
- Implements red→alpha channel conversion pattern
- Uses PyTorch interpolate for GPU-accelerated scaling
- Maintains compatibility with ComfyUI's mask/image formats
- Includes auto-versioning via git hooks
