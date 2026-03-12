"""Unit tests for shape classes.

Coverage:
- Point: creation, type, describe, unique IDs, distance_to, negatives, float conversion
- Segment: creation, type, length (Pythagorean triples, horizontal, vertical, zero)
- Circle: creation, type, area, perimeter, invalid radius (0, negative)
- Square: creation, type, area, perimeter, invalid side (0, negative)
- All shapes: ID uniqueness across types, __repr__ format
"""

import math

import pytest

from vector_editor.shapes import Circle, Point, Segment, Square


# ---------------------------------------------------------------------------
# Point
# ---------------------------------------------------------------------------

class TestPoint:
    """Tests for the Point shape."""

    def test_creation_stores_coordinates(self):
        """Point stores x and y as floats."""
        p = Point(1, 2)
        assert p.x == 1.0
        assert p.y == 2.0

    def test_shape_type(self):
        """shape_type returns 'point'."""
        assert Point(0, 0).shape_type == "point"

    def test_describe_contains_coordinates(self):
        """describe() contains x and y values."""
        desc = Point(3, 4).describe()
        assert "3.0" in desc and "4.0" in desc

    def test_id_is_assigned(self):
        """Each Point gets a non-empty ID."""
        p = Point(0, 0)
        assert p.id and len(p.id) > 0

    def test_ids_are_unique(self):
        """Two Point instances always get different IDs."""
        assert Point(0, 0).id != Point(0, 0).id

    def test_distance_to_345_triangle(self):
        """distance_to() returns 5 for the classic 3-4-5 right triangle."""
        assert Point(0, 0).distance_to(Point(3, 4)) == pytest.approx(5.0)

    def test_distance_to_self_is_zero(self):
        """Distance from a point to itself is 0."""
        p = Point(7, 7)
        assert p.distance_to(p) == 0.0

    def test_negative_coordinates(self):
        """Point accepts negative coordinates."""
        p = Point(-3, -5)
        assert p.x == -3.0 and p.y == -5.0

    def test_string_inputs_are_converted(self):
        """Point converts string arguments to float."""
        p = Point("1.5", "2.5")
        assert p.x == 1.5 and p.y == 2.5

    def test_repr_contains_id(self):
        """__repr__ includes the shape ID in brackets."""
        p = Point(1, 2)
        assert f"[{p.id}]" in repr(p)


# ---------------------------------------------------------------------------
# Segment
# ---------------------------------------------------------------------------

class TestSegment:
    """Tests for the Segment shape."""

    def test_creation_stores_endpoints(self):
        """Segment stores start and end as float tuples."""
        s = Segment(0, 0, 3, 4)
        assert s.start == (0.0, 0.0)
        assert s.end == (3.0, 4.0)

    def test_shape_type(self):
        """shape_type returns 'segment'."""
        assert Segment(0, 0, 1, 1).shape_type == "segment"

    def test_length_pythagorean_triple(self):
        """length() returns 5 for a 3-4-5 segment."""
        assert Segment(0, 0, 3, 4).length() == pytest.approx(5.0)

    def test_length_horizontal(self):
        """Horizontal segment length equals x difference."""
        assert Segment(0, 0, 5, 0).length() == pytest.approx(5.0)

    def test_length_vertical(self):
        """Vertical segment length equals y difference."""
        assert Segment(0, 0, 0, 5).length() == pytest.approx(5.0)

    def test_length_zero(self):
        """Degenerate segment (point) has length 0."""
        assert Segment(3, 3, 3, 3).length() == 0.0

    def test_describe_contains_length(self):
        """describe() mentions the word 'length'."""
        assert "length" in Segment(0, 0, 1, 1).describe().lower()

    def test_ids_are_unique(self):
        """Two Segment instances get different IDs."""
        assert Segment(0, 0, 1, 1).id != Segment(0, 0, 1, 1).id


# ---------------------------------------------------------------------------
# Circle
# ---------------------------------------------------------------------------

class TestCircle:
    """Tests for the Circle shape."""

    def test_creation_stores_attributes(self):
        """Circle stores center and radius correctly."""
        c = Circle(1, 2, 3)
        assert c.cx == 1.0 and c.cy == 2.0 and c.radius == 3.0

    def test_shape_type(self):
        """shape_type returns 'circle'."""
        assert Circle(0, 0, 1).shape_type == "circle"

    def test_area_unit_circle(self):
        """Area of a unit circle is π."""
        assert Circle(0, 0, 1).area() == pytest.approx(math.pi)

    def test_area_radius_5(self):
        """Area with radius 5 is 25π."""
        assert Circle(0, 0, 5).area() == pytest.approx(25 * math.pi)

    def test_perimeter_unit_circle(self):
        """Perimeter of a unit circle is 2π."""
        assert Circle(0, 0, 1).perimeter() == pytest.approx(2 * math.pi)

    def test_invalid_radius_zero(self):
        """Radius of 0 raises ValueError."""
        with pytest.raises(ValueError):
            Circle(0, 0, 0)

    def test_invalid_radius_negative(self):
        """Negative radius raises ValueError."""
        with pytest.raises(ValueError):
            Circle(0, 0, -10)

    def test_describe_contains_radius(self):
        """describe() mentions radius."""
        assert "radius" in Circle(0, 0, 5).describe().lower()

    def test_ids_are_unique(self):
        """Two Circle instances get different IDs."""
        assert Circle(0, 0, 1).id != Circle(0, 0, 1).id


# ---------------------------------------------------------------------------
# Square
# ---------------------------------------------------------------------------

class TestSquare:
    """Tests for the Square shape."""

    def test_creation_stores_attributes(self):
        """Square stores origin and side correctly."""
        s = Square(1, 2, 4)
        assert s.x == 1.0 and s.y == 2.0 and s.side == 4.0

    def test_shape_type(self):
        """shape_type returns 'square'."""
        assert Square(0, 0, 1).shape_type == "square"

    def test_area(self):
        """Area equals side²."""
        assert Square(0, 0, 5).area() == pytest.approx(25.0)

    def test_perimeter(self):
        """Perimeter equals 4 × side."""
        assert Square(0, 0, 5).perimeter() == pytest.approx(20.0)

    def test_invalid_side_zero(self):
        """Side of 0 raises ValueError."""
        with pytest.raises(ValueError):
            Square(0, 0, 0)

    def test_invalid_side_negative(self):
        """Negative side raises ValueError."""
        with pytest.raises(ValueError):
            Square(0, 0, -3)

    def test_describe_contains_side(self):
        """describe() mentions side."""
        assert "side" in Square(0, 0, 3).describe().lower()

    def test_ids_are_unique(self):
        """Two Square instances get different IDs."""
        assert Square(0, 0, 1).id != Square(0, 0, 1).id


# ---------------------------------------------------------------------------
# Cross-type ID uniqueness
# ---------------------------------------------------------------------------

class TestCrossTypeIds:
    """ID uniqueness is guaranteed across different shape types."""

    def test_all_shape_types_have_unique_ids(self):
        shapes = [Point(0, 0), Segment(0, 0, 1, 1), Circle(0, 0, 1), Square(0, 0, 1)]
        ids = [s.id for s in shapes]
        assert len(ids) == len(set(ids))
