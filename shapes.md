# Dolze Image Templates - Shapes Documentation

This document outlines the various shapes and their supported properties in the Dolze Image Templates library.

## Common Properties

All shape components inherit these common properties from the base `Component` class:

- `position` (Tuple[int, int]): The (x, y) coordinates of the shape's position on the canvas
  - Example: `(100, 200)` places the shape at x=100, y=200

## Available Shapes

### 1. Circle

Renders a circular shape with optional fill, outline, and gradient effects.

**Properties:**
- `radius` (int): The radius of the circle in pixels
- `fill_color` (Optional[Tuple[int, int, int]]): RGB tuple for the fill color (e.g., `(255, 0, 0)` for red)
- `outline_color` (Optional[Tuple[int, int, int]]): RGB tuple for the outline color
- `outline_width` (int): Width of the outline in pixels (default: 1)
- `gradient_config` (Optional[Dict[str, Any]]): Configuration for gradient fill
  - `type`: Either "linear" or "radial"
  - `colors`: List of color stops (e.g., `["#FF0000", "#0000FF"]`)
  - `direction` (for linear): Gradient angle in degrees (0-360)
  - `center` (for radial): Center point as (x, y) ratios (0.0-1.0)

**Example Configuration:**
```json
{
  "type": "circle",
  "position": {"x": 100, "y": 100},
  "radius": 50,
  "fill_color": [255, 0, 0],
  "outline_color": [0, 0, 0],
  "outline_width": 2,
  "gradient_config": {
    "type": "radial",
    "colors": ["#FF0000", "#0000FF"],
    "center": [0.5, 0.5]
  }
}
```

### 2. Rectangle

Renders a rectangular shape with optional rounded corners, fill, outline, and gradient effects.

**Properties:**
- `size` (Tuple[int, int]): The (width, height) of the rectangle in pixels
- `fill_color` (Optional[Tuple[int, int, int]]): RGB tuple for the fill color
- `outline_color` (Optional[Tuple[int, int, int]]): RGB tuple for the outline color
- `outline_width` (int): Width of the outline in pixels (default: 1)
- `border_radius` (int): Radius of the corners in pixels (0 for square corners)
- `gradient_config`: Same as Circle component

**Example Configuration:**
```json
{
  "type": "rectangle",
  "position": {"x": 50, "y": 50},
  "size": [200, 100],
  "fill_color": [0, 255, 0],
  "outline_color": [0, 0, 0],
  "outline_width": 1,
  "border_radius": 10,
  "gradient_config": {
    "type": "linear",
    "colors": ["#00FF00", "#0000FF"],
    "direction": 45
  }
}
```

### 3. Polygon

Renders a custom polygon shape defined by a list of points, with optional fill, outline, and gradient effects.

**Properties:**
- `points` (List[Tuple[int, int]]): List of (x, y) points that define the polygon
- `fill_color` (Optional[Tuple[int, int, int]]): RGB tuple for the fill color
- `outline_color` (Optional[Tuple[int, int, int]]): RGB tuple for the outline color
- `outline_width` (int): Width of the outline in pixels (default: 1)
- `gradient_config`: Same as Circle component

**Example Configuration:**
```json
{
  "type": "polygon",
  "position": {"x": 0, "y": 0},
  "points": [
    [0, 0],
    [100, 50],
    [0, 100],
    [50, 50]
  ],
  "fill_color": [0, 0, 255],
  "outline_color": [0, 0, 0],
  "outline_width": 1,
  "gradient_config": {
    "type": "linear",
    "colors": ["#0000FF", "#00FFFF"]
  }
}
```

## Color Formats

Colors can be specified in several formats:

1. **RGB/RGBA Tuples/Lists**:
   - RGB: `[255, 0, 0]` (red)
   - RGBA: `[255, 0, 0, 128]` (semi-transparent red)

2. **Hex Strings**:
   - 3-digit hex: `"#F00"` (red)
   - 4-digit hex: `"#F00F"` (semi-transparent red)
   - 6-digit hex: `"#FF0000"` (red)
   - 8-digit hex: `"#FF0000FF"` (red with full opacity)

## Gradient Configuration

Gradients can be either linear or radial and support multiple color stops:

- **Linear Gradient**:
  ```json
  {
    "type": "linear",
    "colors": ["#FF0000", "#00FF00", "#0000FF"],
    "direction": 90  // 0 = left to right, 90 = top to bottom
  }
  ```

- **Radial Gradient**:
  ```json
  {
    "type": "radial",
    "colors": ["#FF0000", "#0000FF"],
    "center": [0.5, 0.5]  // Center point as ratios of width/height
  }
  ```

## Validation Rules

- All position and size values must be non-negative integers
- Colors must be valid RGB/RGBA tuples or hex strings
- Gradient colors must contain at least 2 color stops
- Border radius must be non-negative
- Outline width must be a non-negative integer

## Best Practices

1. Use gradients sparingly as they can increase render time
2. For complex shapes, consider using the polygon component
3. When using transparency, ensure the output format supports it (e.g., PNG)
4. For performance, prefer solid colors over gradients when possible
5. Test your shapes at different sizes to ensure they scale as expected
