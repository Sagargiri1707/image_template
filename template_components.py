from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Tuple, Optional, List, Union
import os
import requests
from io import BytesIO
from font_manager import get_font_manager


class Component:
    """Base class for all template components"""

    def __init__(self, position: Tuple[int, int] = (0, 0)):
        """
        Initialize a component.

        Args:
            position: Position (x, y) of the component on the template
        """
        self.position = position

    def render(self, image: Image.Image) -> Image.Image:
        """
        Render the component onto an image.

        Args:
            image: The image to render the component on

        Returns:
            The image with the component rendered on it
        """
        # Base implementation does nothing
        return image

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "Component":
        """
        Create a component from a configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            A new component instance
        """
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )
        return cls(position=position)


class TextComponent(Component):
    """Component for rendering text"""

    def __init__(
        self,
        text: str,
        position: Tuple[int, int] = (0, 0),
        font_size: int = 24,
        color: Tuple[int, int, int] = (0, 0, 0),
        max_width: Optional[int] = None,
        font_path: Optional[str] = None,
    ):
        """
        Initialize a text component.

        Args:
            text: Text to render
            position: Position (x, y) to place the text
            font_size: Font size
            color: RGB color tuple
            max_width: Maximum width for text wrapping
            font_path: Path to a TTF font file
        """
        super().__init__(position)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.max_width = max_width
        self.font_path = font_path

    def render(self, image: Image.Image) -> Image.Image:
        """Render text onto an image"""
        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Use font manager to get the font
        font_manager = get_font_manager()
        
        # If font_path is a font object, use it directly and get its size
        if hasattr(self.font_path, "getsize"):  # Check if it's a font object
            font = self.font_path
            # If the font has a size attribute, use it
            if hasattr(font, 'size') and font.size:
                self.font_size = font.size
        # If it's a string path that exists, try to load it
        elif isinstance(self.font_path, str) and os.path.exists(self.font_path):
            try:
                font = ImageFont.truetype(self.font_path, self.font_size)
            except (IOError, OSError) as e:
                print(f"Error loading font from {self.font_path}: {e}")
                font = font_manager.get_font(None, self.font_size)
        # Otherwise, try to get it from font manager by name
        else:
            font_name = None
            if isinstance(self.font_path, str):
                # Extract font name from path if it looks like a path
                font_name = os.path.splitext(os.path.basename(self.font_path))[0]
            font = font_manager.get_font(font_name, self.font_size)

        # Handle text wrapping if max_width is specified
        if self.max_width:
            lines = []
            words = self.text.split()

            if not words:
                return result

            current_line = words[0]

            for word in words[1:]:
                # Check if adding this word exceeds max_width
                test_line = current_line + " " + word
                text_width = draw.textlength(test_line, font=font)

                if text_width <= self.max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word

            lines.append(current_line)

            # Draw each line
            y_offset = self.position[1]
            for line in lines:
                draw.text(
                    (self.position[0], y_offset), line, font=font, fill=self.color
                )
                y_offset += self.font_size + 5  # Add some spacing between lines
        else:
            # Draw text without wrapping
            draw.text(self.position, self.text, font=font, fill=self.color)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "TextComponent":
        """Create a text component from a configuration dictionary"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        return cls(
            text=config.get("text", ""),
            position=position,
            font_size=config.get("font_size", 24),
            color=tuple(config.get("color", (0, 0, 0))),
            max_width=config.get("max_width"),
            font_path=config.get("font_path"),
        )


class ImageComponent(Component):
    """Component for rendering images"""

    def __init__(
        self,
        image_path: Optional[str] = None,
        image_url: Optional[str] = None,
        position: Tuple[int, int] = (0, 0),
        size: Optional[Tuple[int, int]] = None,
        circle_crop: bool = False,
    ):
        """
        Initialize an image component.

        Args:
            image_path: Path to a local image file
            image_url: URL of an image
            position: Position (x, y) to place the image
            size: Size (width, height) to resize the image to
            circle_crop: Whether to crop the image into a circle
        """
        super().__init__(position)
        self.image_path = image_path
        self.image_url = image_url
        self.size = size
        self.circle_crop = circle_crop
        self._image = None

    def _load_image(self) -> Optional[Image.Image]:
        """Load the image from path or URL"""
        if self._image is not None:
            return self._image

        if self.image_path and os.path.exists(self.image_path):
            self._image = Image.open(self.image_path)
        elif self.image_url:
            try:
                response = requests.get(self.image_url)
                response.raise_for_status()
                self._image = Image.open(BytesIO(response.content))
            except (requests.RequestException, IOError):
                return None

        # Resize if needed
        if self._image and self.size:
            self._image = self._image.resize(self.size)

        # Apply circle crop if needed
        if self._image and self.circle_crop:
            self._image = self._circle_crop(self._image)

        return self._image

    def _circle_crop(self, image: Image.Image) -> Image.Image:
        """Crop an image into a circle"""
        # Create a circular mask
        width, height = image.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)

        # Ensure image has alpha channel
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Apply the mask
        result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        result.paste(image, (0, 0), mask)

        return result

    def render(self, image: Image.Image) -> Image.Image:
        """Render the image component onto an image"""
        result = image.copy()

        component_image = self._load_image()
        if component_image is None:
            return result

        # Ensure component image has alpha channel for proper pasting
        if component_image.mode != "RGBA":
            component_image = component_image.convert("RGBA")

        # Paste the component image onto the result
        result.paste(
            component_image,
            self.position,
            component_image if component_image.mode == "RGBA" else None,
        )

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "ImageComponent":
        """Create an image component from a configuration dictionary"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        size = None
        if "size" in config:
            size = (config["size"].get("width", 100), config["size"].get("height", 100))

        return cls(
            image_path=config.get("image_path"),
            image_url=config.get("image_url"),
            position=position,
            size=size,
            circle_crop=config.get("circle_crop", False),
        )


