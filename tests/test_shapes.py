"""Unit tests for shape classes.

Coverage:
- Point: creation, type, describe, unique IDs, distance_to, negatives, float conversion
- Segment: creation, type, length (Pythagorean triples, horizontal, vertical, zero)
- Circle: creation, type, area, perimeter, invalid radius (0, negative)
- Square: creation, type, area, perimeter, invalid side (0, negative)
- Rectangle: creation, type, area, perimeter, invalid width/height
- Oval: creation, type, area, perimeter approximation, invalid rx/ry
- Serialization: to_dict / shape_from_dict round-trip for all shape types
- All shapes: ID uniqueness across types, __repr__ format
"""

import math

import pytest

from vector_editor.shapes import (
    Circle, Oval, Point, Rectangle, Segment, Square, shape_from_dict,
)


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

    def test_to_dict_round_trip(self):
        """to_dict / shape_from_dict restores Point with same attributes and ID."""
        p = Point(3, 7)
        restored = shape_from_dict(p.to_dict())
        assert isinstance(restored, Point)
        assert restored.x == p.x
        assert restored.y == p.y
        assert restored.id == p.id


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

    def test_to_dict_round_trip(self):
        """to_dict / shape_from_dict restores Segment with same attributes and ID."""
        s = Segment(1, 2, 3, 4)
        restored = shape_from_dict(s.to_dict())
        assert isinstance(restored, Segment)
        assert restored.start == s.start
        assert restored.end == s.end
        assert restored.id == s.id


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

    def test_to_dict_round_trip(self):
        """to_dict / shape_from_dict restores Circle correctly."""
        c = Circle(1, 2, 5)
        restored = shape_from_dict(c.to_dict())
        assert isinstance(restored, Circle)
        assert restored.cx == c.cx
        assert restored.cy == c.cy
        assert restored.radius == c.radius
        assert restored.id == c.id


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

    def test_to_dict_round_trip(self):
        """to_dict / shape_from_dict restores Square correctly."""
        s = Square(2, 3, 6)
        restored = shape_from_dict(s.to_dict())
        assert isinstance(restored, Square)
        assert restored.x == s.x
        assert restored.y == s.y
        assert restored.side == s.side
        assert restored.id == s.id


# ---------------------------------------------------------------------------
# Rectangle  (new)
# ---------------------------------------------------------------------------

class TestRectangle:
    """Tests for the Rectangle shape."""

    def test_creation_stores_attributes(self):
        """Rectangle stores origin, width, and height correctly."""
        r = Rectangle(1, 2, 10, 5)
        assert r.x == 1.0 and r.y == 2.0 and r.width == 10.0 and r.height == 5.0

    def test_shape_type(self):
        """shape_type returns 'rectangle'."""
        assert Rectangle(0, 0, 1, 1).shape_type == "rectangle"

    def test_area(self):
        """Area equals width × height."""
        assert Rectangle(0, 0, 4, 5).area() == pytest.approx(20.0)

    def test_perimeter(self):
        """Perimeter equals 2 × (width + height)."""
        assert Rectangle(0, 0, 4, 5).perimeter() == pytest.approx(18.0)

    def test_square_is_special_case(self):
        """Rectangle with equal sides behaves like a square numerically."""
        r = Rectangle(0, 0, 5, 5)
        assert r.area() == pytest.approx(25.0)
        assert r.perimeter() == pytest.approx(20.0)

    def test_invalid_width_zero(self):
        """Width of 0 raises ValueError."""
        with pytest.raises(ValueError):
            Rectangle(0, 0, 0, 5)

    def test_invalid_height_negative(self):
        """Negative height raises ValueError."""
        with pytest.raises(ValueError):
            Rectangle(0, 0, 5, -3)

    def test_describe_contains_dimensions(self):
        """describe() contains width and height."""
        desc = Rectangle(0, 0, 4, 5).describe()
        assert "width" in desc.lower() and "height" in desc.lower()

    def test_ids_are_unique(self):
        """Two Rectangle instances get different IDs."""
        assert Rectangle(0, 0, 1, 1).id != Rectangle(0, 0, 1, 1).id

    def test_to_dict_round_trip(self):
        """to_dict / shape_from_dict restores Rectangle correctly."""
        r = Rectangle(1, 2, 8, 3)
        restored = shape_from_dict(r.to_dict())
        assert isinstance(restored, Rectangle)
        assert restored.x == r.x
        assert restored.y == r.y
        assert restored.width == r.width
        assert restored.height == r.height
        assert restored.id == r.id


