"""Shape classes for the vector editor."""

import math
import uuid
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for all shapes.

    Each shape has a unique ID assigned automatically at creation.
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

    def __repr__(self) -> str:
        return f"[{self._id}] {self.describe()}"


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

    def distance_to(self, other: "Point") -> float:
        """Calculate Euclidean distance to another point.

        Args:
            other: Target point.

        Returns:
            Distance between the two points.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


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
