"""Vector editor — manages a collection of shapes."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from .shapes import Shape, shape_from_dict


class VectorEditor:
    """Manages a collection of vector shapes.

    Provides CRUD operations: add, remove, get, list, and clear shapes.
    Supports persistence via save() and load() (JSON format).
    Shapes are stored by their unique ID.
    """

    def __init__(self):
        self._shapes: Dict[str, Shape] = {}

    def add_shape(self, shape: Shape) -> str:
        """Add a shape to the editor.

        Args:
            shape: Any Shape instance.

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
            True if found and removed, False otherwise.
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
        """Return all shapes in insertion order."""
        return list(self._shapes.values())

    def count(self) -> int:
        """Return the total number of shapes in the editor."""
        return len(self._shapes)

    def clear(self) -> int:
        """Remove all shapes.

        Returns:
            The number of shapes removed.
        """
        n = len(self._shapes)
        self._shapes.clear()
        return n

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, filepath: str) -> int:
        """Save all shapes to a JSON file.

        Args:
            filepath: Path to the output file (created or overwritten).

        Returns:
            Number of shapes saved.

        Raises:
            OSError: If the file cannot be written.
        """
        data = [shape.to_dict() for shape in self._shapes.values()]
        Path(filepath).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return len(data)

    def load(self, filepath: str) -> int:
        """Load shapes from a JSON file, replacing the current collection.

        Args:
            filepath: Path to a JSON file previously created by save().

        Returns:
            Number of shapes loaded.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file contains invalid data.
            OSError: If the file cannot be read.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in '{filepath}': {exc}") from exc

        if not isinstance(raw, list):
            raise ValueError(f"Expected a JSON array in '{filepath}', got {type(raw).__name__}")

        self._shapes.clear()
        for item in raw:
            shape = shape_from_dict(item)
            self._shapes[shape.id] = shape

        return len(self._shapes)
