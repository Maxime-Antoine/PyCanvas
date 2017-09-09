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


def test_CreateCanvasCommand_execute():
    width, height = 100, 50
    command = CreateCanvasCommand
    def callback(result):
        assert isinstance(result, Canvas)
        assert result.width == width
        assert result.height == height
    command.execute(width, height, callback)


def test_DrawLineCanvas_execute():
    canvas = Mock(spec=Canvas)
    command = DrawLineCommand()
    line = Line(Point(1, 1), Point(1, 10))
    command.execute(canvas, line)
    canvas.draw_line.assert_called_once_with(line)


def test_DrawRectangleCanvas_execute():
    canvas = Mock(spec=Canvas)
    command = DrawRectangleCommand()
    rectangle = Rectangle(Point(1, 1), Point(10, 10))
    command.execute(canvas, rectangle)
    canvas.draw_rectangle.assert_called_once_with(rectangle)


def test_BucketFillCommand_execute():
    canvas = Mock(spec=Canvas)
    command = BucketFillCommand()
    target_point = Point(42, 69)
    command.execute(canvas, target_point)
    canvas.bucket_fill.assert_called_once_with(target_point)


def test_DeleteCommand_execute():
    canvas = Mock(spec=Canvas)
    command = DeleteCommand()
    target_point = Point(42, 69)
    command.execute(canvas, target_point)
    canvas.delete.assert_called_once_with(target_point)


def test_UndoCommand_execute():
    canvas = Mock(spec=Canvas)
    command = UndoCommand()
    command.execute(canvas)
    canvas.undo.assert_called_once()
