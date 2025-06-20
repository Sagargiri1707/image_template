# Dolze Templates

A powerful Python library for generating beautiful, dynamic images using JSON templates. Perfect for creating social media posts, marketing materials, product showcases, and more.

## ✨ Features

- 🎨 **Template Engine**: Create complex image compositions using a simple JSON structure
- 🖼️ **Rich Component Library**: Text, images, shapes, and more with extensive styling options
- ⚡ **Performance**: Built-in caching for fonts and images to speed up generation
- 📦 **Extensible**: Easy to extend with custom components and templates
- 🎯 **Production Ready**: Comprehensive validation and error handling

## 📦 Installation

Install the package using pip:

```bash
pip install dolze-templates
```

For development, you can install from source:

```bash
git clone https://github.com/yourusername/dolze-templates.git
cd dolze-templates
pip install -e .
```

## 🚀 Quick Start

### 1. Using Python API

```python
from dolze_templates import TemplateEngine

# Initialize the template engine
engine = TemplateEngine(output_dir="output")

# Process a template file
results = engine.process_from_file("templates/social_media_post.json")

# Process multiple templates from a directory
# results = engine.process_from_file("templates/")

print(f"Generated: {results}")
```

### 2. Using the Command Line

```bash
# Process a single template
dolze-templates render templates/social_media_post.json -o output

# Process all templates in a directory
dolze-templates render templates/ -o output

# Clear the cache
dolze-templates cache clear

# Show cache info
dolze-templates cache info
```

## 📋 Example Templates

Check out the [examples](examples/) directory for ready-to-use templates:

1. **Social Media Post** - Create engaging social media posts with images and text overlays
2. **Quote Image** - Generate beautiful quote images with custom styling
3. **Product Showcase** - Showcase products with images, descriptions, and pricing

## 🛠️ Template Structure

Templates are defined using JSON and can include various components:

```json
{
  "template_name": {
    "size": [1200, 1200],
    "background_color": [255, 255, 255],
    "use_base_image": false,
    "components": [
      {
        "type": "text",
        "text": "Hello, World!",
        "position": [100, 100],
        "font_size": 48,
        "color": [0, 0, 0]
      },
      {
        "type": "image",
        "image_url": "https://example.com/image.jpg",
        "position": [200, 200],
        "size": [400, 300]
      }
    ]
  }
}
```

## 📚 Documentation

### Available Components

#### Text

Display text with various styling options.

```json
{
  "type": "text",
  "text": "Hello, World!",
  "position": [100, 100],
  "font_size": 36,
  "font_weight": "bold",
  "color": [0, 0, 0],
  "max_width": 800,
  "align": "center",
  "line_height": 1.5
}
```

#### Image

Display images from URLs or local files.

```json
{
  "type": "image",
  "image_url": "https://example.com/image.jpg",
  "position": [100, 100],
  "size": [400, 300],
  "border_radius": 10,
  "opacity": 0.9
}
```

#### Rectangle

Draw rectangles with customizable styles.

```json
{
  "type": "rectangle",
  "position": [50, 50],
  "size": [200, 100],
  "color": [255, 0, 0, 128],
  "border_radius": 10,
  "border_width": 2,
  "border_color": [0, 0, 0]
}
```

### Effects

Apply various visual effects to components:

```json
{
  "effects": ["shadow", "blur"],
  "shadow_color": [0, 0, 0, 100],
  "shadow_offset": [5, 5],
  "shadow_blur_radius": 10,
  "blur_radius": 5
}
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

````

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
````

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

````

## JSON Schema

The input JSON must contain at least an `image_url` field:

```json
{
  "image_url": "https://example.com/image.jpg"
}
````

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
