# Dolze Templates

A powerful Python library for generating social media posts, banners, and other marketing materials using JSON templates.

## Features

- 🎨 Create beautiful, responsive templates with a simple JSON structure
- 🖼️ Support for images, text, buttons, and other UI elements
- 🎯 Pre-built templates for common use cases (social media posts, quotes, banners)
- 🚀 Easy to extend with custom components
- 🎨 Support for custom fonts and colors
- 📱 Responsive design that works across different aspect ratios

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Using Pre-built Templates

```python
from dolze_templates import get_template_registry

# Get the template registry
registry = get_template_registry()

# Render a template with your data
result = registry.render_template(
    "social_media_post",  # Template name
    {
        "logo_url": "https://example.com/logo.png",
        "image_url": "https://example.com/featured.jpg",
        "heading": "Amazing Product Launch",
        "subheading": "Check out our latest innovation!",
        "cta_text": "Learn More",
        "contact_email": "info@example.com",
        "contact_phone": "+1-800-555-1234",
        "website_url": "https://example.com"
    }
)

# Save the result
result.save("output/post.png")
```

### Available Templates

1. **Social Media Post** (`social_media_post.json`)
   - Perfect for sharing updates, announcements, and promotions
   - Includes logo, featured image, heading, subheading, and CTA button

2. **Quote Post** (`quote_post.json`)
   - Elegant design for sharing quotes and testimonials
   - Supports background images and custom styling

3. **Promotional Banner** (`promotional_banner.json`)
   - Eye-catching banner for promotions and announcements
   - Features gradient backgrounds and clear call-to-action

## Template Format

Templates are defined using a simple JSON structure. Here's an example:

```json
{
  "name": "social_media_post",
  "description": "A clean and modern social media post template",
  "size": {
    "width": 1080,
    "height": 1080
  },
  "background_color": [255, 255, 255, 255],
  "use_base_image": false,
  "components": [
    {
      "type": "rectangle",
      "position": {"x": 0, "y": 0},
      "size": {"width": 1080, "height": 1080},
      "fill_color": [245, 245, 245, 255]
    },
    {
      "type": "image",
      "image_url": "${logo_url}",
      "position": {"x": 40, "y": 40},
      "size": {"width": 100, "height": 100},
      "circle_crop": true
    },
    {
      "type": "text",
      "text": "${heading}",
      "position": {"x": 90, "y": 740},
      "font_size": 64,
      "color": [51, 51, 51, 255],
      "max_width": 900,
      "font_path": "Roboto-Bold"
    }
  ]
}
```

### Standard Template Variables

All templates support these standard variables that will be replaced with actual values:

- `logo_url`: URL to your logo/image
- `image_url`: URL to the main featured image
- `heading`: Main heading text
- `subheading`: Subheading text
- `cta_text`: Call-to-action button text
- `contact_email`: Contact email address
- `contact_phone`: Contact phone number
- `website_url`: Website URL for CTAs
- `quote`: For quote templates, the main quote text

## Examples

See the `examples/` directory for complete examples of how to use each template.

```bash
# Generate all example templates
python examples/generate_examples.py
```

## Customization

### Adding Custom Fonts

1. Place your font files in the `fonts/` directory
2. Reference them in your templates using the font name (without extension)

### Creating Custom Templates

1. Create a new JSON file in the `dolze_templates/templates/` directory
2. Define your template structure following the format shown above
3. Register your template in the `TemplateRegistry`

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Building the Package

```bash
python setup.py sdist bdist_wheel
```

## License

MIT
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