class CTAButtonComponent(Component):
    """Component for rendering CTA buttons"""

    def __init__(
        self,
        text: str,
        position: Tuple[int, int] = (0, 0),
        size: Tuple[int, int] = (200, 50),
        bg_color: Tuple[int, int, int] = (0, 123, 255),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        corner_radius: int = 10,
        font_path: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """
        Initialize a CTA button component.

        Args:
            text: Button text
            position: Position (x, y) of the button
            size: Size (width, height) of the button
            bg_color: RGB color tuple for button background
            text_color: RGB color tuple for button text
            corner_radius: Radius for rounded corners
            font_path: Path to a TTF font file
            url: URL to link to (for metadata)
        """
        super().__init__(position)
        self.text = text
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.font_path = font_path
        self.url = url

    def render(self, image: Image.Image) -> Image.Image:
        """Render a CTA button onto an image"""
        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Draw rounded rectangle for button
        x, y = self.position
        width, height = self.size

        # Draw the button with rounded corners
        draw.rounded_rectangle(
            [x, y, x + width, y + height], fill=self.bg_color, radius=self.corner_radius
        )

        # Use font manager to get the font
        font_manager = get_font_manager()

        # If font_path is already a font object, use it directly
        if hasattr(self.font_path, "getsize"):  # Check if it's a font object
            font = self.font_path
        # If it's a string path that exists, try to load it
        elif isinstance(self.font_path, str) and os.path.exists(self.font_path):
            try:
                font = ImageFont.truetype(self.font_path, 18)
            except (IOError, OSError) as e:
                print(f"Error loading font from {self.font_path}: {e}")
                font = font_manager.get_font("Roboto-Bold", 18)
        # Otherwise, use default font
        else:
            font = font_manager.get_font("Roboto-Bold", 18)

        # Calculate text position to center it in the button
        text_width = draw.textlength(self.text, font=font)
        text_x = x + (width - text_width) // 2
        text_y = y + (height - 18) // 2  # Approximate font height

        # Draw the text
        draw.text((text_x, text_y), self.text, font=font, fill=self.text_color)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "CTAButtonComponent":
        """Create a CTA button component from a configuration dictionary"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        size = (
            config.get("size", {}).get("width", 200),
            config.get("size", {}).get("height", 50),
        )

        return cls(
            text=config.get("text", "Click Here"),
            position=position,
            size=size,
            bg_color=tuple(config.get("bg_color", (0, 123, 255))),
            text_color=tuple(config.get("text_color", (255, 255, 255))),
            corner_radius=config.get("corner_radius", 10),
            font_path=config.get("font_path"),
            url=config.get("url"),
        )


class FooterComponent(Component):
    """Component for rendering a footer"""

    def __init__(
        self,
        text: str,
        position: Optional[Tuple[int, int]] = None,
        font_size: int = 14,
        color: Tuple[int, int, int] = (100, 100, 100),
        bg_color: Optional[Tuple[int, int, int]] = None,
        padding: int = 10,
        font_path: Optional[str] = None,
    ):
        """
        Initialize a footer component.

        Args:
            text: Footer text
            position: Position (x, y) of the footer (if None, will be placed at bottom)
            font_size: Font size
            color: RGB color tuple for text
            bg_color: RGB color tuple for background (None for transparent)
            padding: Padding around the text
            font_path: Path to a TTF font file
        """
        super().__init__(position if position else (0, 0))
        self.text = text
        self.font_size = font_size
        self.color = color
        self.bg_color = bg_color
        self.padding = padding
        self.font_path = font_path
        self._auto_position = position is None

    def render(self, image: Image.Image) -> Image.Image:
        """Render a footer onto an image"""
        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Use font manager to get the font
        font_manager = get_font_manager()

        # If font_path is already a font object, use it directly
        if hasattr(self.font_path, "getsize"):  # Check if it's a font object
            font = self.font_path
        # If it's a string path that exists, try to load it
        elif isinstance(self.font_path, str) and os.path.exists(self.font_path):
            try:
                font = ImageFont.truetype(self.font_path, self.font_size)
            except (IOError, OSError) as e:
                print(f"Error loading font from {self.font_path}: {e}")
                font = font_manager.get_font("OpenSans-Regular", self.font_size)
        # Otherwise, use default font
        else:
            font = font_manager.get_font("OpenSans-Regular", self.font_size)

        # Calculate position if auto-positioning is enabled
        if self._auto_position:
            width, height = image.size
            text_width = draw.textlength(self.text, font=font)
            x = (width - text_width) // 2
            y = height - self.font_size - self.padding * 2
            self.position = (x, y)

        # Draw background if specified
        if self.bg_color:
            text_width = draw.textlength(self.text, font=font)
            x, y = self.position
            draw.rectangle(
                [
                    x - self.padding,
                    y - self.padding,
                    x + text_width + self.padding,
                    y + self.font_size + self.padding,
                ],
                fill=self.bg_color,
            )

        # Draw the text
        draw.text(self.position, self.text, font=font, fill=self.color)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "FooterComponent":
        """Create a footer component from a configuration dictionary"""
        position = None
        if "position" in config:
            position = (config["position"].get("x", 0), config["position"].get("y", 0))

        bg_color = None
        if "bg_color" in config:
            bg_color = tuple(config["bg_color"])

        return cls(
            text=config.get("text", ""),
            position=position,
            font_size=config.get("font_size", 14),
            color=tuple(config.get("color", (100, 100, 100))),
            bg_color=bg_color,
            padding=config.get("padding", 10),
            font_path=config.get("font_path"),
        )


def create_component_from_config(config: Dict[str, Any]) -> Optional[Component]:
    """
    Factory function to create a component from a configuration dictionary.

    Args:
        config: Configuration dictionary with a "type" field

    Returns:
        A component instance or None if the type is unknown
    """
    component_type = config.get("type")

    if component_type == "text":
        return TextComponent.from_config(config)
    elif component_type == "image":
        return ImageComponent.from_config(config)
    elif component_type == "cta_button":
        return CTAButtonComponent.from_config(config)
    elif component_type == "footer":
        return FooterComponent.from_config(config)

    return None
