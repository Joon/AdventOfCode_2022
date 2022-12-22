def move(current_tile, direction, world_tiles, number):    
    move_tile = current_tile
    for i in range(number):
        curr_x, curr_y = move_tile
        min_y = min([y for x, y in world_tiles.keys() if x == move_tile[0]])
        max_y = max([y for x, y in world_tiles.keys() if x == move_tile[0]])
        min_x = min([x for x, y in world_tiles.keys() if y == move_tile[1]])
        max_x = max([x for x, y in world_tiles.keys() if y == move_tile[1]])
        if direction == 'U':
            curr_y -= 1     
            if curr_y < min_y:
                curr_y = max_y
        elif direction == 'D':
            curr_y += 1     
            if curr_y > max_y:
                curr_y = min_y
        elif direction == 'L':
            curr_x -= 1     
            if curr_x < min_x:
                curr_x = max_x
        elif direction == 'R':
            curr_x += 1     
            if curr_x > max_x:
                curr_x = min_x
        else:
            raise Exception(f"Unknown direction {direction}")
        if world_tiles[(curr_x, curr_y)] == '#':
            print(f"Hit wall at {curr_x}, {curr_y}")
            return move_tile
        else:
            move_tile = (curr_x, curr_y)  
    return move_tile      

file = open('day22_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

world_tiles = {}
for y, line in enumerate(lines):
    if line == '':
        break    
    for x, char in enumerate(line):
        if char in ['.', '#']:
            world_tiles[(x, y)] = char

current_tile = (min([x for x, y in world_tiles.keys() if y == 0]), 0)
sprite_direction = 'R'
sprite_degrees = 0
print("Starting on", current_tile)

instructions = lines[-1]
pending_number = ''

for i, c in enumerate(instructions):
    if c.isnumeric():
        pending_number += c
    else:
        if pending_number != '':
            print(f"Moving {pending_number} tiles {sprite_direction}")
            current_tile = move(current_tile, sprite_direction, world_tiles, int(pending_number))
            print("Moved to", current_tile)
            pending_number = ''
        if c == "L":
            sprite_degrees -= 90
            if sprite_degrees < 0:
                sprite_degrees = 270
            print("Turning Left, new heading", sprite_degrees)
        elif c == "R":
            sprite_degrees += 90
            if sprite_degrees == 360:
                sprite_degrees = 0
            print("Turning Right, new heading", sprite_degrees)
        match sprite_degrees:
            case 0:
                sprite_direction = 'R'
            case 90:
                sprite_direction = 'D'
            case 180:
                sprite_direction = 'L'
            case 270:
                sprite_direction = 'U'
            case _:
                raise Exception(f"Unknown sprite degrees {sprite_degrees}")
        
if pending_number != '':
    print(f"Moving {pending_number} tiles {sprite_direction}")
    current_tile = move(current_tile, sprite_direction, world_tiles, int(pending_number))

print("Final position", current_tile)
final_cell_x = current_tile[0] + 1
final_cell_y = current_tile[1] + 1
print("Answer 1: ", 1000 * final_cell_y + 4 * final_cell_x + sprite_degrees)
