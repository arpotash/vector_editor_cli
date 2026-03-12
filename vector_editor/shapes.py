"""Shape classes for the vector editor."""

import math
import uuid
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for all shapes.

    Each shape has a unique ID assigned automatically at creation.
    Supports JSON serialization via to_dict() / shape_from_dict().
    """

    def __init__(self):
        self._id = str(uuid.uuid4())[:8]

    @property
    def id(self) -> str:
        """Unique identifier of the shape."""
        return self._id

    @property
    @abstractmethod
    def shape_type(self) -> str:
        """Return the type name of the shape (e.g. 'point', 'circle')."""

    @abstractmethod
    def describe(self) -> str:
        """Return a human-readable description of the shape."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize the shape to a JSON-compatible dict (includes 'type' and 'id')."""

    def __repr__(self) -> str:
        return f"[{self._id}] {self.describe()}"

    # ------------------------------------------------------------------
    # Internal helper used by subclasses to build the base dict
    # ------------------------------------------------------------------

    def _base_dict(self) -> dict:
        return {"type": self.shape_type, "id": self._id}


# ---------------------------------------------------------------------------
# Point
# ---------------------------------------------------------------------------

class Point(Shape):
    """A point in 2D space defined by coordinates (x, y).

    Args:
        x: X-coordinate.
        y: Y-coordinate.
    """

    def __init__(self, x: float, y: float):
        super().__init__()
        self.x = float(x)
        self.y = float(y)

    @property
    def shape_type(self) -> str:
        return "point"

    def describe(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def to_dict(self) -> dict:
        return {**self._base_dict(), "x": self.x, "y": self.y}

    def distance_to(self, other: "Point") -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


# ---------------------------------------------------------------------------
# Segment
# ---------------------------------------------------------------------------

class Segment(Shape):
    """A line segment between two points.

    Args:
        x1, y1: Start point coordinates.
        x2, y2: End point coordinates.
    """

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        super().__init__()
        self.start = (float(x1), float(y1))
        self.end = (float(x2), float(y2))

    @property
    def shape_type(self) -> str:
        return "segment"

    def length(self) -> float:
        """Calculate the Euclidean length of the segment."""
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def describe(self) -> str:
        return (
            f"Segment("
            f"start=({self.start[0]}, {self.start[1]}), "
            f"end=({self.end[0]}, {self.end[1]}), "
            f"length={self.length():.2f})"
        )

    def to_dict(self) -> dict:
        return {
            **self._base_dict(),
            "x1": self.start[0], "y1": self.start[1],
            "x2": self.end[0],   "y2": self.end[1],
        }


# ---------------------------------------------------------------------------
# Circle
# ---------------------------------------------------------------------------

class Circle(Shape):
    """A circle defined by a center point and radius.

    Args:
        cx, cy: Center coordinates.
        radius: Circle radius (must be positive).

    Raises:
        ValueError: If radius is not positive.
    """

    def __init__(self, cx: float, cy: float, radius: float):
        super().__init__()
        radius = float(radius)
        if radius <= 0:
            raise ValueError(f"Radius must be positive, got {radius}")
        self.cx = float(cx)
        self.cy = float(cy)
        self.radius = radius

    @property
    def shape_type(self) -> str:
        return "circle"

    def area(self) -> float:
        """Calculate the area of the circle."""
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        """Calculate the circumference of the circle."""
        return 2 * math.pi * self.radius

    def describe(self) -> str:
        return (
            f"Circle("
            f"center=({self.cx}, {self.cy}), "
            f"radius={self.radius}, "
            f"area={self.area():.2f})"
        )

    def to_dict(self) -> dict:
        return {**self._base_dict(), "cx": self.cx, "cy": self.cy, "radius": self.radius}


# ---------------------------------------------------------------------------
# Square
# ---------------------------------------------------------------------------

class Square(Shape):
    """A square defined by its top-left origin and side length.

    Args:
        x, y: Top-left corner coordinates.
        side: Side length (must be positive).

    Raises:
        ValueError: If side is not positive.
    """

    def __init__(self, x: float, y: float, side: float):
        super().__init__()
        side = float(side)
        if side <= 0:
            raise ValueError(f"Side must be positive, got {side}")
        self.x = float(x)
        self.y = float(y)
        self.side = side

    @property
    def shape_type(self) -> str:
        return "square"

    def area(self) -> float:
        """Calculate the area of the square."""
        return self.side ** 2

    def perimeter(self) -> float:
        """Calculate the perimeter of the square."""
        return 4 * self.side

    def describe(self) -> str:
        return (
            f"Square("
            f"origin=({self.x}, {self.y}), "
            f"side={self.side}, "
            f"area={self.area():.2f})"
        )

    def to_dict(self) -> dict:
        return {**self._base_dict(), "x": self.x, "y": self.y, "side": self.side}


# ---------------------------------------------------------------------------
# Rectangle  (new)
# ---------------------------------------------------------------------------

class Rectangle(Shape):
    """A rectangle defined by its top-left origin, width, and height.

    Args:
        x, y: Top-left corner coordinates.
        width: Horizontal size (must be positive).
        height: Vertical size (must be positive).

    Raises:
        ValueError: If width or height is not positive.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__()
        width, height = float(width), float(height)
        if width <= 0:
            raise ValueError(f"Width must be positive, got {width}")
        if height <= 0:
            raise ValueError(f"Height must be positive, got {height}")
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height

    @property
    def shape_type(self) -> str:
        return "rectangle"

    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle."""
        return 2 * (self.width + self.height)

    def describe(self) -> str:
        return (
            f"Rectangle("
            f"origin=({self.x}, {self.y}), "
            f"width={self.width}, height={self.height}, "
            f"area={self.area():.2f})"
        )

    def to_dict(self) -> dict:
        return {
            **self._base_dict(),
            "x": self.x, "y": self.y,
            "width": self.width, "height": self.height,
        }


# ---------------------------------------------------------------------------
# Oval  (new)
# ---------------------------------------------------------------------------

class Oval(Shape):
    """An oval (ellipse) defined by a center point and two semi-axes.

    Args:
        cx, cy: Center coordinates.
        rx: Horizontal semi-axis (must be positive).
        ry: Vertical semi-axis (must be positive).

    Raises:
        ValueError: If rx or ry is not positive.
    """

    def __init__(self, cx: float, cy: float, rx: float, ry: float):
        super().__init__()
        rx, ry = float(rx), float(ry)
        if rx <= 0:
            raise ValueError(f"rx must be positive, got {rx}")
        if ry <= 0:
            raise ValueError(f"ry must be positive, got {ry}")
        self.cx = float(cx)
        self.cy = float(cy)
        self.rx = rx
        self.ry = ry

    @property
    def shape_type(self) -> str:
        return "oval"

    def area(self) -> float:
        """Calculate the area of the oval (π·rx·ry)."""
        return math.pi * self.rx * self.ry

    def perimeter(self) -> float:
        """Approximate the perimeter using the Ramanujan formula."""
        h = ((self.rx - self.ry) / (self.rx + self.ry)) ** 2
        return math.pi * (self.rx + self.ry) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))

    def describe(self) -> str:
        return (
            f"Oval("
            f"center=({self.cx}, {self.cy}), "
            f"rx={self.rx}, ry={self.ry}, "
            f"area={self.area():.2f})"
        )

    def to_dict(self) -> dict:
        return {
            **self._base_dict(),
            "cx": self.cx, "cy": self.cy,
            "rx": self.rx, "ry": self.ry,
        }


# ---------------------------------------------------------------------------
# Deserialization factory
# ---------------------------------------------------------------------------

def shape_from_dict(data: dict) -> Shape:
    """Reconstruct a Shape from a dict produced by Shape.to_dict().

    Args:
        data: Dict with at least a 'type' key.

    Returns:
        The corresponding Shape instance with the original ID restored.

    Raises:
        ValueError: If 'type' is unknown or required keys are missing.
    """
    shape_type = data.get("type")

    match shape_type:
        case "point":
            shape = Point(data["x"], data["y"])
        case "segment":
            shape = Segment(data["x1"], data["y1"], data["x2"], data["y2"])
        case "circle":
            shape = Circle(data["cx"], data["cy"], data["radius"])
        case "square":
            shape = Square(data["x"], data["y"], data["side"])
        case "rectangle":
            shape = Rectangle(data["x"], data["y"], data["width"], data["height"])
        case "oval":
            shape = Oval(data["cx"], data["cy"], data["rx"], data["ry"])
        case _:
            raise ValueError(f"Unknown shape type '{shape_type}' in saved data")

    # Restore the original ID so references stay consistent after load
    if "id" in data:
        shape._id = data["id"]

    return shape
