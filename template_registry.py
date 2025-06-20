"""
Template Registry - Single source of truth for all template definitions and logic
"""

from typing import Dict, Any, List, Optional, Union
import json
import os
import re
from template_engine import TemplateEngine, Template
from font_manager import get_font_manager


class TemplateRegistry:
    """
    Registry for managing and accessing all available templates.
    Acts as a single point of contact for template-related operations.
    """

    def __init__(self):
        """Initialize the template registry"""
        self.templates: Dict[str, Dict[str, Any]] = {}
        self._load_default_templates()

    def _load_default_templates(self) -> None:
        """Register default templates."""
        # Register clean_minimal template
        self.register_template(
            "clean_minimal",
            {
                "name": "clean_minimal",
                "description": "Clean minimal business template with central alignment and creative design elements",
                "size": {"width": 1080, "height": 1080},
                "use_base_image": False,
                "components": [
                    # Background
                    {
                        "type": "rectangle",
                        "position": {"x": 0, "y": 0},
                        "size": {"width": 1080, "height": 1080},
                        "fill_color": [255, 255, 255],
                        "outline_color": None,
                    },
                    # Top right purple circle (centered)
                    {
                        "type": "circle",
                        "position": {"x": 1100, "y": -200},
                        "radius": 400,
                        "fill_color": [239, 230, 250],
                        "outline_color": [255, 255, 255],
                        "outline_width": 2,
                    },
                    # Bottom left pink circle
                    {
                        "type": "circle",
                        "position": {"x": 50, "y": 1080},
                        "radius": 350,
                        "fill_color": [255, 230, 240],
                        "outline_color": [255, 255, 255],
                        "outline_width": 2,
                    },
                    # Logo (top left)
                    {
                        "type": "image",
                        "image_url": "${logo_url}",
                        "position": {"x": 80, "y": 60},
                        "size": {"width": 100, "height": 100},
                    },
                    # Main heading (centered)
                    {
                        "type": "text",
                        "text": "${heading}",
                        "position": {"x": 240, "y": 120},
                        "font_size": 72,
                        "color": [50, 50, 50],
                        "font_path": get_font_manager().get_font_path("Roboto-Bold"),
                        "alignment": "center",
                        "max_width": 600,
                    },
                    # Subheading (centered)
                    {
                        "type": "text",
                        "text": "${subheading}",
                        "position": {"x": 140, "y": 290},
                        "font_size": 32,
                        "color": [100, 100, 100],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                        "alignment": "center",
                        "max_width": 800,
                    },
                    # Main image (centered)
                    {
                        "type": "image",
                        "image_url": "${image_url}",
                        "position": {"x": 290, "y": 400},
                        "size": {"width": 500, "height": 500},
                        "circle_crop": True,
                    },
                    # Divider dots
                    {
                        "type": "circle",
                        "position": {"x": 480, "y": 940},
                        "radius": 10,
                        "fill_color": [128, 0, 128],
                        "outline_color": [255, 255, 255],
                        "outline_width": 2,
                    },
                    {
                        "type": "circle",
                        "position": {"x": 520, "y": 940},
                        "radius": 10,
                        "fill_color": [255, 100, 150],
                        "outline_color": [255, 255, 255],
                        "outline_width": 2,
                    },
                    {
                        "type": "circle",
                        "position": {"x": 560, "y": 940},
                        "radius": 10,
                        "fill_color": [128, 0, 128],
                        "outline_color": [255, 255, 255],
                        "outline_width": 2,
                    },
                    # Contact info (centered)
                    {
                        "type": "text",
                        "text": "${contact_email}",
                        "position": {"x": 240, "y": 970},
                        "font_size": 28,
                        "color": [100, 100, 100],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                        "alignment": "center",
                    },
                    {
                        "type": "text",
                        "text": "${contact_phone}",
                        "position": {"x": 550, "y": 970},
                        "font_size": 28,
                        "color": [100, 100, 100],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                        "alignment": "center",
                    },
                    # Website (centered)
                    {
                        "type": "text",
                        "text": "${website_url}",
                        "position": {"x": 440, "y": 1020},
                        "font_size": 28,
                        "color": [128, 0, 128],
                        "font_path": get_font_manager().get_font_path("Roboto-Medium"),
                        "alignment": "center",
                    },
                ],
            },
        )

        # Template 69 - Split layout with text left, image right
        self.register_template(
            "template69",
            {
                "name": "template69",
                "description": "Split layout with text on left and image on right",
                "size": {"width": 1080, "height": 1080},
                "use_base_image": False,
                "components": [
                    # Left side - White background
                    {
                        "type": "rectangle",
                        "position": {"x": 0, "y": 0},
                        "size": {"width": 540, "height": 1080},
                        "fill_color": [255, 255, 255],
                        "outline_color": None,
                    },
                    # Right side - Image
                    {
                        "type": "image",
                        "image_url": "${image_url}",
                        "position": {"x": 540, "y": 0},
                        "size": {"width": 1080, "height": 1080},
                    },
                    # Logo
                    {
                        "type": "image",
                        "image_url": "${logo_url}",
                        "position": {"x": 50, "y": 50},
                        "size": {"width": 60, "height": 60},
                    },
                    # Main heading
                    {
                        "type": "text",
                        "text": "${heading}",
                        "position": {"x": 50, "y": 200},
                        "font_size": 56,
                        "color": [0, 0, 0],
                        "font_path": get_font_manager().get_font_path("Roboto-Bold"),
                        "max_width": 440,
                    },
                    # Subheading
                    {
                        "type": "text",
                        "text": "${subheading}",
                        "position": {"x": 50, "y": 350},
                        "font_size": 36,
                        "color": [90, 90, 90],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                        "max_width": 440,
                    },
                    # Divider line (thick purple line)
                    {
                        "type": "rectangle",
                        "position": {"x": 50, "y": 900},
                        "size": {"width": 450, "height": 8},
                        "fill_color": [128, 0, 128],  # Purple
                        "outline_color": None,
                    },
                    # Contact email
                    {
                        "type": "text",
                        "text": "${contact_email}",
                        "position": {"x": 50, "y": 940},
                        "font_size": 28,
                        "color": [100, 100, 100],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                    },
                    # Contact phone
                    {
                        "type": "text",
                        "text": "${contact_phone}",
                        "position": {"x": 50, "y": 980},
                        "font_size": 28,
                        "color": [100, 100, 100],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                    },
                    # Website URL
                    {
                        "type": "text",
                        "text": "${website_url}",
                        "position": {"x": 50, "y": 1020},
                        "font_size": 28,
                        "color": [128, 0, 128],  # Purple
                        "font_path": get_font_manager().get_font_path("Roboto-Medium"),
                    },
                ],
            },
        )

        # Green Fintech template
        self.register_template(
            "green_fintech",
            {
                "name": "green_fintech",
                "description": "Green fintech template with gradient background and modern typography",
                "size": {"width": 1080, "height": 1080},
                "use_base_image": False,
                "components": [
                    # Background image
                    {
                        "type": "image",
                        "image_url": "https://img.freepik.com/free-vector/abstract-green-background_698452-3092.jpg?t=st=1750341344~exp=1750344944~hmac=fb613d9b3d8c853e9ec583a665051fabcd7b538df96a17c20ba7a18ee4974568",
                        "position": {"x": 0, "y": 0},
                        "size": {"width": 1080, "height": 1080},
                        "tint_overlay": [
                            0,
                            0,
                            0,
                            30,
                        ],
                    },
                    {
                        "type": "image",
                        "image_url": "${logo_url}",
                        "position": {"x": 60, "y": 60},
                        "size": {"width": 60, "height": 60},
                        "circle_crop": True,
                    },
                    {
                        "type": "text",
                        "text": "${heading}",
                        "position": {"x": 100, "y": 300},
                        "font_size": 42,
                        "color": [255, 255, 255],
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                    },
                    {
                        "type": "text",
                        "text": "${subheading}",
                        "max_width": 880,
                        "position": {"x": 100, "y": 380},
                        "font_size": 100,
                        "color": [255, 255, 0],  # Yellow color
                        "line_height": 1.1,
                        "font_path": get_font_manager().get_font_path("Roboto-Bold"),
                    },
                    {
                        "type": "rectangle",
                        "position": {"x": 600, "y": 700},
                        "size": {"width": 80, "height": 80},
                        "color": [0, 80, 0],  # Dark green
                        "border_radius": 15,
                    },
                    {
                        "type": "circle",
                        "position": {"x": 720, "y": 700},
                        "size": 80,
                        "color": [255, 255, 0],  # Yellow
                    },
                    {
                        "type": "rectangle",
                        "position": {"x": 100, "y": 850},
                        "size": {"width": 350, "height": 100},
                        "color": [255, 255, 0],  # Yellow
                        "border_radius": 10,
                    },
                    {
                        "type": "cta_button",
                        "text": "${cta_text}",
                        "position": {"x": 275, "y": 885},
                        "font_size": 36,
                        "color": [0, 80, 0],  # Dark green
                        "font_path": get_font_manager().get_font_path("Roboto-Bold"),
                        "alignment": "center",
                    },
                    {
                        "type": "text",
                        "text": "${contact_email}",
                        "position": {"x": 600, "y": 880},
                        "font_size": 28,
                        "color": [255, 255, 255],  # White
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                    },
                    {
                        "type": "text",
                        "text": "${contact_phone}",
                        "position": {"x": 600, "y": 920},
                        "font_size": 28,
                        "color": [255, 255, 255],  # White
                        "font_path": get_font_manager().get_font_path("Roboto-Light"),
                    },
                ],
            },
        )

        # Business template
        self.register_template(
            "business_template",
            {
                "name": "business_template",
                "description": "Professional business template with gradient background",
                "size": {"width": 1080, "height": 1080},
                "use_base_image": False,
                "components": [
                    {
                        "type": "image",
                        "image_url": "${image_url}",
                        "position": {"x": 0, "y": 0},
                        "size": {"width": 1080, "height": 1080},
                        "tint_overlay": [
                            0,
                            0,
                            0,
                            80,
                        ],  # Semi-transparent black overlay (0,0,0,80)
                    },
                    {
                        "type": "image",
                        "image_url": "${logo_url}",
                        "position": {"x": 50, "y": 50},
                        "size": {"width": 80, "height": 80},
                        "circle_crop": True,
                    },
                    {
                        "type": "text",
                        "text": "${heading}",
                        "position": {"x": 100, "y": 180},
                        "font_size": 72,
                        "color": [255, 255, 255],
                        "max_width": 880,  # Full width of the template
                        "alignment": "center",  # Center align the heading
                        "font_path": get_font_manager().get_font_path(
                            "Roboto-ExtraBold"
                        ),
                    },
                    {
                        "type": "text",
                        "text": "${subheading}",
                        "position": {"x": 100, "y": 260},
                        "font_size": 32,
                        "color": [255, 255, 255],
                        "max_width": 880,  # Full width of the template
                        "alignment": "center",  # Center align the subheading
                        "font_path": get_font_manager().get_font_path("Roboto-Medium"),
                    },
                    {
                        "type": "image",
                        "image_url": "${cta_image}",
                        "position": {"x": 100, "y": 400},
                        "size": {"width": 880, "height": 520},
                    },
                    {
                        "type": "text",
                        "text": "${contact_email}",
                        "position": {"x": 300, "y": 980},
                        "font_size": 32,
                        "color": [255, 255, 255],
                        "alignment": "center",  # Center align contact info
                        "font_path": get_font_manager().get_font_path("Roboto-Medium"),
                    },
                    {
                        "type": "text",
                        "text": "${contact_phone}",
                        "position": {"x": 640, "y": 980},
                        "font_size": 32,
                        "color": [255, 255, 255],
                        "alignment": "center",  # Center align phone number
                        "font_path": get_font_manager().get_font_path("Roboto-Medium"),
                    },
                    {
                        "type": "text",
                        "text": "${website_url}",
                        "position": {
                            "x": 100,
                            "y": 1030,
                        },  # Adjusted x position for better centering
                        "font_size": 32,
                        "color": [166, 166, 166],
                        "max_width": 880,  # Full width for better centering
                        "alignment": "center",  # Center align website URL
                        "font_path": get_font_manager().get_font_path("Roboto-Medium"),
                    },
                ],
            },
        )

    def register_template(
        self, template_id: str, template_config: Dict[str, Any]
    ) -> None:
        """
        Register a new template or update an existing one

        Args:
            template_id: Unique identifier for the template
            template_config: Template configuration dictionary
        """
        self.templates[template_id] = template_config

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a template configuration by its ID

        Args:
            template_id: Unique identifier for the template

        Returns:
            Template configuration or None if not found
        """
        return self.templates.get(template_id)

    def list_templates(self) -> List[Dict[str, Any]]:
        """
        Get a list of all available templates with their metadata

        Returns:
            List of template metadata dictionaries
        """
        return [
            {
                "id": template_id,
                "name": config.get("name", template_id),
                "description": config.get("description", ""),
            }
            for template_id, config in self.templates.items()
        ]

    def process_dynamic_values(
        self, template_config: Dict[str, Any], user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a template configuration by replacing dynamic values with user-provided data

        Args:
            template_config: Template configuration dictionary
            user_data: User-provided data dictionary

        Returns:
            Processed template configuration
        """
        # Deep copy the template config to avoid modifying the original
        import copy

        processed_config = copy.deepcopy(template_config)

        # Process components recursively
        if "components" in processed_config:
            for component in processed_config["components"]:
                for key, value in component.items():
                    if (
                        isinstance(value, str)
                        and value.startswith("${")
                        and value.endswith("}")
                    ):
                        # Extract variable name and default value if present
                        var_parts = value[2:-1].split("|")
                        var_name = var_parts[0]
                        default_value = var_parts[1] if len(var_parts) > 1 else None

                        # Replace with user data or default value
                        component[key] = user_data.get(var_name, default_value)

        return processed_config

    def render_template(
        self, template_id: str, user_data: Dict[str, Any], output_dir: str = "output"
    ) -> Optional[str]:
        """
        Render a template with user-provided data

        Args:
            template_id: Unique identifier for the template
            user_data: User-provided data dictionary
            output_dir: Directory to store the generated image

        Returns:
            Path to the generated image or None if the template was not found
        """
        template_config = self.get_template(template_id)
        if not template_config:
            return None

        # Process dynamic values
        processed_config = self.process_dynamic_values(template_config, user_data)

        # Create template engine
        engine = TemplateEngine(output_dir=output_dir)

        # Prepare JSON data for the engine
        json_data = {
            "image_url": user_data.get("image_url", ""),
            "templates": [processed_config],
        }

        # Process the template
        result = engine.process_json(json_data)

        # Return the path to the generated image
        return result.get(template_id)

    def save_to_file(self, filepath: str) -> None:
        """
        Save the template registry to a JSON file

        Args:
            filepath: Path to the JSON file
        """
        with open(filepath, "w") as f:
            json.dump(self.templates, f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> "TemplateRegistry":
        """
        Load a template registry from a JSON file

        Args:
            filepath: Path to the JSON file

        Returns:
            New TemplateRegistry instance
        """
        registry = cls()

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                templates = json.load(f)

            for template_id, config in templates.items():
                registry.register_template(template_id, config)

        return registry


# Example usage
if __name__ == "__main__":
    # Create a registry
    registry = TemplateRegistry()

    # List available templates
    templates = registry.list_templates()
    print("Available templates:")
    for template in templates:
        print(f"- {template['name']}: {template['description']}")

    # Example user data for clean_minimal template

    user_data = {
        "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
        "image_url": "https://dolze-templates-uat.s3.eu-north-1.amazonaws.com/3188fb75-00e1-4633-bc1b-55ba41346147.png",
        "heading": "Grow Your Business Today",
        "subheading": "Custom solutions for modern challenges in the digital landscape",
        "cta_text": "GET STARTED",
        "cta_image": "https://static.vecteezy.com/system/resources/thumbnails/035/576/450/small/ai-generated-3d-rendering-of-a-beautiful-colorful-candle-on-transparent-background-ai-generated-png.png",
        "contact_email": "info@rrefyne.com",
        "contact_phone": "+1-800-555-1234",
        "website_url": "www.business.com",
    }

    # Render the clean_minimal template
    output_path = registry.render_template("clean_minimal", user_data)

    if output_path:
        print(f"\nGenerated clean minimal template image: {output_path}")
        print("Try opening the generated image to see the customized template!")
    else:
        print("Failed to generate template image.")
