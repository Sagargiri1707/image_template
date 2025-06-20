"""
Example script demonstrating how to use the Dolze Templates library.

This script shows how to:
1. Load templates from JSON files
2. Render templates with different data
3. Save the generated images
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import the package
import sys

sys.path.append(str(Path(__file__).parent.parent))

from dolze_templates import TemplateRegistry, get_template_registry, configure

# Configure the library
configure(
    templates_dir=os.path.join(
        os.path.dirname(__file__), "..", "dolze_templates", "templates"
    ),
    output_dir=os.path.join(os.path.dirname(__file__), "output"),
)


def generate_business_template(templateName: str):
    """Generate a post using the business_template template."""
    print("\nGenerating business template post...")

    # Get the template registry
    registry = get_template_registry()

    # Render the template with sample data
    output_path = os.path.join("output", "business_template_post.png")
    rendered_image = registry.render_template(
        templateName,
        {
            "cta_text": "LEARN MORE",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "image_url": "https://images.unsplash.com/photo-1551434678-e076c223a692",
            "cta_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
            "heading": "Business Solutions",
            "subheading": "Driving your success forward",
            "contact_email": "contact@business.com",
            "contact_phone": "+1-800-555-1234",
            "website_url": "www.business.com",
            "quote": "The only way to do great work is to love what you do.",
        },
        output_path=output_path,
    )

    print(f"Business template post saved to {os.path.abspath(output_path)}")
    return rendered_image


def main():
    """Generate all example templates."""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), "output"), exist_ok=True)

    try:
        generate_business_template("promotional_banner")
        generate_business_template("template69")

        print("\nAll examples generated successfully!")
    except Exception as e:
        print(f"\nError generating examples: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
