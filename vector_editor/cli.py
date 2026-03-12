"""Command-line interface for the vector editor."""

from .editor import VectorEditor
from .shapes import Circle, Point, Segment, Square

HELP_TEXT = """\
Commands:
  create point   <x> <y>                  Create a point
  create segment <x1> <y1> <x2> <y2>     Create a line segment
  create circle  <cx> <cy> <radius>       Create a circle
  create square  <x> <y> <side>           Create a square
  delete <id>                             Delete shape by ID
  list                                    Show all shapes
  clear                                   Remove all shapes
  help                                    Show this help
  exit                                    Quit
"""

_SHAPE_USAGE = {
    "point":   "create point <x> <y>",
    "segment": "create segment <x1> <y1> <x2> <y2>",
    "circle":  "create circle <cx> <cy> <radius>",
    "square":  "create square <x> <y> <side>",
}


class CLI:
    """Interactive CLI loop for the vector editor."""

    def __init__(self):
        self.editor = VectorEditor()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the interactive REPL."""
        print("Vector Editor  |  type 'help' for commands, 'exit' to quit.")
        while True:
            try:
                raw = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break

            if not raw:
                continue

            parts = raw.split()
            cmd, args = parts[0].lower(), parts[1:]

            match cmd:
                case "exit":
                    print("Goodbye!")
                    break
                case "help":
                    print(HELP_TEXT)
                case "list":
                    self._cmd_list()
                case "clear":
                    self._cmd_clear()
                case "delete":
                    self._cmd_delete(args)
                case "create":
                    self._cmd_create(args)
                case _:
                    print(f"Unknown command '{cmd}'. Type 'help' to see available commands.")

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    def _cmd_create(self, args: list) -> None:
        if not args:
            print("Usage: create <point|segment|circle|square> [params...]")
            return

        shape_type = args[0].lower()
        params = args[1:]

        try:
            shape = self._build_shape(shape_type, params)
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")
            return

        shape_id = self.editor.add_shape(shape)
        print(f"Created [{shape_id}] {shape.describe()}")

    def _cmd_delete(self, args: list) -> None:
        if not args:
            print("Usage: delete <id>")
            return

        shape_id = args[0]
        if self.editor.remove_shape(shape_id):
            print(f"Deleted shape [{shape_id}].")
        else:
            print(f"Shape with id '{shape_id}' not found.")

    def _cmd_list(self) -> None:
        shapes = self.editor.list_shapes()
        if not shapes:
            print("No shapes. Use 'create' to add one.")
            return
        print(f"Total: {len(shapes)} shape(s)")
        for shape in shapes:
            print(f"  [{shape.id}] {shape.describe()}")

    def _cmd_clear(self) -> None:
        removed = self.editor.clear()
        print(f"Removed {removed} shape(s).")

    # ------------------------------------------------------------------
    # Shape factory
    # ------------------------------------------------------------------

    def _build_shape(self, shape_type: str, params: list):
        match shape_type:
            case "point":
                self._require_params(params, 2, _SHAPE_USAGE["point"])
                return Point(params[0], params[1])
            case "segment":
                self._require_params(params, 4, _SHAPE_USAGE["segment"])
                return Segment(*map(float, params[:4]))
            case "circle":
                self._require_params(params, 3, _SHAPE_USAGE["circle"])
                return Circle(*map(float, params[:3]))
            case "square":
                self._require_params(params, 3, _SHAPE_USAGE["square"])
                return Square(*map(float, params[:3]))
            case _:
                known = ", ".join(_SHAPE_USAGE.keys())
                raise ValueError(f"Unknown shape type '{shape_type}'. Known types: {known}")

    @staticmethod
    def _require_params(params: list, expected: int, usage: str) -> None:
        if len(params) < expected:
            raise ValueError(f"Not enough arguments. Usage: {usage}")
        try:
            list(map(float, params[:expected]))
        except ValueError:
            raise ValueError(f"All coordinates must be numbers. Usage: {usage}")
