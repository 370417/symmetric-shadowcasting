import math
from fractions import Fraction

def compute_fov(origin, is_blocking, mark_visible):

    mark_visible(*origin)

    for i in range(4):
        quadrant = Quadrant(i, origin)

        def reveal(tile):
            x, y = quadrant.transform(tile)
            mark_visible(x, y)

        def is_wall(tile):
            if tile is None:
                return False
            x, y = quadrant.transform(tile)
            return is_blocking(x, y)

        def is_floor(tile):
            if tile is None:
                return False
            x, y = quadrant.transform(tile)
            return not is_blocking(x, y)

        def scan(row):
            prev_tile = None
            for tile in row.tiles():
                if is_wall(tile) or is_symmetric(row, tile):
                    reveal(tile)
                if is_wall(prev_tile) and is_floor(tile):
                    row.start_slope = slope(tile)
                if is_floor(prev_tile) and is_wall(tile):
                    next_row = row.next()
                    next_row.end_slope = slope(tile)
                    scan(next_row)
                prev_tile = tile
            if is_floor(prev_tile):
                scan(row.next())

        first_row = Row(1, Fraction(-1), Fraction(1))
        scan(first_row)

class Quadrant:

    north = 0
    east  = 1
    south = 2
    west  = 3

    def __init__(self, cardinal, origin):
        self.cardinal = cardinal
        self.ox, self.oy = origin

    def transform(self, tile):
        row, col = tile
        if self.cardinal == self.north:
            return (self.ox + col, self.oy - row)
        if self.cardinal == self.south:
            return (self.ox + col, self.oy + row)
        if self.cardinal == self.east:
            return (self.ox + row, self.oy + col)
        if self.cardinal == self.west:
            return (self.ox - row, self.oy + col)

class Row:

    def __init__(self, depth, start_slope, end_slope):
        self.depth = depth
        self.start_slope = start_slope
        self.end_slope = end_slope

    def tiles(self):
        min_col = round_ties_up(self.depth * self.start_slope)
        max_col = round_ties_down(self.depth * self.end_slope)
        for col in range(min_col, max_col + 1):
            yield (self.depth, col)

    def next(self):
        return Row(
            self.depth + 1,
            self.start_slope,
            self.end_slope)

def slope(tile):
    row_depth, col = tile
    return Fraction(2 * col - 1, 2 * row_depth)

def is_symmetric(row, tile):
    row_depth, col = tile
    return (col >= row.depth * row.start_slope
        and col <= row.depth * row.end_slope)

def round_ties_up(n):
    return math.floor(n + 0.5)

def round_ties_down(n):
    return math.ceil(n - 0.5)

def scan_iterative(row):
    rows = [row]
    while rows:
        row = rows.pop()
        prev_tile = None
        for tile in row.tiles():
            if is_wall(tile) or is_symmetric(row, tile):
                reveal(tile)
            if is_wall(prev_tile) and is_floor(tile):
                row.start_slope = slope(tile)
            if is_floor(prev_tile) and is_wall(tile):
                next_row = row.next()
                next_row.end_slope = slope(tile)
                rows.append(next_row)
            prev_tile = tile
        if is_floor(prev_tile):
            rows.append(row.next())
