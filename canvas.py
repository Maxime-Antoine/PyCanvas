from enum import Enum

class Canvas(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [
            [(CanvasCellContentType.Empty, ' ') for i in range(width)] for j in range(height)
        ]

    def _draw_point(self, point):
        self.cells[point.x][point.y] = (CanvasCellContentType.Line, 'x')

    def _point_is_out_of_bound(self, point):
        x_is_out_of_canvas_bound = point.x < 0 or point.x >= self.width
        y_is_out_of_canvas_bound = point.y < 0 or point.y >= self.height
        return x_is_out_of_canvas_bound or y_is_out_of_canvas_bound

    def draw_line(self, line):
        if (self._point_is_out_of_bound(line.from_point) or
            self._point_is_out_of_bound(line.to_point)):
            raise OutOfCanvasBoundError()
        self._draw_line(line)

    def _draw_line(self, line):
        for point in line.get_points():
            self._draw_point(point)

    def draw_rectangle(self, rectangle):
        if (self._point_is_out_of_bound(rectangle.top_left_point) or
            self._point_is_out_of_bound(rectangle.bottom_right_point)):
            raise OutOfCanvasBoundError()
        for line in rectangle.get_lines():
            self._draw_line(line)

    def bucket_fill(self, point, colour):
        if self._point_is_out_of_bound(point):
            raise OutOfCanvasBoundError()
        self._bucket_fill(point, colour)

    def _bucket_fill(self, point, colour):
        content_type_to_fill, _ = self.cells[point.x][point.y]
        processed = set()
        to_process = [point]
        
        def can_process_cell(cell):
            return (cell not in processed and 
                    cell not in to_process and 
                    not self._point_is_out_of_bound(cell))
        
        while to_process != []:
            current_point = to_process.pop()
            processed.add(current_point)
            
            current_point_type, _ = self.cells[current_point.x][current_point.y]
            if current_point_type == content_type_to_fill:
                self.cells[current_point.x][current_point.y] = (content_type_to_fill, colour)
                #enqueue non processed neighbours
                left_neighbour = Point(current_point.x - 1, current_point.y)
                if can_process_cell(left_neighbour):
                    to_process.insert(0, left_neighbour)
                right_neighbour = Point(current_point.x + 1, current_point.y)
                if can_process_cell(right_neighbour):
                    to_process.insert(0, right_neighbour)
                top_neighbour = Point(current_point.x, current_point.y - 1)
                if can_process_cell(top_neighbour):
                    to_process.insert(0, top_neighbour)
                bottom_neighbour = Point(current_point.x, current_point.y + 1)
                if can_process_cell(bottom_neighbour):
                    to_process.insert(0, bottom_neighbour)

    def delete(self, point):
        if self._point_is_out_of_bound(point):
            raise OutOfCanvasBoundError()
        #TODO rest of implementation

    def undo(self):
        pass

    def __str__(self):
        print(' ' + '-' * self.width + ' ')
        for y in range(self.height):
            str_line = '|'
            for x in range(self.width):
                _, colour = self.cells[x][y]
                str_line += colour
            print(str_line + '|' + '\n')
        print(' ' + '-' * self.width + ' ')


class CanvasCellContentType(Enum):
    Empty = 1
    Line = 2


class OutOfCanvasBoundError(Exception):
    pass


class Point(object):
    
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x * 97 + self.y * 101)


class Line(object):

    def __init__(self, from_point, to_point):
        self.from_point = from_point
        self.to_point = to_point

    def __eq__(self, other):
        return self.from_point == other.from_point and self.to_point == other.to_point

    def get_points(self):
        if self._is_horizontal():
            return [Point(self.from_point.x, y) for y in range(self.from_point.y, self.to_point.y + 1)]
        elif self._is_vertical():
            return [Point(x, self.from_point.y) for x in range(self.from_point.x, self.to_point.x + 1)]
        else:
            raise NotImplementedError("Only horizontal and vertical lines are implemented so far")

    def _is_horizontal(self):
        return self.from_point.x == self.to_point.x

    def _is_vertical(self):
        return self.from_point.y == self.to_point.y


class Rectangle(object):

    def __init__(self, top_left_point, bottom_right_point):
        self.top_left_point = top_left_point
        self.bottom_right_point = bottom_right_point

    def get_lines(self):
        top_right_point = Point(self.bottom_right_point.x, self.top_left_point.y)
        bottom_left_point = Point(self.top_left_point.x, self.bottom_right_point.y)
        return [
            Line(self.top_left_point, top_right_point),
            Line(self.top_left_point, bottom_left_point),
            Line(top_right_point, self.bottom_right_point),
            Line(bottom_left_point, self.bottom_right_point)
        ]
