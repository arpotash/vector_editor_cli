# Vector Editor CLI

Простой векторный редактор с интерфейсом командной строки. Поддерживает четыре типа фигур: точка, отрезок, круг, квадрат.

## Структура проекта

```
test_project/
├── vector_editor/
│   ├── __init__.py      # Экспорт публичного API
│   ├── shapes.py        # Классы фигур
│   ├── editor.py        # VectorEditor — управление коллекцией фигур
│   └── cli.py           # Интерактивный CLI
├── tests/
│   ├── test_shapes.py   # Тесты фигур
│   └── test_editor.py   # Тесты редактора
├── main.py              # Точка входа
└── README.md
```

## Запуск

```bash
python main.py
```

## Зависимости

Стандартная библиотека Python 3.9+. Для тестов нужен `pytest`:

```bash
pip install pytest
pytest tests/
```

---

## Команды CLI

| Команда | Описание |
|---------|----------|
| `create point <x> <y>` | Создать точку |
| `create segment <x1> <y1> <x2> <y2>` | Создать отрезок |
| `create circle <cx> <cy> <radius>` | Создать круг |
| `create square <x> <y> <side>` | Создать квадрат |
| `delete <id>` | Удалить фигуру по ID |
| `list` | Показать все фигуры |
| `clear` | Удалить все фигуры |
| `help` | Помощь |
| `exit` | Выйти |

### Пример сессии

```
Vector Editor  |  type 'help' for commands, 'exit' to quit.
> create point 0 0
Created [a1b2c3d4] Point(x=0.0, y=0.0)
> create circle 5 5 10
Created [e5f6g7h8] Circle(center=(5.0, 5.0), radius=10.0, area=314.16)
> create square 1 1 4
Created [i9j0k1l2] Square(origin=(1.0, 1.0), side=4.0, area=16.00)
> list
Total: 3 shape(s)
  [a1b2c3d4] Point(x=0.0, y=0.0)
  [e5f6g7h8] Circle(center=(5.0, 5.0), radius=10.0, area=314.16)
  [i9j0k1l2] Square(origin=(1.0, 1.0), side=4.0, area=16.00)
> delete a1b2c3d4
Deleted shape [a1b2c3d4].
> exit
Goodbye!
```

---

## Описание модулей

### `vector_editor/shapes.py`

Иерархия классов фигур.

#### `Shape` (ABC)

Абстрактный базовый класс. При создании автоматически генерирует уникальный `id` (8 символов UUID4).

| Метод / свойство | Описание |
|-----------------|----------|
| `id: str` | Уникальный идентификатор |
| `shape_type: str` *(abstract)* | Тип фигуры (`'point'`, `'circle'`, …) |
| `describe() -> str` *(abstract)* | Человекочитаемое описание |

---

#### `Point(x, y)`

Точка в 2D-пространстве.

| Метод | Описание |
|-------|----------|
| `describe()` | `"Point(x=…, y=…)"` |
| `distance_to(other: Point) -> float` | Евклидово расстояние до другой точки |

---

#### `Segment(x1, y1, x2, y2)`

Отрезок между двумя точками.

| Метод | Описание |
|-------|----------|
| `describe()` | Начало, конец и длина отрезка |
| `length() -> float` | Длина отрезка |

---

#### `Circle(cx, cy, radius)`

Круг с центром и радиусом. Выбрасывает `ValueError` при `radius <= 0`.

| Метод | Описание |
|-------|----------|
| `describe()` | Центр, радиус и площадь |
| `area() -> float` | Площадь (`π r²`) |
| `perimeter() -> float` | Длина окружности (`2 π r`) |

---

#### `Square(x, y, side)`

Квадрат с левым верхним углом в `(x, y)`. Выбрасывает `ValueError` при `side <= 0`.

| Метод | Описание |
|-------|----------|
| `describe()` | Начало координат, сторона и площадь |
| `area() -> float` | Площадь (`side²`) |
| `perimeter() -> float` | Периметр (`4 × side`) |

---

### `vector_editor/editor.py`

#### `VectorEditor`

Коллекция фигур, хранящихся в `dict` по ID.

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `add_shape(shape)` | `str` (ID) | Добавить фигуру |
| `remove_shape(id)` | `bool` | Удалить фигуру; `False` если не найдена |
| `get_shape(id)` | `Shape \| None` | Получить фигуру по ID |
| `list_shapes()` | `list[Shape]` | Все фигуры в порядке добавления |
| `count()` | `int` | Количество фигур |
| `clear()` | `int` | Удалить всё; вернуть количество удалённых |

---

### `vector_editor/cli.py`

#### `CLI`

Обёртка над `VectorEditor` с REPL-циклом.

| Метод | Описание |
|-------|----------|
| `run()` | Запустить интерактивный цикл ввода |
| `_cmd_create(args)` | Обработать `create` — разобрать тип и параметры |
| `_cmd_delete(args)` | Обработать `delete <id>` |
| `_cmd_list()` | Вывести все фигуры |
| `_cmd_clear()` | Очистить редактор |
| `_build_shape(type, params)` | Фабрика фигур; выбрасывает `ValueError` при неверных данных |

---

## Тесты

### `tests/test_shapes.py`

| Тест-класс | Что проверяет |
|------------|--------------|
| `TestPoint` | Создание, `shape_type`, `describe`, уникальность ID, `distance_to`, отрицательные координаты, приведение строк к float |
| `TestSegment` | Создание, `shape_type`, `length` (тройка Пифагора, горизонталь, вертикаль, нуль) |
| `TestCircle` | Создание, `shape_type`, `area`, `perimeter`, `ValueError` при радиусе 0 и отрицательном |
| `TestSquare` | Создание, `shape_type`, `area`, `perimeter`, `ValueError` при стороне 0 и отрицательной |
| `TestCrossTypeIds` | ID уникальны среди всех четырёх типов |

### `tests/test_editor.py`

| Тест-класс | Что проверяет |
|------------|--------------|
| `TestInitialState` | `count() == 0`, `list_shapes() == []` |
| `TestAddShape` | Возврат ID, прирост `count`, добавление всех типов |
| `TestRemoveShape` | `True` при удалении, `False` при несуществующем ID, сохранность остальных фигур |
| `TestGetShape` | Возврат корректного объекта, `None` для неизвестного ID и после удаления |
| `TestListShapes` | Все фигуры присутствуют, изменение результата не меняет редактор |
| `TestClear` | Опустошение коллекции, возврат количества удалённых, работа на пустом редакторе |
| `TestMixedWorkflow` | Цикл add → clear → add; двойное удаление одного ID |
