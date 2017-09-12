from canvas import (
    Canvas,
    Point,
    Line,
    Rectangle
)

class ExitCommand(object):

    @staticmethod
    def execute():
        raise SystemExit()


class CreateCanvasCommand(object):

    def __init__(self, callback):
        self._callback = callback

    def execute(self, width, height):
        self._callback(Canvas(width, height))


class DrawLineCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, args):
        if len(args) < 4:
            raise ValueError("4 arguments expected (x1, y1, x2, y2)")
        line = Line(Point(args[0], args[1]), Point(args[2], args[3]))
        self.get_canvas_fn().draw_line(line)


class DrawRectangleCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, args):
        if len(args) < 4:
            raise ValueError("4 arguments expected (x1, y1, x2, y2)")
        rectangle = Rectangle(Point(args[0], args[1]), Point(args[2], args[3]))
        self.get_canvas_fn().draw_rectangle(rectangle)


class BucketFillCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, args):
        if len(args) < 2:
            raise ValueError("2 arguments expected (x1, y1)")
        self.get_canvas_fn().bucket_fill(Point(args[0], args[1]))


class DeleteCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, args):
        if len(args) < 2:
            raise ValueError("2 arguments expected (x1, y1)")
        self.get_canvas_fn().delete(Point(args[0], args[1]))


class UndoCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, args = None):
        self.get_canvas_fn().undo()
