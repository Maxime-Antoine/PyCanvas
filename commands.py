from canvas import (
    Canvas,
    Point,
    Line,
    Rectangle
)

class ExitCommand(object):

    @staticmethod
    def execute(*_):
        raise SystemExit()


class CreateCanvasCommand(object):

    def __init__(self, callback):
        self._callback = callback

    def execute(self, *args):
        if len(args) < 2:
            raise ValueError("2 arguments expected (width, heigth)")
        width, heigth = args[0], args[1]
        try:
            self._callback(Canvas(width, heigth))
        except (TypeError, ValueError) as ex:
            raise TypeError("Width and heigth must be convertible to integers") from ex


class DrawLineCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        if len(args) < 4:
            raise ValueError("4 arguments expected (x1, y1, x2, y2)")
        x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        line = Line(Point(x1, y1), Point(x2, y2))
        self.get_canvas_fn().draw_line(line)


class DrawRectangleCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        if len(args) < 4:
            raise ValueError("4 arguments expected (x1, y1, x2, y2)")
        x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        rectangle = Rectangle(Point(x1, y1), Point(x2, y2))
        self.get_canvas_fn().draw_rectangle(rectangle)


class BucketFillCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        if len(args) < 2:
            raise ValueError("3 arguments expected (x, y, colour)")
        x, y, colour = args[0], args[1], args[2]
        self.get_canvas_fn().bucket_fill(Point(x, y), colour)


class DeleteCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        if len(args) < 2:
            raise ValueError("2 arguments expected (x, y)")
        x, y = args[0], args[1]
        self.get_canvas_fn().delete(Point(x, y))


class UndoCommand(object):

    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *_):
        self.get_canvas_fn().undo()
