import pytest
from copy import deepcopy
from canvas import (
    Canvas,
    CanvasCellContentType,
    OutOfCanvasBoundError,
    Point,
    Line,
    Rectangle
)

######## Test Canvas ########

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
    canvas._draw_point(point)
    assert canvas.cells[x][y] == (CanvasCellContentType.Line, 'x')


def test_Canvas_draw_line_horizontal():
    canvas = Canvas(50, 50)
    from_point = Point(3, 3)
    to_point = Point(3, 35)
    line = Line(from_point, to_point)
    canvas.draw_line(line)
    for point in line.get_points():
        assert canvas.cells[point.x][point.y] == (CanvasCellContentType.Line, 'x')


def test_Canvas_draw_line_vertical():
    canvas = Canvas(50, 50)
    from_point = Point(3, 3)
    to_point = Point(3, 35)
    line = Line(from_point, to_point)
    canvas.draw_line(line)
    for point in line.get_points():
        assert canvas.cells[point.x][point.y] == (CanvasCellContentType.Line, 'x')


def test_Canvas_draw_line_fails_when_a_point_is_out_of_bounds():
    canvas = Canvas(50, 50)
    from_point1 = Point(3, 3)
    to_point1 = Point(3, 350)
    line1 = Line(from_point1, to_point1)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.draw_line(line1)

    from_point2 = Point(3, 300)
    to_point2 = Point(3, 35)
    line2 = Line(from_point2, to_point2)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.draw_line(line2)


def test_Rectangle_draw_rectangle():
    canvas = Canvas(50, 50)
    top_left = Point(3, 3)
    bottom_right = Point(10, 10)
    rectangle = Rectangle(top_left, bottom_right)
    canvas.draw_rectangle(rectangle)
    for line in rectangle.get_lines():
        for point in line.get_points():
            assert canvas.cells[point.x][point.y] == (CanvasCellContentType.Line, 'x')


def test_Rectangle_draw_rectangle_fails_when_a_point_is_out_of_bounds():
    canvas = Canvas(50, 50)
    top_left1 = Point(3, 350)
    bottom_right1 = Point(10, 10)
    rectangle1 = Rectangle(top_left1, bottom_right1)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.draw_rectangle(rectangle1)

    top_left2 = Point(3, 3)
    bottom_right2 = Point(10, 100)
    rectangle2 = Rectangle(top_left2, bottom_right2)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.draw_rectangle(rectangle2)


def test_Canvas_bucket_fill_shape():
    width, height = 10, 10
    canvas = Canvas(width, height)
    line = Line(Point(0, 1), Point(9, 1))
    canvas.draw_line(line)
    canvas.bucket_fill(Point(0, 1), 'o')
    #line has been filled
    for point in line.get_points():
        assert canvas.cells[point.x][point.y] == (CanvasCellContentType.Line, 'o')
    #rest have not been filled
    for x in range(width):
        for y in range(height):
            if Point(x, y) not in line.get_points():
                assert canvas.cells[x][y] == (CanvasCellContentType.Empty, ' ')


def test_Canvas_bucket_fill_area():
    width, height = 10, 10
    canvas = Canvas(width, height)
    line = Line(Point(0, 2), Point(9, 2))
    canvas.draw_line(line)
    canvas.bucket_fill(Point(0, 0), 'o')
    #top area have been filled
    for x in range(width):
        assert (canvas.cells[x][0] == (CanvasCellContentType.Empty, 'o') and
                canvas.cells[x][1] == (CanvasCellContentType.Empty, 'o'))
        #bottom area have not been filled
        for y in range(3, height):
            assert canvas.cells[x][y] == (CanvasCellContentType.Empty, ' ')
    #line have not been filled
    for point in line.get_points():
        assert canvas.cells[point.x][point.y] == (CanvasCellContentType.Line, 'x')


def test_Canvas_bucket_fill_fails_when_target_out_of_bounds():
    canvas = Canvas(50, 50)
    target = Point(100, 25)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.bucket_fill(target, 'o')


def test_Canvas_delete_shape():
    canvas = Canvas(10, 10)
    line = Line(Point(0, 1), Point(9, 1))
    expected_cells_after_delete = deepcopy(canvas.cells)
    canvas.draw_line(line)
    canvas.delete(Point(0, 1))
    assert canvas.cells == expected_cells_after_delete


def test_Canvas_delete_colour():
    width, height = 10, 10
    canvas = Canvas(width, height)
    line = Line(Point(0, 1), Point(9, 1))
    canvas.draw_line(line)
    expected_cells_after_delete = deepcopy(canvas.cells)
    canvas.bucket_fill(Point(0, 0), 'o')
    canvas.delete(Point(0, 0))
    assert canvas.cells == expected_cells_after_delete


def test_Canvas_delete_fails_when_target_out_of_bounds():
    canvas = Canvas(50, 50)
    target = Point(100, 25)
    with pytest.raises(OutOfCanvasBoundError):
        canvas.delete(target)


######## Test Point ########

def test_Point_initialize():
    x, y = 1, 2
    point = Point(x, y)
    assert point.x == x and point.y == y


def test_Point_creation_fails_whith_incorrect_params():
    with pytest.raises(ValueError):
        Point("hi", 5)
    with pytest.raises(TypeError):
        Point(1, ValueError())


######## Test Line ########

def test_Line_initialize():
    point1 = Point(1, 1)
    point2 = Point(5, 1)
    line = Line(point1, point2)
    assert line.from_point == point1 and line.to_point == point2


def test_line_get_points_for_horizontal_line():
    from_point = Point(1, 1)
    to_point = Point(1, 5)
    expected_points = [from_point, Point(1, 2), Point(1, 3), Point(1, 4), to_point]
    line = Line(from_point, to_point)
    points = line.get_points()
    assert points == expected_points


def test_Line_get_points_for_vertical_line():
    from_point = Point(1, 1)
    to_point = Point(5, 1)
    expected_points = [from_point, Point(2, 1), Point(3, 1), Point(4, 1), to_point]
    line = Line(from_point, to_point)
    points = line.get_points()
    assert points == expected_points


######## Test Rectangle ########

def test_Rectangle_initialize():
    top_left = Point(1, 1)
    bottom_right = Point(5, 5)
    rectangle = Rectangle(top_left, bottom_right)
    assert rectangle.top_left_point == top_left and rectangle.bottom_right_point == bottom_right


def test_Rectangle_get_lines():
    top_right = Point(1, 1)
    top_left = Point(5, 1)
    bottom_left = Point(5, 5)
    bottom_right = Point(1, 5)
    rectangle = Rectangle(top_left, bottom_right)
    expected_lines = [
        Line(top_left, top_right),
        Line(top_left, bottom_left),
        Line(top_right, bottom_right),
        Line(bottom_left, bottom_right)
    ]
    lines = rectangle.get_lines()
    assert lines == expected_lines
