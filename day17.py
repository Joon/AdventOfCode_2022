import datetime
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

def print_world(world, max_y, min_y = -1):
    print('   -   ')
    for y in range(max_y, min_y, -1):
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

def buildworld(iterations, enable_trim = True, track_placements = {}):
    max_y = 0

    world = {}

    max_y = -1
    fall_iterations = 0
    shape_count = 0
    for i in range(iterations):
        if i > 0 and i % 100000 == 0:
            print("{:.5%}".format(i / iterations), datetime.datetime.now())
        if i % 100 == 0 and i > 0 and enable_trim:
            #print('World trimming commenced')
            block_depth = []
            for x in range(7):
                block_depth.append(max([w[1] for w in world.keys() if w[0] == x]))
            min_block_depth = min(block_depth)
            old_world = world.copy()
            world = {}
            for p in old_world.keys():
                if p[1] >= min_block_depth:
                    world[p] = old_world[p]
            #print('World trimming complete')
            
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
                track_placements[max_y] = shape_count
                falling = False
            fall_iterations += 1
        #print_world(world, max_y)
    return world

def calc_line(world, y):
    result = []
    for x in range(7):
        if (x, y) in world.keys():
            result += [world[(x, y)]]
        else:
            result += ['.']
    return str(result)

world_2022 = buildworld(2022) 
tallest_block = max([p[1] for p in world_2022.keys()]) + 1
print('tallest block', tallest_block)

#world_monster = buildworld(1000000000000) 
#monster_tallest_block = max([p[1] for p in world_monster.keys()]) + 1
#print('tallest block', monster_tallest_block)

#pattern_test_length = len(line) * len(shapes)
track_placements = {}
search_space = buildworld(6000, False, track_placements)
search_max_y = max([p[1] for p in search_space.keys()])
print('search space built')
cycle_size = 0
cycle_start = 0
# Look for cycles 
#for cycle_length in range(50, 60):
for cycle_length in range(2700, 2800):
    if cycle_size > 0:
        break
    for test_line in range(search_max_y - cycle_length):        
        cycle_exists = True
        for j in range(cycle_length):
            line1 = calc_line(search_space, test_line + j)
            line2 = calc_line(search_space, test_line + j + cycle_length)
            if line1 != line2:
                cycle_exists = False
                break
        if cycle_exists:
            print('cycle found', cycle_length, test_line)
            cycle_size = cycle_length
            cycle_start = test_line
            break

target = 1000000000000

if cycle_size > 0:
    print("Finding the answer for part 2")
    
    blocks_in_cycle = track_placements[cycle_start + cycle_size] - track_placements[cycle_start]
    blocks_at_cycle_start = track_placements[cycle_start]

    print("Cycle consists of", blocks_in_cycle, "blocks. blocks before cycle", blocks_at_cycle_start)
    blocks_to_fill = target - blocks_at_cycle_start + 1
    
    remainder_to_fill = (blocks_to_fill % blocks_in_cycle) - blocks_at_cycle_start - 1
    remainder_guess = 0
    placements = [k - cycle_start for k in track_placements.keys() if k > cycle_start]
    print("should pick from", [k for k in placements if k >= 1585 and k <= 1587])
    if remainder_to_fill > 0:
        print(remainder_to_fill)
        print(placements.index(1586))
        remainder_guess = placements[remainder_to_fill]
    # End segment catch-up logic is wrong.
    # Correct, expected answer: 264 1565517239532 1586
    # This program's answer:    264 1565517239532 1773
    print(cycle_start, ((blocks_to_fill // blocks_in_cycle) * cycle_size), remainder_guess)
    all_blocks_height = cycle_start + ((blocks_to_fill // blocks_in_cycle) * cycle_size) + remainder_guess
    print("all blocks", all_blocks_height)    
else:
    print("Part 2 is not answereable in thousands of years")


# too haa    1565518315371
# Too high:  1565517244500
# Too high:  1565517244400
# no answer: 1565517241904 [excel]
#            1565517241902 [excel 2]
 
# no answer: 1565517241681
# no answer: 1565517239796
# no answer: 1565517241370
             
