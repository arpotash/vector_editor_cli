"""Unit tests for VectorEditor.

Coverage:
- Initial state (empty)
- add_shape: returns correct ID, increments count, stores object
- remove_shape: returns True on success, False for unknown ID, decrements count
- get_shape: returns the correct object or None
- list_shapes: returns all shapes in insertion order
- count: reflects current number of shapes
- clear: removes all shapes, returns the count removed
- Mixed workflow: add several shapes, delete one, verify the rest remain
"""

import pytest

from vector_editor.editor import VectorEditor
from vector_editor.shapes import Circle, Point, Segment, Square


@pytest.fixture
def editor():
    """Fresh VectorEditor instance for each test."""
    return VectorEditor()


@pytest.fixture
def all_shapes():
    """One instance of each shape type."""
    return [Point(0, 0), Segment(0, 0, 1, 1), Circle(0, 0, 5), Square(1, 1, 3)]


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

class TestInitialState:
    """VectorEditor starts empty."""

    def test_count_is_zero(self, editor):
        """A new editor has 0 shapes."""
        assert editor.count() == 0

    def test_list_is_empty(self, editor):
        """A new editor returns an empty list."""
        assert editor.list_shapes() == []


# ---------------------------------------------------------------------------
# add_shape
# ---------------------------------------------------------------------------

class TestAddShape:
    """Tests for VectorEditor.add_shape()."""

    def test_returns_shape_id(self, editor):
        """add_shape() returns the same ID as shape.id."""
        p = Point(1, 2)
        assert editor.add_shape(p) == p.id

    def test_count_increments(self, editor):
        """count() increases by 1 after each add."""
        editor.add_shape(Point(0, 0))
        assert editor.count() == 1
        editor.add_shape(Circle(0, 0, 5))
        assert editor.count() == 2

    def test_add_all_shape_types(self, editor, all_shapes):
        """All four shape types can be added."""
        for shape in all_shapes:
            editor.add_shape(shape)
        assert editor.count() == 4


# ---------------------------------------------------------------------------
# remove_shape
# ---------------------------------------------------------------------------

class TestRemoveShape:
    """Tests for VectorEditor.remove_shape()."""

    def test_remove_existing_returns_true(self, editor):
        """Removing a known ID returns True."""
        p = Point(0, 0)
        editor.add_shape(p)
        assert editor.remove_shape(p.id) is True

    def test_remove_existing_decrements_count(self, editor):
        """count() decreases by 1 after removal."""
        p = Point(0, 0)
        editor.add_shape(p)
        editor.remove_shape(p.id)
        assert editor.count() == 0

    def test_remove_nonexistent_returns_false(self, editor):
        """Removing an unknown ID returns False."""
        assert editor.remove_shape("does-not-exist") is False

    def test_remove_does_not_affect_other_shapes(self, editor):
        """Removing one shape leaves the others intact."""
        p1, p2, p3 = Point(0, 0), Point(1, 1), Point(2, 2)
        for p in (p1, p2, p3):
            editor.add_shape(p)
        editor.remove_shape(p2.id)
        remaining = editor.list_shapes()
        assert p1 in remaining
        assert p2 not in remaining
        assert p3 in remaining


# ---------------------------------------------------------------------------
# get_shape
# ---------------------------------------------------------------------------

class TestGetShape:
    """Tests for VectorEditor.get_shape()."""

    def test_get_existing_returns_object(self, editor):
        """get_shape() returns the exact object that was added."""
        p = Point(3, 4)
        editor.add_shape(p)
        assert editor.get_shape(p.id) is p

    def test_get_nonexistent_returns_none(self, editor):
        """get_shape() returns None for an unknown ID."""
        assert editor.get_shape("unknown") is None

    def test_get_after_remove_returns_none(self, editor):
        """get_shape() returns None after the shape is removed."""
        p = Point(0, 0)
        editor.add_shape(p)
        editor.remove_shape(p.id)
        assert editor.get_shape(p.id) is None


# ---------------------------------------------------------------------------
# list_shapes
# ---------------------------------------------------------------------------

class TestListShapes:
    """Tests for VectorEditor.list_shapes()."""

    def test_contains_all_added_shapes(self, editor, all_shapes):
        """list_shapes() contains every added shape."""
        for shape in all_shapes:
            editor.add_shape(shape)
        listed = editor.list_shapes()
        for shape in all_shapes:
            assert shape in listed

    def test_returns_copy(self, editor):
        """Mutating the returned list does not affect the editor."""
        editor.add_shape(Point(0, 0))
        listed = editor.list_shapes()
        listed.clear()
        assert editor.count() == 1


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

class TestClear:
    """Tests for VectorEditor.clear()."""

    def test_clear_empties_editor(self, editor, all_shapes):
        """clear() removes all shapes."""
        for shape in all_shapes:
            editor.add_shape(shape)
        editor.clear()
        assert editor.count() == 0

    def test_clear_returns_removed_count(self, editor, all_shapes):
        """clear() returns the number of shapes removed."""
        for shape in all_shapes:
            editor.add_shape(shape)
        removed = editor.clear()
        assert removed == len(all_shapes)

    def test_clear_on_empty_editor(self, editor):
        """clear() on an empty editor returns 0 and does not raise."""
        assert editor.clear() == 0


# ---------------------------------------------------------------------------
# Mixed workflow
# ---------------------------------------------------------------------------

class TestMixedWorkflow:
    """Integration-style tests combining multiple operations."""

    def test_add_remove_add_cycle(self, editor):
        """Shapes can be added again after the editor is cleared."""
        p = Point(1, 1)
        editor.add_shape(p)
        editor.clear()
        p2 = Point(2, 2)
        editor.add_shape(p2)
        assert editor.count() == 1
        assert editor.get_shape(p2.id) is p2

    def test_remove_same_id_twice(self, editor):
        """Removing an ID twice returns True then False."""
        p = Point(0, 0)
        editor.add_shape(p)
        assert editor.remove_shape(p.id) is True
        assert editor.remove_shape(p.id) is False
