"""
Validation utilities for template and component configurations.
"""
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path


def validate_color(color: Any) -> Tuple[int, int, int, int]:
    """
    Validate and normalize a color value to RGBA tuple.
    
    Args:
        color: Color value to validate (can be list, tuple, or hex string)
        
    Returns:
        Normalized RGBA tuple (r, g, b, a)
        
    Raises:
        ValueError: If the color format is invalid
    """
    if color is None:
        return (0, 0, 0, 0)  # Transparent
        
    if isinstance(color, str) and color.startswith('#'):
        # Handle hex color (e.g., "#RRGGBB" or "#RRGGBBAA")
        hex_color = color.lstrip('#')
        if len(hex_color) not in (3, 4, 6, 8):
            raise ValueError(f"Invalid hex color: {color}")
            
        # Expand shorthand (e.g., "#RGB" -> "RRGGBB")
        if len(hex_color) in (3, 4):
            hex_color = ''.join(c * 2 for c in hex_color)
            
        # Convert to RGBA
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16) if len(hex_color) > 4 else 255
            a = int(hex_color[6:8], 16) if len(hex_color) > 6 else 255
            return (r, g, b, a)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid hex color: {color}") from e
            
    if isinstance(color, (list, tuple)):
        if len(color) == 3:  # RGB
            if all(isinstance(c, (int, float)) and 0 <= c <= 255 for c in color):
                return (*[int(c) for c in color], 255)
        elif len(color) == 4:  # RGBA
            if all(isinstance(c, (int, float)) and 0 <= c <= 255 for c in color):
                return tuple(int(c) for c in color)
                
    raise ValueError(f"Invalid color format: {color}")


def validate_position(position: Any) -> Tuple[int, int]:
    """
    Validate and normalize a position value.
    
    Args:
        position: Position value to validate (can be dict with x,y or tuple/list)
        
    Returns:
        Normalized position tuple (x, y)
        
    Raises:
        ValueError: If the position format is invalid
    """
    if isinstance(position, dict):
        try:
            x = int(position.get('x', 0))
            y = int(position.get('y', 0))
            return (x, y)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid position format: {position}") from e
            
    if isinstance(position, (list, tuple)) and len(position) == 2:
        try:
            return (int(position[0]), int(position[1]))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid position format: {position}") from e
            
    raise ValueError(f"Invalid position format: {position}")


def validate_size(size: Any) -> Tuple[int, int]:
    """
    Validate and normalize a size value.
    
    Args:
        size: Size value to validate (can be dict with width,height or tuple/list)
        
    Returns:
        Normalized size tuple (width, height)
        
    Raises:
        ValueError: If the size format is invalid
    """
    if isinstance(size, dict):
        try:
            width = int(size.get('width', 0))
            height = int(size.get('height', 0))
            if width < 0 or height < 0:
                raise ValueError("Size values must be non-negative")
            return (width, height)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid size format: {size}") from e
            
    if isinstance(size, (list, tuple)) and len(size) == 2:
        try:
            width, height = int(size[0]), int(size[1])
            if width < 0 or height < 0:
                raise ValueError("Size values must be non-negative")
            return (width, height)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid size format: {size}") from e
            
    raise ValueError(f"Invalid size format: {size}")


def validate_font_path(font_path: Any) -> Optional[str]:
    """
    Validate a font path.
    
    Args:
        font_path: Font path to validate
        
    Returns:
        Normalized font path if valid, None otherwise
    """
    if font_path is None:
        return None
        
    if isinstance(font_path, str):
        # Check if it's a system font name or a file path
        if '.' not in font_path.split('/')[-1]:  # No file extension, treat as font name
            return font_path
            
        # Check if file exists
        path = Path(font_path)
        if path.exists() and path.is_file():
            return str(path.absolute())
            
    return None

def validate_template_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize a template configuration.
    
    Args:
        config: Template configuration to validate
        
    Returns:
        Normalized template configuration
        
    Raises:
        ValueError: If the configuration is invalid
    """
    if not isinstance(config, dict):
        raise ValueError("Template config must be a dictionary")
        
    # Validate required fields
    if 'name' not in config:
        raise ValueError("Template config must include a 'name' field")
        
    if 'components' not in config or not isinstance(config['components'], list):
        raise ValueError("Template config must include a 'components' list")
    
    # Set defaults
    normalized = {
        'name': str(config['name']),
        'components': [],
        'size': validate_size(config.get('size', {'width': 800, 'height': 600})),
        'background_color': validate_color(config.get('background_color', (255, 255, 255))),
        'use_base_image': bool(config.get('use_base_image', False)),
    }
    
    # Validate components
    for i, component in enumerate(config['components']):
        if not isinstance(component, dict):
            raise ValueError(f"Component at index {i} must be a dictionary")
            
        if 'type' not in component:
            raise ValueError(f"Component at index {i} is missing 'type' field")
            
        # Basic validation for common component fields
        if 'position' in component:
            component['position'] = validate_position(component['position'])
            
        if 'size' in component:
            component['size'] = validate_size(component['size'])
            
        if 'color' in component or 'text_color' in component:
            color_field = 'color' if 'color' in component else 'text_color'
            component[color_field] = validate_color(component[color_field])
            
        if 'font_path' in component:
            component['font_path'] = validate_font_path(component['font_path'])
        
        normalized['components'].append(component)
    
    return normalized
