"""
Text component for rendering text in templates.
"""
import os
from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
from .base import Component
from dolze_templates.core.font_manager import get_font_manager


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
        alignment: str = "left",
    ):
        """
        Initialize a text component.

        Args:
            text: Text to render
            position: Position (x, y) to place the text
            font_size: Font size
            color: RGB color tuple
            max_width: Maximum width for text wrapping
            font_path: Path to a TTF font file or font name
            alignment: Text alignment ('left', 'center', 'right')
        """
        super().__init__(position)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.max_width = max_width
        self.font_path = font_path
        self.alignment = alignment.lower()

        # Validate alignment
        if self.alignment not in ["left", "center", "right"]:
            print(f"Warning: Invalid alignment '{alignment}'. Defaulting to 'left'.")
            self.alignment = "left"

    def render(self, image: Image.Image) -> Image.Image:
        """Render text onto an image"""
        if not self.text:  # Skip rendering if text is None or empty
            return image

        result = image.copy()
        draw = ImageDraw.Draw(result)

        # Use font manager to get the font
        font_manager = get_font_manager()
        font = font_manager.get_font(self.font_path, self.font_size)

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

            # Draw each line with proper alignment
            y_offset = self.position[1]
            for line in lines:
                line_width = draw.textlength(line, font=font)

                # Calculate x position based on alignment
                if self.alignment == "center":
                    x = self.position[0] + (self.max_width - line_width) // 2
                elif self.alignment == "right":
                    x = self.position[0] + (self.max_width - line_width)
                else:  # left alignment (default)
                    x = self.position[0]

                draw.text((x, y_offset), line, font=font, fill=self.color)
                y_offset += self.font_size + 5  # Add some spacing between lines
        else:
            # For single line without max_width, just draw the text at the given position
            # (alignment doesn't apply as there's no width constraint)
            draw.text(self.position, self.text, font=font, fill=self.color)

        return result

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'TextComponent':
        """Create a text component from a configuration dictionary"""
        position = (
            config.get("position", {}).get("x", 0),
            config.get("position", {}).get("y", 0),
        )

        # Handle color which might be a list or tuple
        color = config.get("color", (0, 0, 0))
        if isinstance(color, (list, tuple)) and len(color) >= 3:
            color = tuple(color[:3])  # Ensure it's a tuple of 3 values
        else:
            color = (0, 0, 0)  # Default to black if invalid

        return cls(
            text=config.get("text", ""),
            position=position,
            font_size=config.get("font_size", 24),
            color=color,
            max_width=config.get("max_width"),
            font_path=config.get("font_path"),
            alignment=config.get("alignment", "left"),
        )
