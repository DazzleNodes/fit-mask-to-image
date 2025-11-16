# Changelog

All notable changes to ComfyUI ImageMask Fix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2-alpha] - 2025-11-15

### Added
- `pass_through` option to `missing_mask` parameter
  - Preserves original behavior: process empty masks without checking
  - Useful for workflows that expect empty mask outputs

### Changed
- Updated `missing_mask` options order for better UX

## [0.2.1-alpha] - 2025-11-15

### Added
- `missing_mask` parameter to handle empty or missing mask inputs
  - `all_visible` (default): Generate white mask (1.0) - entire image visible
  - `all_hidden`: Generate black mask (0.0) - entire image masked
  - `error`: Fail with clear error message when mask is missing
- Empty mask detection to prevent crashes when no mask is provided
- Automatic mask generation that fits image dimensions

### Changed
- Node now gracefully handles workflows without mask input
- Default behavior: creates full-visible mask when no mask provided

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
