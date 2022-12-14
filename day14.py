from itertools import chain
file = open('day14_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

rock_structures = []
# 498,4 -> 498,6 -> 496,6
for l in lines:
    s_points = l.split(' -> ')    
    rock_structures.append([(int(s_p.split(',')[0]), int(s_p.split(',')[1])) for s_p in s_points])

all_rock_x = list(chain.from_iterable(([[p[0] for p in l] for l in rock_structures])))
all_rock_y = list(chain.from_iterable(([[p[1] for p in l] for l in rock_structures])))

min_x = min(all_rock_x) - 1
max_x = max(all_rock_x) + 1
# sand starts from 500, 0
min_y = 0
max_y = max(all_rock_y) + 1

print(f"World params: X axis: {min_x} to {max_x}  Y Axis: {min_y} to {max_y}")

world = {}

for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        world[(x, y)] = "."

for r in rock_structures:
    origin = r[0]
    for i in range(1,len(r)):
        dest = r[i]
        x_step = 1
        if dest[0] < origin[0]:
            x_step = -1
        y_step = 1
        if dest[1] < origin[1]:
            y_step = -1
        for x in range(origin[0], dest[0] + x_step, x_step):
            for y in range(origin[1], dest[1] + y_step, y_step):
                world[(x, y)] = "#"
        origin = r[i]


def print_grid(world):
    for y in range(min_y, max_y + 1):
        print_line = ""
        for x in range(min_x, max_x + 1):
            print_line = print_line + world[(x, y)]
        print(print_line)


def try_fall(location, delta):
    global min_x
    global max_x
    new_location = tuple_add(location, delta)
    if (new_location[0] < min_x):
        min_x = min_x - 1
        for y in range(min_y, max_y + 1):
            world[(min_x, y)] = "."
    if (new_location[0] > max_x):
        max_x = max_x + 1
        for y in range(min_y, max_y + 1):
            world[(max_x, y)] = "."
    if world[new_location] == ".":
        world[new_location] = 'o'
        world[location] = '.'
        return True
    return False

def tuple_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

sand_produced = 0


done = False
while not done:
    sand_produced = sand_produced + 1
    current_sand_location = (500, 0)
    sand_in_motion = True
    while (sand_in_motion):
        # first - try fall straight down
        if try_fall(current_sand_location, (0, 1)):
            current_sand_location = tuple_add(current_sand_location, (0, 1))
        # second - down and to the left
        elif try_fall(current_sand_location, (-1, 1)):
            current_sand_location = tuple_add(current_sand_location, (-1, 1))
        # third - down and to the right
        elif try_fall(current_sand_location, (1, 1)):
            current_sand_location = tuple_add(current_sand_location, (1, 1))
        else:
            sand_in_motion = False
            if current_sand_location == (500, 0):
                done = True
        # This sand unit has fallen on to the floor - stop it here
        if current_sand_location[1] == max_y:            
            sand_in_motion = False

print_grid(world)
print("Units of sand produced: " + str(sand_produced))
