"""
Template engine for rendering templates with components.
"""
import os
import json
import requests
from io import BytesIO
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image

from dolze_templates.components import create_component_from_config, Component


class Template:
    """
    A template that can be composed of multiple components.
    """

    def __init__(
        self,
        name: str,
        size: Tuple[int, int] = (800, 600),
        background_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        """
        Initialize a template.

        Args:
            name: Template name
            size: Size (width, height) of the template
            background_color: RGB color tuple for the background
        """
        self.name = name
        self.size = size
        self.background_color = background_color
        self.components: List[Component] = []

    def add_component(self, component: Component) -> None:
        """
        Add a component to the template.

        Args:
            component: Component to add
        """
        self.components.append(component)

    def render(self, base_image: Optional[Image.Image] = None) -> Image.Image:
        """
        Render the template with all its components.

        Args:
            base_image: Optional base image to use instead of creating a new one

        Returns:
            Rendered image
        """
        # Create a new image if no base image is provided
        if base_image is None:
            result = Image.new("RGBA", self.size, self.background_color)
        else:
            # Resize the base image if needed
            if base_image.size != self.size:
                base_image = base_image.resize(self.size, Image.Resampling.LANCZOS)

            # Convert to RGBA if needed
            if base_image.mode != "RGBA":
                result = base_image.convert("RGBA")
            else:
                result = base_image.copy()

        # Render each component
        for component in self.components:
            result = component.render(result)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'Template':
        """
        Create a template from a configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            A new template instance
        """
        name = config.get("name", "unnamed")

        size = (
            config.get("size", {}).get("width", 800),
            config.get("size", {}).get("height", 600),
        )

        background_color = tuple(config.get("background_color", (255, 255, 255)))

        template = cls(name=name, size=size, background_color=background_color)

        # Add components
        for component_config in config.get("components", []):
            component = create_component_from_config(component_config)
            if component:
                template.add_component(component)

        return template


class TemplateEngine:
    """
    Engine for processing templates and generating images.
    """

    def __init__(self, output_dir: str = "output"):
        """
        Initialize the template engine.

        Args:
            output_dir: Directory to store generated images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.templates: Dict[str, Template] = {}

    def add_template(self, template: Template) -> None:
        """
        Add a template to the engine.

        Args:
            template: Template to add
        """
        self.templates[template.name] = template

    def download_image(self, url: str) -> Optional[Image.Image]:
        """
        Download an image from a URL.

        Args:
            url: URL of the image to download

        Returns:
            PIL Image object or None if download fails
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except (requests.RequestException, IOError) as e:
            print(f"Failed to download image from {url}: {e}")
            return None

    def process_json(self, json_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Process JSON input to generate images.

        Args:
            json_data: JSON data containing template configurations

        Returns:
            Dictionary with paths to generated images
        """
        result = {}

        # Validate input
        if "image_url" not in json_data:
            raise ValueError("JSON input must contain 'image_url' field")

        # Download the base image
        base_image = self.download_image(json_data["image_url"])
        if base_image is None:
            raise ValueError(f"Failed to download image from {json_data['image_url']}")

        # Process each template
        for template_config in json_data.get("templates", []):
            template_name = template_config.get("name")
            if not template_name:
                continue

            # Create template from config
            template = Template.from_config(template_config)


            # Render the template
            rendered_image = template.render(
                base_image.copy()
                if template_config.get("use_base_image", False)
                else None
            )

            # Save the rendered image
            output_path = os.path.join(self.output_dir, f"{template_name}.png")
            rendered_image.save(output_path)

            # Add to result
            result[template_name] = output_path

        return result

    def process_from_file(self, json_file: str) -> Dict[str, str]:
        """
        Process JSON from a file.

        Args:
            json_file: Path to JSON file

        Returns:
            Dictionary with paths to generated images
        """
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
            return self.process_json(json_data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file {json_file}: {e}")
            return {}

    def clear_templates(self) -> None:
        """Clear all registered templates."""
        self.templates.clear()
