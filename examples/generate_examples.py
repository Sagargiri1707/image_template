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
    """Generate a business template post."""
    # Get the template registry
    registry = get_template_registry()

    # Template data mapping
    if templateName == "calendar_app_promo":
        template_data = {
            "cta_text": "LEARN MORE",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "image_url": "https://www.calendar.com/wp-content/uploads/2019/09/CalendarAndroidApp.png.webp",
            "cta_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
            "heading": "plan your day in a snap",
            "subheading": "Driving your success forward",
            "contact_email": "contact@business.com",
            "contact_phone": "+1-800-555-1234",
            "website_url": "dolze.ai /download",
            "quote": "The only way to do great work is to love what you do.",
            "theme_color": "#d4ffdd",
            "user_avatar": "https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "user_name": "Alex Johnson",
            "user_title": "Marketing Director, TechCorp",
            "testimonial_text": "This product has completely transformed how our team works. The intuitive interface and powerful features have saved us countless hours of work. Highly recommended!",
        }
    elif templateName == "testimonials_template":
        template_data = {
            # Common fields
            "theme_color": "#44ec9d",
            "website_url": "dolze.ai/download",
            # Testimonials specific
            "user_avatar": "https://img.freepik.com/free-vector/isolated-young-handsome-man-different-poses-white-background-illustration_632498-859.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "user_name": "Sarah Johnson",
            "user_title": "Verified Buyer",
            "testimonial_text": "This product was absolutely amazing! The quality exceeded my expectations and the customer service was outstanding. I've already recommended it to all my friends.",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
        }
    elif templateName == "blog_post":
        template_data = {
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
            "title": "How to be environment conscious without being weird",
            "author": "@username",
            "read_time": "4",
            "image_url": "https://img.freepik.com/free-vector/underwater-ocean-reef-coral-background_107791-1853.jpg",
            "logo_url": "https://img.freepik.com/free-vector/gradient-s-letter-logo_343694-1365.jpg",
        }

    # Render the template with the data
    output_path = os.path.join("output", f"{templateName}.png")
    rendered_image = registry.render_template(
        templateName,
        template_data,
        output_path=output_path,
    )

    print(f"Template saved to {os.path.abspath(output_path)}")
    return rendered_image


def main():
    """Generate all example templates."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Generate all templates
        templates = [
            # "calendar_app_promo",
            # "testimonials_template",
            "blog_post",
        ]
        for template in templates:
            generate_business_template(template)

        print("\nAll examples generated successfully!")
    except Exception as e:
        print(f"\nError generating examples: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
