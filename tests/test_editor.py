"""Unit tests for VectorEditor.

Coverage:
- Initial state (empty)
- add_shape: returns correct ID, increments count, stores object
- remove_shape: returns True on success, False for unknown ID, decrements count
- get_shape: returns the correct object or None
- list_shapes: returns all shapes in insertion order
- count: reflects current number of shapes
- clear: removes all shapes, returns the count removed
- save / load: JSON round-trip preserves all shapes and their IDs
- load: error handling for missing file and invalid JSON
- Mixed workflow: add several shapes, delete one, verify the rest remain
"""

import json
import pytest

from vector_editor.editor import VectorEditor
from vector_editor.shapes import Circle, Oval, Point, Rectangle, Segment, Square


@pytest.fixture
def editor():
    """Fresh VectorEditor instance for each test."""
    return VectorEditor()


@pytest.fixture
def all_shapes():
    """One instance of each shape type."""
    return [
        Point(0, 0), Segment(0, 0, 1, 1),
        Circle(0, 0, 5), Square(1, 1, 3),
        Rectangle(0, 0, 4, 2), Oval(0, 0, 3, 2),
    ]


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

class TestInitialState:
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
        """All six shape types can be added."""
        for shape in all_shapes:
            editor.add_shape(shape)
        assert editor.count() == len(all_shapes)


# ---------------------------------------------------------------------------
# remove_shape
# ---------------------------------------------------------------------------

class TestRemoveShape:
    def test_remove_existing_returns_true(self, editor):
        p = Point(0, 0)
        editor.add_shape(p)
        assert editor.remove_shape(p.id) is True

    def test_remove_existing_decrements_count(self, editor):
        p = Point(0, 0)
        editor.add_shape(p)
        editor.remove_shape(p.id)
        assert editor.count() == 0

    def test_remove_nonexistent_returns_false(self, editor):
        assert editor.remove_shape("does-not-exist") is False

    def test_remove_does_not_affect_other_shapes(self, editor):
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
    def test_get_existing_returns_object(self, editor):
        p = Point(3, 4)
        editor.add_shape(p)
        assert editor.get_shape(p.id) is p

    def test_get_nonexistent_returns_none(self, editor):
        assert editor.get_shape("unknown") is None

    def test_get_after_remove_returns_none(self, editor):
        p = Point(0, 0)
        editor.add_shape(p)
        editor.remove_shape(p.id)
        assert editor.get_shape(p.id) is None


# ---------------------------------------------------------------------------
# list_shapes
# ---------------------------------------------------------------------------

class TestListShapes:
    def test_contains_all_added_shapes(self, editor, all_shapes):
        for shape in all_shapes:
            editor.add_shape(shape)
        listed = editor.list_shapes()
        for shape in all_shapes:
            assert shape in listed

    def test_returns_copy(self, editor):
        """Mutating the returned list does not affect the editor."""
        editor.add_shape(Point(0, 0))
        editor.list_shapes().clear()
        assert editor.count() == 1


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_clear_empties_editor(self, editor, all_shapes):
        for shape in all_shapes:
            editor.add_shape(shape)
        editor.clear()
        assert editor.count() == 0

    def test_clear_returns_removed_count(self, editor, all_shapes):
        for shape in all_shapes:
            editor.add_shape(shape)
        assert editor.clear() == len(all_shapes)

    def test_clear_on_empty_editor(self, editor):
        assert editor.clear() == 0


# ---------------------------------------------------------------------------
# save / load
# ---------------------------------------------------------------------------

class TestSaveLoad:
    def test_save_returns_shape_count(self, editor, all_shapes, tmp_path):
        """save() returns the number of shapes written."""
        for shape in all_shapes:
            editor.add_shape(shape)
        n = editor.save(str(tmp_path / "shapes.json"))
        assert n == len(all_shapes)

    def test_load_returns_shape_count(self, editor, all_shapes, tmp_path):
        """load() returns the number of shapes read."""
        for shape in all_shapes:
            editor.add_shape(shape)
        path = str(tmp_path / "shapes.json")
        editor.save(path)

        editor2 = VectorEditor()
        assert editor2.load(path) == len(all_shapes)

    def test_round_trip_preserves_ids(self, editor, all_shapes, tmp_path):
        """Saved and loaded shapes have identical IDs."""
        for shape in all_shapes:
            editor.add_shape(shape)
        path = str(tmp_path / "shapes.json")
        editor.save(path)

        editor2 = VectorEditor()
        editor2.load(path)

        original_ids = {s.id for s in all_shapes}
        loaded_ids = {s.id for s in editor2.list_shapes()}
        assert original_ids == loaded_ids

    def test_round_trip_preserves_shape_types(self, editor, all_shapes, tmp_path):
        """Loaded shapes have the same type as the originals."""
        for shape in all_shapes:
            editor.add_shape(shape)
        path = str(tmp_path / "shapes.json")
        editor.save(path)

        editor2 = VectorEditor()
        editor2.load(path)

        original_types = sorted(s.shape_type for s in all_shapes)
        loaded_types = sorted(s.shape_type for s in editor2.list_shapes())
        assert original_types == loaded_types

    def test_load_replaces_existing_shapes(self, editor, tmp_path):
        """load() clears existing shapes before loading."""
        editor.add_shape(Point(0, 0))
        editor.add_shape(Circle(0, 0, 5))
        path = str(tmp_path / "shapes.json")
        editor.save(path)

        editor.add_shape(Square(1, 1, 3))  # extra shape not in file
        editor.load(path)
        assert editor.count() == 2

    def test_load_file_not_found(self, editor):
        """load() raises FileNotFoundError for a missing file."""
        with pytest.raises(FileNotFoundError):
            editor.load("/nonexistent/path/shapes.json")

    def test_load_invalid_json(self, editor, tmp_path):
        """load() raises ValueError for a file with invalid JSON."""
        bad = tmp_path / "bad.json"
        bad.write_text("not json at all", encoding="utf-8")
        with pytest.raises(ValueError):
            editor.load(str(bad))

    def test_load_non_array_json(self, editor, tmp_path):
        """load() raises ValueError if JSON root is not an array."""
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"type": "point"}), encoding="utf-8")
        with pytest.raises(ValueError):
            editor.load(str(bad))

    def test_save_creates_valid_json_file(self, editor, tmp_path):
        """The file written by save() is valid JSON."""
        editor.add_shape(Rectangle(0, 0, 5, 3))
        path = tmp_path / "shapes.json"
        editor.save(str(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data, list)
        assert data[0]["type"] == "rectangle"


# ---------------------------------------------------------------------------
# Mixed workflow
# ---------------------------------------------------------------------------

class TestMixedWorkflow:
    def test_add_remove_add_cycle(self, editor):
        p = Point(1, 1)
        editor.add_shape(p)
        editor.clear()
        p2 = Point(2, 2)
        editor.add_shape(p2)
        assert editor.count() == 1
        assert editor.get_shape(p2.id) is p2

    def test_remove_same_id_twice(self, editor):
        p = Point(0, 0)
        editor.add_shape(p)
        assert editor.remove_shape(p.id) is True
        assert editor.remove_shape(p.id) is False
