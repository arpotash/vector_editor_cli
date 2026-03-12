"""Vector editor — manages a collection of shapes."""

from typing import Dict, List, Optional

from .shapes import Shape


class VectorEditor:
    """Manages a collection of vector shapes.

    Provides CRUD operations: add, remove, get, list, and clear shapes.
    Shapes are stored by their unique ID.
    """

    def __init__(self):
        self._shapes: Dict[str, Shape] = {}

    def add_shape(self, shape: Shape) -> str:
        """Add a shape to the editor.

        Args:
            shape: Any Shape instance (Point, Segment, Circle, Square).

        Returns:
            The ID assigned to the shape.
        """
        self._shapes[shape.id] = shape
        return shape.id

    def remove_shape(self, shape_id: str) -> bool:
        """Remove a shape by its ID.

        Args:
            shape_id: The ID of the shape to remove.

        Returns:
            True if the shape was found and removed, False otherwise.
        """
        if shape_id in self._shapes:
            del self._shapes[shape_id]
            return True
        return False

    def get_shape(self, shape_id: str) -> Optional[Shape]:
        """Retrieve a shape by its ID.

        Args:
            shape_id: The ID of the shape to retrieve.

        Returns:
            The Shape instance, or None if not found.
        """
        return self._shapes.get(shape_id)

    def list_shapes(self) -> List[Shape]:
        """Return all shapes in the editor.

        Returns:
            List of all Shape instances (insertion order preserved).
        """
        return list(self._shapes.values())

    def count(self) -> int:
        """Return the total number of shapes in the editor."""
        return len(self._shapes)

    def clear(self) -> int:
        """Remove all shapes from the editor.

        Returns:
            The number of shapes that were removed.
        """
        n = len(self._shapes)
        self._shapes.clear()
        return n
