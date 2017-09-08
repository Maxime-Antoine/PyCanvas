import pytest
from canvas import (
    Canvas,
    CanvasCellContentType,
    OutOfCanvasBoundError,
    Point
)

def test_Canvas_creation_fails_whith_incorrect_params():
    with pytest.raises(TypeError):
        Canvas("width", 50)
    with pytest.raises(TypeError):
        Canvas(50, [50])


def test_Canvas_initialize():
    width, height = 50, 50
    canvas = Canvas(width, height)
    assert canvas.width == width and canvas.height == height
    for i in range(width):
        for j in range(width):
            assert canvas.cells[i][j] == (CanvasCellContentType.Empty, ' ')


def test_Canvas_draw_point():
    width, height = 50, 50
    canvas = Canvas(width, height)
    x, y = 2, 3
    point = Point(x, y)
    canvas.draw_point(point)
    assert canvas.cells[x][y] == (CanvasCellContentType.Line, 'x')


def test_Canvas_draw_point_when_point_is_out_of_bounds():
    width, height = 50, 50
    canvas = Canvas(width, height)
    x, y = 300, 500
    point = Point(x, y)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.draw_point(point)


def test_Point_initialize():
    x, y = 1, 2
    point = Point(x, y)
    assert point.x == x and point.y == y

def test_Point_creation_fails_whith_incorrect_params():
    with pytest.raises(ValueError):
        Point("hi", 5)
    with pytest.raises(TypeError):
        Point(1, ValueError())
    with pytest.raises(ValueError):
        Point(-1, 5)
