import pytest
from unittest.mock import Mock
from canvas import (
    Canvas,
    Point,
    Line,
    Rectangle
)
from commands import (
    ExitCommand,
    CreateCanvasCommand,
    DrawLineCommand,
    DrawRectangleCommand,
    BucketFillCommand,
    DeleteCommand,
    UndoCommand
)

def test_exit_command_execute():
    command = ExitCommand()
    with pytest.raises(SystemExit):
        command.execute()


def test_create_canvas_command_execute():
    width, height = 100, 50
    def callback(result):
        assert isinstance(result, Canvas)
        assert result.width == width
        assert result.height == height
    command = CreateCanvasCommand(callback)
    command.execute(width, height)


def test_draw_line_command_execute():
    canvas = Mock(spec=Canvas)
    command = DrawLineCommand(lambda: canvas)
    x1, y1, x2, y2 = 1, 1, 1, 10
    line = Line(Point(x1, y1), Point(x2, y2))
    command.execute([x1, y1, x2, y2])
    canvas.draw_line.assert_called_once_with(line)


def test_draw_line_command_execute_with_incorrect_nb_args():
    canvas = Mock(spec=Canvas)
    command = DrawLineCommand(lambda: canvas)
    with pytest.raises(ValueError) as ex:
        command.execute([1, 1, 1])
    assert str(ex.value) == "4 arguments expected (x1, y1, x2, y2)"


def test_draw_rectangle_command_execute():
    canvas = Mock(spec=Canvas)
    command = DrawRectangleCommand(lambda: canvas)
    x1, y1, x2, y2 = 1, 1, 10, 10
    rectangle = Rectangle(Point(x1, y1), Point(x2, y2))
    command.execute([x1, y1, x2, y2])
    canvas.draw_rectangle.assert_called_once_with(rectangle)


def test_draw_rectangle_command_execute_with_incorrect_nb_args():
    canvas = Mock(spec=Canvas)
    command = DrawRectangleCommand(lambda: canvas)
    with pytest.raises(ValueError) as ex:
        command.execute([1, 1, 1])
    assert str(ex.value) == "4 arguments expected (x1, y1, x2, y2)"


def test_bucket_fill_command_execute():
    canvas = Mock(spec=Canvas)
    command = BucketFillCommand(lambda: canvas)
    x1, y1 = 42, 69
    target_point = Point(x1, y1)
    command.execute((x1, y1))
    canvas.bucket_fill.assert_called_once_with(target_point)


def test_bucket_fill_command_execute_with_incorrect_nb_args():
    canvas = Mock(spec=Canvas)
    command = BucketFillCommand(lambda: canvas)
    with pytest.raises(ValueError) as ex:
        command.execute([1])
    assert str(ex.value) == "2 arguments expected (x1, y1)"


def test_delete_command_execute():
    canvas = Mock(spec=Canvas)
    command = DeleteCommand(lambda: canvas)
    x1, y1 = 42, 69
    target_point = Point(x1, y1)
    command.execute([x1, y1])
    canvas.delete.assert_called_once_with(target_point)


def test_delete_command_execute_with_incorrect_nb_args():
    canvas = Mock(spec=Canvas)
    command = DeleteCommand(lambda: canvas)
    with pytest.raises(ValueError) as ex:
        command.execute([1])
    assert str(ex.value) == "2 arguments expected (x1, y1)"


def test_undo_command_execute():
    canvas = Mock(spec=Canvas)
    command = UndoCommand(lambda: canvas)
    command.execute()
    canvas.undo.assert_called_once()
