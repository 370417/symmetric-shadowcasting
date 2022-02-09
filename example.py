import shadowcasting

# Minimal shadowcasting example

map_str = '''
##################
#................#
#...###..........#
#...###....#.....#
#...###....#.....#
#..........#.....#
##################
'''[1:] # Use [1:] to remove first newline

width = 18
height = 7
player_location = (9, 3)

map_list = list(map_str.splitlines())

def is_blocking(x, y):
    return map_list[y][x] == '#'

is_visible = set()
def reveal(x, y):
    is_visible.add((x, y))

shadowcasting.compute_fov(player_location, is_blocking, reveal)

for y in range(height):
    for x in range(width):
        if (x, y) == player_location:
            print('@', end='')
        elif (x, y) in is_visible:
            print(map_list[y][x], end='')
        else:
            print(' ', end='')
    print()

# expected output:
#     ##############
#      ............#
#       #.......
#       #..@.#
#       #....#
#      ......#
#     ########