# ---------------------------------------------------------------------------
# Oval  (new)
# ---------------------------------------------------------------------------

class TestOval:
    """Tests for the Oval shape."""

    def test_creation_stores_attributes(self):
        """Oval stores center and semi-axes correctly."""
        o = Oval(1, 2, 5, 3)
        assert o.cx == 1.0 and o.cy == 2.0 and o.rx == 5.0 and o.ry == 3.0

    def test_shape_type(self):
        """shape_type returns 'oval'."""
        assert Oval(0, 0, 1, 1).shape_type == "oval"

    def test_area(self):
        """Area equals π·rx·ry."""
        o = Oval(0, 0, 3, 4)
        assert o.area() == pytest.approx(math.pi * 3 * 4)

    def test_area_equal_axes_matches_circle(self):
        """Oval with equal axes has the same area as a circle of that radius."""
        r = 5.0
        assert Oval(0, 0, r, r).area() == pytest.approx(math.pi * r ** 2)

    def test_perimeter_is_positive(self):
        """Perimeter (Ramanujan approximation) is always positive."""
        assert Oval(0, 0, 10, 3).perimeter() > 0

    def test_perimeter_equal_axes_approximates_circle(self):
        """Oval with equal axes approximates circle circumference."""
        r = 5.0
        assert Oval(0, 0, r, r).perimeter() == pytest.approx(2 * math.pi * r, rel=1e-3)

    def test_invalid_rx_zero(self):
        """rx of 0 raises ValueError."""
        with pytest.raises(ValueError):
            Oval(0, 0, 0, 5)

    def test_invalid_ry_negative(self):
        """Negative ry raises ValueError."""
        with pytest.raises(ValueError):
            Oval(0, 0, 5, -1)

    def test_describe_contains_axes(self):
        """describe() contains rx and ry."""
        desc = Oval(0, 0, 3, 5).describe()
        assert "rx" in desc.lower() and "ry" in desc.lower()

    def test_ids_are_unique(self):
        """Two Oval instances get different IDs."""
        assert Oval(0, 0, 1, 2).id != Oval(0, 0, 1, 2).id

    def test_to_dict_round_trip(self):
        """to_dict / shape_from_dict restores Oval correctly."""
        o = Oval(1, 2, 6, 4)
        restored = shape_from_dict(o.to_dict())
        assert isinstance(restored, Oval)
        assert restored.cx == o.cx
        assert restored.cy == o.cy
        assert restored.rx == o.rx
        assert restored.ry == o.ry
        assert restored.id == o.id


# ---------------------------------------------------------------------------
# shape_from_dict — error handling
# ---------------------------------------------------------------------------

class TestShapeFromDict:
    """Tests for the shape_from_dict factory."""

    def test_unknown_type_raises(self):
        """shape_from_dict raises ValueError for unknown type."""
        with pytest.raises(ValueError, match="Unknown shape type"):
            shape_from_dict({"type": "hexagon"})


# ---------------------------------------------------------------------------
# Cross-type ID uniqueness
# ---------------------------------------------------------------------------

class TestCrossTypeIds:
    """ID uniqueness is guaranteed across different shape types."""

    def test_all_shape_types_have_unique_ids(self):
        shapes = [
            Point(0, 0), Segment(0, 0, 1, 1),
            Circle(0, 0, 1), Square(0, 0, 1),
            Rectangle(0, 0, 2, 3), Oval(0, 0, 2, 1),
        ]
        ids = [s.id for s in shapes]
        assert len(ids) == len(set(ids))
