'''
This module define the canvas application commands
'''

from canvas import (
    Canvas,
    Point,
    Line,
    Rectangle
)

class ExitCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to exit the application
    '''
    @staticmethod
    def execute(*_):
        '''
        Exit the application
        '''
        raise SystemExit()


class CreateCanvasCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to create a new canvas

    Args:
        callback: a function that will receive the newly created canvas instance
    '''
    def __init__(self, callback):
        self._callback = callback

    def execute(self, *args):
        '''
        Create a new canvas instance

        Args:
            width, height of the canvas
        '''
        if len(args) < 2:
            raise ValueError("2 arguments expected (width, heigth)")
        width, heigth = args[0], args[1]
        try:
            self._callback(Canvas(width, heigth))
        except (TypeError, ValueError) as ex:
            raise TypeError("Width and heigth must be convertible to integers") from ex


class DrawLineCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to draw a line on the canvas

    Args:
        get_canvas_fn: a function that returns the canvas instance to draw on
    '''
    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        #pylint: disable=invalid-name
        '''
        Draw a line on the canvas

        Args:
            x1, y1, x2, y2:
            the int coordinates of (x1, y1) and (x2, y2) between which the line will be drawn
        '''
        if len(args) < 4:
            raise ValueError("4 arguments expected (x1, y1, x2, y2)")
        x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        line = Line(Point(x1, y1), Point(x2, y2))
        self.get_canvas_fn().draw_line(line)


class DrawRectangleCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to draw a rectangle on the canvas

    Args:
        get_canvas_fn: a function that returns the canvas instance to draw on
    '''
    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        #pylint: disable=invalid-name
        '''
        Draw a rectangle on the canvas

        Args:
            x1, y1, x2, y2:
            the int coordinates of (x1, y1), the top-left corner of the rectangle
            and (x2, y2), the bottom-right corner of the rectangle
        '''
        if len(args) < 4:
            raise ValueError("4 arguments expected (x1, y1, x2, y2)")
        x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        rectangle = Rectangle(Point(x1, y1), Point(x2, y2))
        self.get_canvas_fn().draw_rectangle(rectangle)


class BucketFillCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to paint a shape or fill a zone with a given colour

    Args:
        get_canvas_fn: a function that returns the canvas instance to draw on
    '''
    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        #pylint: disable=invalid-name
        '''
        Paint a shape or fill a zone with a given colour

        Args:
            x, y: the int coordinates of the point from which to paint the connected shape or zone
            colour: the colour to paint with
        '''
        if len(args) < 2:
            raise ValueError("3 arguments expected (x, y, colour)")
        x, y, colour = args[0], args[1], args[2]
        self.get_canvas_fn().bucket_fill(Point(x, y), colour)


class DeleteCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to delete a shape or reset a zone colour

    Args:
        get_canvas_fn: a function that returns the canvas instance to draw on
    '''
    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *args):
        #pylint: disable=invalid-name
        '''
        Delete a shape or reset a zone colour

        Args:
            x, y: the int coordinates of the point from which to delete the connected shape or zone
        '''
        if len(args) < 2:
            raise ValueError("2 arguments expected (x, y)")
        x, y = args[0], args[1]
        self.get_canvas_fn().delete(Point(x, y))


class UndoCommand(object):
    #pylint: disable=too-few-public-methods
    '''
    Command to undo the last action

    Args:
        get_canvas_fn: a function that returns the canvas instance to draw on
    '''
    def __init__(self, get_canvas_fn):
        self.get_canvas_fn = get_canvas_fn

    def execute(self, *_):
        '''
        Undo the last action
        '''
        self.get_canvas_fn().undo()
