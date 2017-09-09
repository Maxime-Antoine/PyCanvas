from canvas import Canvas

class ExitCommand(object):

    @staticmethod
    def execute():
        raise SystemExit()


class CreateCanvasCommand(object):

    @staticmethod
    def execute(width, height):
        return Canvas(width, height)


class DrawLineCommand(object):

    @staticmethod
    def execute(canvas, line):
        canvas.draw_line(line)


class DrawRectangleCommand(object):

    @staticmethod
    def execute(canvas, rectangle):
        canvas.draw_rectangle(rectangle)


class BucketFillCommand(object):

    @staticmethod
    def execute(canvas, target_point):
        canvas.bucket_fill(target_point)


class DeleteCommand(object):

    @staticmethod
    def execute(canvas, target_point):
        canvas.delete(target_point)


class UndoCommand(object):

    @staticmethod
    def execute(canvas):
        canvas.undo()
