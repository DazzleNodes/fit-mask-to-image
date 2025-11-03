# ComfyUI Fit Mask to Image

$badges

Automatically resizes masks to match image dimensions for seamless inpainting workflows.

## Overview

This node replaces a 10-node workflow chain with a single, efficient node that automatically scales masks to match image dimensions. Perfect for inpainting workflows where masks and images come from different sources.

## Features

- **One-Node Solution**: Replaces 10-node workflow with single node
- **Smart Dimension Matching**: Automatically scales masks to match image dimensions
- **Multiple Outputs**: Fixed mask, preview image, debug mask, and masked latent
- **Inpainting Ready**: Direct integration with KSampler via latent output
- **Debug Information**: Detailed info output showing dimension changes

## Installation

### Method 1: Symlink (Recommended for Development)
```bash
cd C:\code\ComfyUI_experiment\custom_nodes
mklink /D imagemask-fix C:\code\ComfyUI-ImageMask-Fix\local
```

### Method 2: Direct Copy
```bash
cd C:\code\ComfyUI_experiment\custom_nodes
cp -r C:\code\ComfyUI-ImageMask-Fix\local imagemask-fix
```

Then restart ComfyUI.

## Usage

1. Add "Fit Mask to Image" node to your workflow (found under "DazzleNodes")
2. Connect your source IMAGE (for dimension reference)
3. Connect your MASK (to fix dimensions)
4. Optionally connect a LATENT for inpainting workflows

### Outputs

- **fixed_mask**: Final mask with corrected dimensions (from alpha channel)
- **preview_image**: RGB+alpha merged image for visual verification
- **info**: Text showing original→target dimensions and processing status
- **masked_latent**: Latent with mask applied (if latent input provided)

### Example Workflow

See `examples/` folder for workflow JSON files demonstrating the node in action

## Development

### Prerequisites

- List prerequisites here

### Setup

```bash
# Setup instructions here
```

## Contributions
Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to contribute.

Like the project?

[!["Buy Me A Coffee"](https://camo.githubusercontent.com/0b448aabee402aaf7b3b256ae471e7dc66bcf174fad7d6bb52b27138b2364e47/68747470733a2f2f7777772e6275796d6561636f666665652e636f6d2f6173736574732f696d672f637573746f6d5f696d616765732f6f72616e67655f696d672e706e67)](https://www.buymeacoffee.com/djdarcy)

## License

This project is licensed under the terms specified in the LICENSE file.

## Acknowledgements

Dustin 6962246+djdarcy@users.noreply.github.com
