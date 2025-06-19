#!/usr/bin/env python3
"""
Font Demo - Demonstrates the use of custom fonts in templates
"""
import os
import json
from template_registry import TemplateRegistry
from font_manager import get_font_manager


def main():
    """Main function to demonstrate custom fonts in templates"""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Get the font manager and list available fonts
    font_manager = get_font_manager()
    print("Available fonts:")
    for font_name in font_manager.list_fonts():
        print(f"- {font_name}")

    # Initialize the template registry
    registry = TemplateRegistry()

    # Create a template that showcases different fonts
    font_showcase_template = {
        "id": "font_showcase",
        "name": "Font Showcase Template",
        "description": "Template showcasing different custom fonts",
        "base_image": {
            "type": "solid_color",
            "width": 1080,
            "height": 1080,
            "color": [240, 240, 240],
        },
        "components": [
            {
                "type": "text",
                "text": "Custom Font Showcase",
                "position": {"x": 540, "y": 100},
                "font_size": 48,
                "color": [50, 50, 50],
                "align": "center",
                "font_path": "fonts/Montserrat-Bold.ttf",
            },
            {
                "type": "text",
                "text": "Roboto Regular",
                "position": {"x": 540, "y": 200},
                "font_size": 36,
                "color": [70, 70, 70],
                "align": "center",
                "font_path": "fonts/Roboto-Regular.ttf",
            },
            {
                "type": "text",
                "text": "This is text in Roboto Regular font",
                "position": {"x": 540, "y": 250},
                "font_size": 24,
                "color": [100, 100, 100],
                "align": "center",
                "font_path": "fonts/Roboto-Regular.ttf",
            },
            {
                "type": "text",
                "text": "Roboto Bold",
                "position": {"x": 540, "y": 320},
                "font_size": 36,
                "color": [70, 70, 70],
                "align": "center",
                "font_path": "fonts/Roboto-Bold.ttf",
            },
            {
                "type": "text",
                "text": "This is text in Roboto Bold font",
                "position": {"x": 540, "y": 370},
                "font_size": 24,
                "color": [100, 100, 100],
                "align": "center",
                "font_path": "fonts/Roboto-Bold.ttf",
            },
            {
                "type": "text",
                "text": "Montserrat Regular",
                "position": {"x": 540, "y": 440},
                "font_size": 36,
                "color": [70, 70, 70],
                "align": "center",
                "font_path": "fonts/Montserrat-Regular.ttf",
            },
            {
                "type": "text",
                "text": "This is text in Montserrat Regular font",
                "position": {"x": 540, "y": 490},
                "font_size": 24,
                "color": [100, 100, 100],
                "align": "center",
                "font_path": "fonts/Montserrat-Regular.ttf",
            },
            {
                "type": "text",
                "text": "Montserrat Bold",
                "position": {"x": 540, "y": 560},
                "font_size": 36,
                "color": [70, 70, 70],
                "align": "center",
                "font_path": "fonts/Montserrat-Bold.ttf",
            },
            {
                "type": "text",
                "text": "This is text in Montserrat Bold font",
                "position": {"x": 540, "y": 610},
                "font_size": 24,
                "color": [100, 100, 100],
                "align": "center",
                "font_path": "fonts/Montserrat-Bold.ttf",
            },
            {
                "type": "text",
                "text": "Open Sans Regular",
                "position": {"x": 540, "y": 680},
                "font_size": 36,
                "color": [70, 70, 70],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
            {
                "type": "text",
                "text": "This is text in Open Sans Regular font",
                "position": {"x": 540, "y": 730},
                "font_size": 24,
                "color": [100, 100, 100],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
            {
                "type": "cta_button",
                "text": "Roboto Bold Button",
                "position": {"x": 540, "y": 820},
                "size": {"width": 300, "height": 60},
                "bg_color": [0, 123, 255],
                "text_color": [255, 255, 255],
                "corner_radius": 10,
                "font_path": "fonts/Roboto-Bold.ttf",
                "url": "https://example.com",
            },
            {
                "type": "footer",
                "text": "Footer with Open Sans Regular",
                "position": {"x": 540, "y": 950},
                "font_size": 16,
                "color": [150, 150, 150],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
        ],
    }

    # Register the font showcase template
    registry.register_template(font_showcase_template)

    # Create a business card template with custom fonts
    business_card_template = {
        "id": "business_card",
        "name": "Business Card Template",
        "description": "Professional business card template with custom fonts",
        "base_image": {
            "type": "gradient",
            "width": 1080,
            "height": 1080,
            "start_color": [41, 128, 185],
            "end_color": [109, 213, 250],
            "direction": "diagonal",
        },
        "components": [
            {
                "type": "text",
                "text": "${company_name|ACME Corporation}",
                "position": {"x": 540, "y": 300},
                "font_size": 60,
                "color": [255, 255, 255],
                "align": "center",
                "font_path": "fonts/Montserrat-Bold.ttf",
            },
            {
                "type": "text",
                "text": "${name|John Doe}",
                "position": {"x": 540, "y": 400},
                "font_size": 36,
                "color": [255, 255, 255],
                "align": "center",
                "font_path": "fonts/Roboto-Regular.ttf",
            },
            {
                "type": "text",
                "text": "${position|Chief Executive Officer}",
                "position": {"x": 540, "y": 450},
                "font_size": 24,
                "color": [220, 220, 220],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
            {
                "type": "text",
                "text": "${email|contact@example.com}",
                "position": {"x": 540, "y": 550},
                "font_size": 20,
                "color": [255, 255, 255],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
            {
                "type": "text",
                "text": "${phone|+1 (555) 123-4567}",
                "position": {"x": 540, "y": 590},
                "font_size": 20,
                "color": [255, 255, 255],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
            {
                "type": "text",
                "text": "${website|www.example.com}",
                "position": {"x": 540, "y": 630},
                "font_size": 20,
                "color": [255, 255, 255],
                "align": "center",
                "font_path": "fonts/OpenSans-Regular.ttf",
            },
            {
                "type": "cta_button",
                "text": "Contact Me",
                "position": {"x": 390, "y": 720},
                "size": {"width": 300, "height": 60},
                "bg_color": [255, 255, 255],
                "text_color": [41, 128, 185],
                "corner_radius": 30,
                "font_path": "fonts/Roboto-Bold.ttf",
                "url": "${contact_url|https://example.com/contact}",
            },
            {
                "type": "footer",
                "text": "${tagline|Building the future, one pixel at a time}",
                "position": {"x": 540, "y": 850},
                "font_size": 18,
                "color": [220, 220, 220],
                "align": "center",
                "font_path": "fonts/Montserrat-Regular.ttf",
            },
        ],
    }

    # Register the business card template
    registry.register_template(business_card_template)

    # User data for the business card
    user_data = {
        "company_name": "Dolze Design Studio",
        "name": "Sarah Johnson",
        "position": "Creative Director",
        "email": "sarah@dolzedesign.com",
        "phone": "+1 (415) 555-9876",
        "website": "www.dolzedesign.com",
        "contact_url": "https://dolzedesign.com/contact",
        "tagline": "Transforming ideas into visual masterpieces",
    }

    # Render the font showcase template
    print("\nRendering font showcase template...")
    showcase_output = registry.render_template("font_showcase")
    print(f"Font showcase template saved to: {showcase_output}")

    # Render the business card template with user data
    print("\nRendering business card template with custom data...")
    business_output = registry.render_template("business_card", user_data)
    print(f"Business card template saved to: {business_output}")

    print("\nTry opening the generated images to see the custom fonts in action!")


if __name__ == "__main__":
    main()
