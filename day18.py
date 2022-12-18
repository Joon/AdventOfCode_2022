from numpy import genfromtxt
import numpy as np
import itertools
my_data = genfromtxt('day18_input.txt', delimiter=',')
face_count = 0
side_transforms = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]
for (x, y, z) in my_data:
    for (tx, ty, tz) in side_transforms:
        neighbour = (x + tx, y + ty, z + tz)
        if not any(np.equal(my_data,neighbour).all(1)):
            face_count += 1
print("Answer 1", face_count)

clear_transforms = list(itertools.product([0,1, -1], repeat=3))
max_x = max([point[0] for point in my_data])
max_y = max([point[1] for point in my_data])
max_z = max([point[2] for point in my_data])
min_x = min([point[0] for point in my_data])
min_y = min([point[1] for point in my_data])
min_z = min([point[2] for point in my_data])

start_x = min_x + ((max_x - min_x) // 2)
start_y = min_y + ((max_y - min_y) // 2)
start_z = max_z + 50

while True:
    if any(np.equal(my_data,(start_x, start_y, start_z - 1)).all(1)):
        break
    start_z = start_z - 1
    if (start_z < min_z):
        print("no start point found")
        break

visited_clear_spots = set()

print(f"starting at last clear spot approaching block: {(start_x, start_y, start_z)}")   

def count_adjacent_blocks(clear_spot):
    (x, y, z) = clear_spot
    block_count = 0
    for (tx, ty, tz) in side_transforms:
        neighbour = (x + tx, y + ty, z + tz)
        if any(np.equal(my_data,neighbour).all(1)):
            block_count += 1
    return block_count

def is_adjacent(clear_spot):
    (x, y, z) = clear_spot
    for (tx, ty, tz) in clear_transforms:
        neighbour = (x + tx, y + ty, z + tz)
        if any(np.equal(my_data,neighbour).all(1)):
            return True
    return False

total_spots = 0
spots_to_process = [(start_x, start_y, start_z)]
while len(spots_to_process) > 0:
    (x, y, z) = spots_to_process.pop()
    #print("Checking", (x, y, z))
    if (x, y, z) in visited_clear_spots:
        continue
    total_spots += count_adjacent_blocks((x, y, z))
    visited_clear_spots.add((x, y, z))
    for (tx, ty, tz) in side_transforms:
        clear_neighbour = (x + tx, y + ty, z + tz)
        if not any(np.equal(my_data, clear_neighbour).all(1)):
            if is_adjacent(clear_neighbour) > 0:
                spots_to_process.append(clear_neighbour)

print("Answer 2", total_spots)