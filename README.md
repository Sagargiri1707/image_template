# Image Processor System

A Python system that processes JSON input to generate and store images using Pillow.

## Features

- Accepts JSON input with an image URL
- Generates two images:
  - One with the original image as background
  - One with the original image in a circular crop at the top left
- Stores generated images in the local filesystem
- Extensible design for adding more elements (text, CTA buttons, etc.)

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Using the demo script

```bash
# Run with default example
python demo.py

# Run with a JSON string
python demo.py --json '{"image_url": "https://example.com/image.jpg"}'

# Run with a JSON file
python demo.py --file sample.json

# Specify output directory
python demo.py --output my_images
```

### Using the ImageProcessor class

```python
from image_processor import ImageProcessor

# Initialize processor
processor = ImageProcessor(output_dir="my_images")

# Process JSON data
json_data = {
    "image_url": "https://example.com/image.jpg"
}
result = processor.process_json(json_data)

# Print paths to generated images
for key, path in result.items():
    print(f"{key}: {path}")
```

## JSON Schema

The input JSON must contain at least an `image_url` field:

```json
{
  "image_url": "https://example.com/image.jpg"
}
```

Additional fields can be added for future extensions:

```json
{
  "image_url": "https://example.com/image.jpg",
  "text": {
    "title": "My Title",
    "description": "Description text"
  },
  "cta": {
    "text": "Click Here",
    "url": "https://example.com"
  }
}
```

## Extending the System

The `ImageProcessor` class is designed to be easily extended. To add new features:

1. Add new methods to the `ImageProcessor` class
2. Update the `process_json` method to use these new features

See the `extensions.py` file for examples of adding text and CTA buttons.
