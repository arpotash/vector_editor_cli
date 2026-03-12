# Vector Editor CLI

Простой векторный редактор с интерфейсом командной строки. Поддерживает шесть типов фигур, сохранение/загрузку коллекции в JSON и полный набор unit-тестов.

## Структура проекта

```
test_project/
├── vector_editor/
│   ├── __init__.py      # Экспорт публичного API
│   ├── shapes.py        # Классы фигур + сериализация
│   ├── editor.py        # VectorEditor — управление коллекцией
│   └── cli.py           # Интерактивный CLI
├── tests/
│   ├── test_shapes.py   # Тесты фигур (+ round-trip сериализации)
│   └── test_editor.py   # Тесты редактора (+ save/load)
├── main.py              # Точка входа
└── README.md
```

## Запуск

```bash
python3 main.py
```

## Зависимости

Стандартная библиотека Python 3.10+. Для тестов — `pytest`:

```bash
pip install pytest
pytest tests/
```

---

## Команды CLI

```
┌─────────────────────────────────────────────────────────────┐
│                    VECTOR EDITOR  —  HELP                   │
├──────────────────────────────┬──────────────────────────────┤
│  SHAPE COMMANDS              │  FILE COMMANDS               │
│  create point   <x> <y>      │  save <file>                 │
│  create segment <x1 y1 x2 y2>│  load <file>                 │
│  create circle  <cx cy r>    ├──────────────────────────────┤
│  create square  <x y side>   │  LIST COMMANDS               │
│  create rect    <x y w h>    │  list                        │
│  create oval    <cx cy rx ry>│  clear                       │
│  delete <id>                 │  help  /  exit               │
└──────────────────────────────┴──────────────────────────────┘
```

### Пример сессии

```
> create point 0 0
Created [a1b2c3d4] Point(x=0.0, y=0.0)
> create rect 10 20 100 50
Created [e5f6g7h8] Rectangle(origin=(10.0, 20.0), width=100.0, height=50.0, area=5000.00)
> create oval 0 0 30 15
Created [i9j0k1l2] Oval(center=(0.0, 0.0), rx=30.0, ry=15.0, area=1413.72)
> list
Total: 3 shape(s)
  [a1b2c3d4]  Point(x=0.0, y=0.0)
  [e5f6g7h8]  Rectangle(origin=(10.0, 20.0), width=100.0, height=50.0, area=5000.00)
  [i9j0k1l2]  Oval(center=(0.0, 0.0), rx=30.0, ry=15.0, area=1413.72)
> save project.json
Saved 3 shape(s) to 'project.json'.
> clear
Removed 3 shape(s).
> load project.json
Loaded 3 shape(s) from 'project.json'.
> exit
Goodbye!
```

---

## Описание модулей

### `vector_editor/shapes.py`

Иерархия классов фигур + функция десериализации.

#### `Shape` (ABC)

Абстрактный базовый класс. При создании автоматически генерирует уникальный `id` (8 символов UUID4).

| Метод / свойство | Описание |
|-----------------|----------|
| `id: str` | Уникальный идентификатор |
| `shape_type: str` *(abstract)* | Тип фигуры |
| `describe() -> str` *(abstract)* | Человекочитаемое описание |
| `to_dict() -> dict` *(abstract)* | Сериализация в JSON-совместимый dict |

---

#### `Point(x, y)`

| Метод | Описание |
|-------|----------|
| `describe()` | `"Point(x=…, y=…)"` |
| `distance_to(other)` | Евклидово расстояние до другой точки |
| `to_dict()` | `{"type": "point", "id": …, "x": …, "y": …}` |

---

#### `Segment(x1, y1, x2, y2)`

| Метод | Описание |
|-------|----------|
| `length()` | Длина отрезка |
| `to_dict()` | `{"type": "segment", "id": …, "x1": …, "y1": …, "x2": …, "y2": …}` |

---

#### `Circle(cx, cy, radius)`

Выбрасывает `ValueError` при `radius <= 0`.

| Метод | Описание |
|-------|----------|
| `area()` | Площадь (`π r²`) |
| `perimeter()` | Длина окружности (`2 π r`) |
| `to_dict()` | `{"type": "circle", "id": …, "cx": …, "cy": …, "radius": …}` |

---

