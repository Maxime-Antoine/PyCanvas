from enum import Enum

class Canvas(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [
            [(CanvasCellContentType.Empty, ' ') for i in range(width)] for j in range(height)
        ]

    def draw_point(self, point):
        if self._point_is_out_of_bound(point):
            raise OutOfCanvasBoundError()
        self.cells[point.x][point.y] = (CanvasCellContentType.Line, 'x')

    def _point_is_out_of_bound(self, point):
        x_is_out_of_canvas_bound = point.x < 0 or point.x >= self.width
        y_is_out_of_canvas_bound = point.y < 0 or point.y >= self.height
        return x_is_out_of_canvas_bound or y_is_out_of_canvas_bound

    def draw_line(self, line):
        pass

    def draw_rectangle(self, rectangle):
        pass

    def delete(self, point):
        pass

    def bucket_fill(self, point):
        pass

    def undo(self):
        pass


class CanvasCellContentType(Enum):
    Empty = 1
    Line = 2


class OutOfCanvasBoundError(Exception):
    pass


class Point(object):
    
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        if self.x < 0 or self.y < 0:
            raise ValueError("(x,y) should both be convertible to positive integers")
