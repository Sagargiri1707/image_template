"""
Template Registry - Single source of truth for all template definitions and logic
"""

from typing import Dict, Any, Optional, List
import os
import json
import re
from pathlib import Path
from PIL import Image

from dolze_image_templates.core.template_engine import Template
from dolze_image_templates.core.font_manager import get_font_manager


class TemplateRegistry:
    """
    Registry for managing and accessing all available templates.
    Acts as a single point of contact for template-related operations.
    """

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the template registry.

        Args:
            templates_dir: Directory containing template definition files
        """
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
        )
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all templates from the templates directory."""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            return

        # Load all JSON files in the templates directory
        for file_path in Path(self.templates_dir).glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    template_data = json.load(f)
                    if isinstance(template_data, dict) and "name" in template_data:
                        self.templates[template_data["name"]] = template_data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading template from {file_path}: {e}")

    def _has_image_upload(self, config: Any) -> bool:
        """Check if the template configuration contains any image upload fields.

        Args:
            config: Template configuration or part of it

        Returns:
            bool: True if any field value is "${image_url}", False otherwise
        """
        if isinstance(config, str):
            return config == "${image_url}"

        if not isinstance(config, (dict, list)):
            return False

        if isinstance(config, dict):
            for value in config.values():
                if value == "${image_url}":
                    return True
                if isinstance(value, (dict, list)) and self._has_image_upload(value):
                    return True
        elif isinstance(config, list):
            for item in config:
                if item == "${image_url}":
                    return True
                if isinstance(item, (dict, list)) and self._has_image_upload(item):
                    return True

        return False

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """
        Get information about all available templates.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing template information with keys:
                - template_name: str - Name of the template
                - isImageUploadPresent: bool - True if template contains any image upload fields
                - sample_url: str - Placeholder for future sample URL (currently empty string)
        """
        result = []
        for name, config in self.templates.items():
            result.append(
                {
                    "template_name": name,
                    "isImageUploadPresent": self._has_image_upload(config),
                    "sample_url": "",  # Empty for now as per requirements
                }
            )
        return result

    def register_template(self, name: str, config: Dict[str, Any]) -> None:
        """
        Register a new template.

        Args:
            name: Name of the template
            config: Template configuration dictionary
        """
        if not name:
            raise ValueError("Template name cannot be empty")

        # Ensure required fields are present
        required_fields = ["components"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Template config is missing required field: {field}")

        # Set default values
        config.setdefault("name", name)
        config.setdefault("size", {"width": 1080, "height": 1080})
        config.setdefault("background_color", [255, 255, 255])
        config.setdefault("use_base_image", False)

        self.templates[name] = config

        # Save to file
        self._save_template(name, config)

    def _save_template(self, name: str, config: Dict[str, Any]) -> None:
        """
        Save a template to a JSON file.

        Args:
            name: Name of the template
            config: Template configuration
        """
        try:
            os.makedirs(self.templates_dir, exist_ok=True)
            file_path = os.path.join(self.templates_dir, f"{name}.json")
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving template {name}: {e}")

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a template configuration by name.

        Args:
            name: Name of the template

        Returns:
            Template configuration dictionary or None if not found
        """
        return self.templates.get(name)

    def get_template_names(self) -> List[str]:
        """
        Get a list of all available template names.

        Returns:
            List of template names
        """
        return list(self.templates.keys())

    def create_template_instance(
        self, name: str, variables: Optional[Dict[str, Any]] = None
    ) -> Optional[Template]:
        """
        Create a template instance with the given variables.

        Args:
            name: Name of the template
            variables: Dictionary of variables to substitute in the template

        Returns:
            A Template instance or None if the template is not found
        """
        template_config = self.get_template(name)
        if not template_config:
            return None

        # Create a deep copy of the config to avoid modifying the original
        config = json.loads(json.dumps(template_config))

        # Apply variable substitution if variables are provided
        if variables:
            config = self._substitute_variables(config, variables)

        return Template.from_config(config)

    def _substitute_variables(self, config: Any, variables: Dict[str, Any]) -> Any:
        """
        Recursively substitute variables in the template configuration.

        Args:
            config: Template configuration or part of it
            variables: Dictionary of variables to substitute

        Returns:
            Configuration with variables substituted
        """
        if isinstance(config, dict):
            result = {}
            for key, value in config.items():
                result[key] = self._substitute_variables(value, variables)
            return result
        elif isinstance(config, list):
            return [self._substitute_variables(item, variables) for item in config]
        elif isinstance(config, str):
            # Replace ${variable} with the corresponding value
            def replace_match(match):
                var_name = match.group(1)
                return str(variables.get(var_name, match.group(0)))

            return re.sub(r"\${([^}]+)}", replace_match, config)
        else:
            return config

    def render_template(
        self,
        template_name: str,
        variables: Dict[str, Any],
        output_path: Optional[str] = None,
    ) -> Optional[Image.Image]:
        """
        Render a template with the given variables.

        Args:
            template_name: Name of the template to render
            variables: Dictionary of variables to substitute in the template
            output_path: Optional path to save the rendered image

        Returns:
            Rendered PIL Image or None if rendering fails
        """
        template = self.create_template_instance(template_name, variables)
        if not template:
            return None

        # Render the template
        rendered_image = template.render()

        # Save to file if output path is provided
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            rendered_image.save(output_path)

        return rendered_image


# Singleton instance for easy access
_instance = None


def get_template_registry(templates_dir: Optional[str] = None) -> TemplateRegistry:
    """
    Get the singleton instance of the template registry.

    Args:
        templates_dir: Optional directory containing template definitions

    Returns:
        TemplateRegistry instance
    """
    global _instance
    if _instance is None:
        _instance = TemplateRegistry(templates_dir)
    return _instance
