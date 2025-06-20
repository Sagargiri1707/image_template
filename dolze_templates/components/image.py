"""
Image component for rendering images in templates.
"""

import os
import requests
from io import BytesIO
from typing import Tuple, Optional, Dict, Any, Union
from PIL import Image, ImageOps, ImageDraw
from .base import Component


class ImageComponent(Component):
    """Component for rendering images"""

    def __init__(
        self,
        image_path: Optional[str] = None,
        image_url: Optional[str] = None,
        position: Tuple[int, int] = (0, 0),
        size: Optional[Tuple[int, int]] = None,
        circle_crop: bool = False,
        opacity: float = 1.0,
        border_radius: int = 0,
    ):
        """
        Initialize an image component.

        Args:
            image_path: Path to a local image file
            image_url: URL of an image to download
            position: Position (x, y) to place the image
            size: Optional size (width, height) to resize the image to
            circle_crop: Whether to crop the image to a circle
            opacity: Opacity of the image (0.0 to 1.0)
            border_radius: Radius for rounded corners in pixels (0 for no rounding)
        """
        super().__init__(position)
        self.image_path = image_path
        self.image_url = image_url
        self.size = size
        self.circle_crop = circle_crop
        self.opacity = max(0.0, min(1.0, opacity))  # Clamp between 0 and 1
        self.border_radius = max(0, int(border_radius))  # Ensure non-negative integer
        self._cached_image = None

    def _load_image(self) -> Optional[Image.Image]:
        """
        Load the image from path or URL if not already loaded.

        Returns:
            Loaded PIL Image or None if loading fails
        """
        if self._cached_image is not None:
            return self._cached_image

        try:
            if self.image_path and os.path.exists(self.image_path):
                img = Image.open(self.image_path)
            elif self.image_url:
                response = requests.get(self.image_url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            else:
                return None

            # Convert to RGBA if needed
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            # Apply opacity if needed
            if self.opacity < 1.0:
                alpha = img.split()[3]
                alpha = Image.eval(alpha, lambda x: int(x * self.opacity))
                img.putalpha(alpha)

            self._cached_image = img
            return img

        except (IOError, requests.RequestException) as e:
            print(f"Error loading image: {e}")
            return None

    def render(self, image: Image.Image) -> Image.Image:
        """
        Render the image onto the template.

        Args:
            image: The base image to render onto

        Returns:
            The image with the component rendered on it
        """
        img = self._load_image()
        if img is None:
            return image

        result = image.copy()

        # Resize if needed
        if self.size:
            img = img.resize(self.size, Image.Resampling.LANCZOS)

        # Apply circle crop if needed
        if self.circle_crop:
            # Create a mask
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, *img.size), fill=255)

            # Apply the mask
            result_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
            result_img.paste(img, (0, 0), mask)
            img = result_img
        # Apply border radius if specified
        elif self.border_radius > 0:
            # Create a mask with rounded corners
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            
            # Draw a rounded rectangle on the mask
            draw.rounded_rectangle(
                [(0, 0), (img.width - 1, img.height - 1)],
                radius=self.border_radius,
                fill=255
            )
            
            # Apply the mask
            result_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
            result_img.paste(img, (0, 0), mask)
            img = result_img

        # Paste the image at the specified position
        if img.mode == "RGBA":
            result.alpha_composite(img, self.position)
        else:
            result.paste(img, self.position)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "ImageComponent":
        """
        Create an image component from a configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            A new ImageComponent instance
        """
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        size = None
        if "size" in config:
            size = (
                config["size"].get("width"),
                config["size"].get("height"),
            )
            if None in size:
                size = None

        return cls(
            image_path=config.get("image_path"),
            image_url=config.get("image_url"),
            position=position,
            size=size,
            circle_crop=config.get("circle_crop", False),
            opacity=float(config.get("opacity", 1.0)),
            border_radius=int(config.get("border_radius", 0)),
        )
