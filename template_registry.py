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
        """Load the default templates into the registry"""

        # Business template
        self.register_template(
            "business_template",
            {
                "name": "business_template",
                "description": "Professional business template with gradient background",
                "size": {"width": 1080, "height": 1080},
                "use_base_image": True,
                "components": [
                    {
                        "type": "image",
                        "image_url": "${logo_url}",
                        "position": {"x": 50, "y": 50},
                        "size": {"width": 120, "height": 120},
                        "circle_crop": True,
                    },
                    {
                        "type": "text",
                        "text": "${heading}",
                        "position": {"x": 140, "y": 280},
                        "font_size": 53,
                        "color": [255, 255, 255],
                        "max_width": 800,
                        "font_path": get_font_manager().get_font("Roboto.ttf"),
                    },
                    {
                        "type": "text",
                        "text": "${subheading}",
                        "position": {"x": 140, "y": 360},
                        "font_size": 32,
                        "color": [255, 255, 255],
                        "max_width": 800,
                        "font_path": get_font_manager().get_font(
                            "OpenSans-Regular.ttf", 32
                        ),
                    },
                    {
                        "type": "image",
                        "image_url": "${cta_image}",
                        "position": {"x": 100, "y": 600},
                        "size": {"width": 880, "height": 320},
                    },
                    {
                        "type": "text",
                        "text": "${contact_email}",
                        "position": {"x": 300, "y": 980},
                        "font_size": 32,
                        "color": [255, 255, 255],
                    },
                    {
                        "type": "text",
                        "text": "•",
                        "position": {"x": 600, "y": 980},
                        "font_size": 32,
                        "color": [255, 255, 255],
                    },
                    {
                        "type": "text",
                        "text": "${contact_phone}",
                        "position": {"x": 640, "y": 980},
                        "font_size": 32,
                        "color": [255, 255, 255],
                    },
                    {
                        "type": "text",
                        "text": "${website_url}",
                        "position": {"x": 460, "y": 1030},
                        "font_size": 32,
                        "color": [255, 255, 255],
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

    # Example user data for the business template
    user_data = {
        "image_url": "https://img.freepik.com/premium-vector/blurry-image-multicolored-gradient-background_502601-1346.jpg",
        "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
        "heading": "Grow Your Business Today",
        "subheading": "Custom solutions for modern challenges in the digital landscape",
        "cta_text": "GET STARTED",
        "cta_image": "https://dolze-templates-uat.s3.eu-north-1.amazonaws.com/36222581-2fba-4839-a1f1-0685615b10c4.png",
        "contact_email": "info@acmecorp.com",
        "contact_phone": "+1-800-555-1234",
        "website_url": "www.acmecorp.com",
    }

    # Render the business template
    output_path = registry.render_template("business_template", user_data)

    if output_path:
        print(f"\nGenerated business template image: {output_path}")
        print("Try opening the generated image to see the customized template!")
    else:
        print("Failed to generate template image.")