#### `Square(x, y, side)`

Выбрасывает `ValueError` при `side <= 0`.

| Метод | Описание |
|-------|----------|
| `area()` | `side²` |
| `perimeter()` | `4 × side` |
| `to_dict()` | `{"type": "square", "id": …, "x": …, "y": …, "side": …}` |

---

#### `Rectangle(x, y, width, height)` *(новая)*

Выбрасывает `ValueError` при `width <= 0` или `height <= 0`.

| Метод | Описание |
|-------|----------|
| `area()` | `width × height` |
| `perimeter()` | `2 × (width + height)` |
| `to_dict()` | `{"type": "rectangle", "id": …, "x": …, "y": …, "width": …, "height": …}` |

---

#### `Oval(cx, cy, rx, ry)` *(новая)*

Эллипс с центром и двумя полуосями. Выбрасывает `ValueError` при `rx <= 0` или `ry <= 0`.

| Метод | Описание |
|-------|----------|
| `area()` | `π × rx × ry` |
| `perimeter()` | Приближение Рамануджана |
| `to_dict()` | `{"type": "oval", "id": …, "cx": …, "cy": …, "rx": …, "ry": …}` |

---

#### `shape_from_dict(data: dict) -> Shape`

Восстанавливает фигуру из dict (результат `to_dict()`), сохраняя оригинальный ID. Используется при загрузке из файла.

---

### `vector_editor/editor.py`

#### `VectorEditor`

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `add_shape(shape)` | `str` (ID) | Добавить фигуру |
| `remove_shape(id)` | `bool` | Удалить фигуру |
| `get_shape(id)` | `Shape \| None` | Получить по ID |
| `list_shapes()` | `list[Shape]` | Все фигуры |
| `count()` | `int` | Количество фигур |
| `clear()` | `int` | Удалить всё |
| `save(filepath)` | `int` | Сохранить в JSON-файл |
| `load(filepath)` | `int` | Загрузить из JSON-файла (заменяет текущую коллекцию) |

---

### `vector_editor/cli.py`

#### `CLI`

| Метод | Описание |
|-------|----------|
| `run()` | Запустить интерактивный REPL |
| `_cmd_create(args)` | `create <type> [params]` |
| `_cmd_delete(args)` | `delete <id>` |
| `_cmd_list()` | `list` |
| `_cmd_clear()` | `clear` |
| `_cmd_save(args)` | `save <file>` |
| `_cmd_load(args)` | `load <file>` |
| `_build_shape(type, params)` | Фабрика фигур |

---

## Тесты

### `tests/test_shapes.py` — 55 тестов

| Тест-класс | Что проверяет |
|------------|--------------|
| `TestPoint` | Создание, тип, describe, ID, distance_to, негативные координаты, строковые аргументы, round-trip сериализация |
| `TestSegment` | Создание, тип, length (3-4-5, горизонталь, вертикаль, нуль), round-trip |
| `TestCircle` | Создание, тип, area, perimeter, ValueError при r≤0, round-trip |
| `TestSquare` | Создание, тип, area, perimeter, ValueError при side≤0, round-trip |
| `TestRectangle` | Создание, тип, area, perimeter, граничный случай (квадрат), ValueError, round-trip |
| `TestOval` | Создание, тип, area, perimeter (приближение), равные полуоси = круг, ValueError, round-trip |
| `TestShapeFromDict` | ValueError для неизвестного типа |
| `TestCrossTypeIds` | Уникальность ID среди всех шести типов |

### `tests/test_editor.py` — 34 теста

| Тест-класс | Что проверяет |
|------------|--------------|
| `TestInitialState` | count=0, list=[] |
| `TestAddShape` | Возврат ID, прирост count, все типы фигур |
| `TestRemoveShape` | True/False, декремент, сохранность других фигур |
| `TestGetShape` | Корректный объект, None для неизвестного и удалённого |
| `TestListShapes` | Все фигуры присутствуют, возврат копии |
| `TestClear` | Очистка, возврат количества, пустой редактор |
| `TestSaveLoad` | Возврат количества, round-trip ID и типов, замена текущей коллекции, FileNotFoundError, ValueError для битого JSON и не-массива, валидность итогового файла |
| `TestMixedWorkflow` | add→clear→add, двойное удаление |
