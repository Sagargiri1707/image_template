"""
Dolze Templates - A flexible template generation library for creating social media posts, banners, and more.

This package provides a powerful and extensible system for generating images with text, shapes, and other
components in a template-based approach.
"""

# Core functionality
from .core import (
    Template,
    TemplateEngine,
    TemplateRegistry,
    get_template_registry,
    FontManager,
    get_font_manager,
)

# Components
from .components import (
    Component,
    TextComponent,
    ImageComponent,
    CircleComponent,
    RectangleComponent,
    CTAButtonComponent,
    FooterComponent,
    create_component_from_config,
)

# Configuration
from .config import (
    Settings,
    get_settings,
    configure,
    DEFAULT_TEMPLATES_DIR,
    DEFAULT_FONTS_DIR,
    DEFAULT_OUTPUT_DIR,
)

# Version
__version__ = "0.1.0"


# Package metadata
__author__ = "Dolze Team"
__email__ = "support@dolze.com"
__license__ = "MIT"
__description__ = "A flexible template generation library for creating social media posts, banners, and more."

# Package-level initialization
def init() -> None:
    """
    Initialize the Dolze Templates package.
    This function ensures all required directories exist and performs any necessary setup.
    """
    settings = get_settings()
    
    # Ensure required directories exist
    import os
    os.makedirs(settings.templates_dir, exist_ok=True)
    os.makedirs(settings.fonts_dir, exist_ok=True)
    os.makedirs(settings.output_dir, exist_ok=True)

# Initialize the package when imported
init()

# Clean up namespace
del init

__all__ = [
    # Core
    'Template',
    'TemplateEngine',
    'TemplateRegistry',
    'get_template_registry',
    'FontManager',
    'get_font_manager',
    
    # Components
    'Component',
    'TextComponent',
    'ImageComponent',
    'CircleComponent',
    'RectangleComponent',
    'CTAButtonComponent',
    'FooterComponent',
    'create_component_from_config',
    
    # Configuration
    'Settings',
    'get_settings',
    'configure',
    'DEFAULT_TEMPLATES_DIR',
    'DEFAULT_FONTS_DIR',
    'DEFAULT_OUTPUT_DIR',
    
    # Metadata
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__description__',
]
