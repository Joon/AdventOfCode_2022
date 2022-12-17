file = open('day17_input.txt', 'r')
line = [s.strip('\n') for s in file.readlines()][0]

shapes = [
    [(0,0), (1,0), (2,0), (3,0)], # -
    [(1,0), (0,1), (1,1), (2,1), (1,2)], # +
    [(2,0), (2,1), (0,2), (1,2), (2,2)], # reverse L
    [(0,0), (0,1), (0,2), (0, 3)], # l
    [(0,0), (1,0), (0,1), (1, 1)], # square
]

shape_x_start = 2
shape_heights = [1, 3, 3, 4, 2]

def can_move_x(shape, new_shape_x, shape_y, world):
    for point in shapes[shape]:
        # the horizontal movement is blocked by a block in the world
        if (new_shape_x + point[0], shape_y - point[1]) in world:
            return False
        if new_shape_x + point[0] < 0 or new_shape_x + point[0] > 6:
            return False
    return True

def can_move_y(shape, shape_x, new_shape_y, world):
    for point in shapes[shape]:
        # the vertical movement is blocked by a block in the world
        if (shape_x + point[0], new_shape_y - point[1]) in world:
            return False
        if new_shape_y < 0:
            return False

    return True

def print_world(world, max_y):
    print('   -   ')
    for y in range(max_y, -1, -1):
        line = ''
        for x in range(7):
            if (x,y) in world:
                line += world[(x,y)]
            else:
                line += '.'
        print(line)

def print_move(world, shape, shape_x, shape_y):
    for p in shapes[shape]:
        world[(shape_x + p[0], shape_y - p[1])] = '@'
    local_max_y = shape_y + 1
    print_world(world, local_max_y)

def buildworld(iterations):
    max_y = 0

    world = {}

    max_y = -1
    fall_iterations = 0
    shape_count = 0
    for i in range(iterations):
        if i % 10000 == 0:
            print('shape_count', i)
        shape = i % len(shapes)
        shape_y = max_y + shape_heights[shape] + 3
        shape_x = shape_x_start    
        falling = True
        max_world_y = -1
        if len(world) > 0:
            max_world_y = max([w[1] for w in world.keys()])
        #print_move(world.copy(), shape, shape_x, shape_y)
        shape_count += 1
        while falling:
            wind_direction_ind = line[fall_iterations % len(line)]
            wind_direction = -1 if wind_direction_ind == "<" else 1
            if can_move_x(shape, shape_x + wind_direction, shape_y, world):
                shape_x += wind_direction
                #print_move(world.copy(), shape, shape_x, shape_y)
            if can_move_y(shape, shape_x, shape_y - 1, world):
                shape_y -= 1
                #print_move(world.copy(), shape, shape_x, shape_y)
            else:            
                for p in shapes[shape]:
                    world[(shape_x + p[0], shape_y - p[1])] = '#'
                new_max_world_y = max([w[1] for w in world.keys()])
                if max_world_y > 0:
                    max_y += new_max_world_y - max_world_y
                else:
                    max_y = new_max_world_y
                falling = False
            fall_iterations += 1
        #print_world(world, max_y)
    return world

world_2022 = buildworld(2022) 
tallest_block = max([p[1] for p in world_2022.keys()]) + 1
print('tallest block', tallest_block)

if len(line) % len(shapes) == 0:
    iteration_1 = buildworld(len(line))
    max_after_1 = max([p[1] for p in iteration_1.keys()]) + 1
    iteration_2 = buildworld(len(line) * 2)
    max_after_2 = max([p[1] for p in iteration_1.keys()]) + 1
    iteration_3 = buildworld(len(line) * 3)
    max_after_3 = max([p[1] for p in iteration_1.keys()]) + 1
    print('max after 1', max_after_1)
    print('max after 2', max_after_2)
    print('max after 3', max_after_3)
else:
    print('no pattern')
    
