import os
from time import sleep


file = open('day24_input.txt', 'r')
lines = [s.strip() for s in file.readlines()]

blizzard_state = {}
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char != '#' and char != '.': 
            blizzard_state[(x, y)] = blizzard_state.get((x, y), '') + char

width = len(lines[0])
height = len(lines)

def move_blizzards(old_state, width, height):
    new_state = {}
    for pos, blizzards in old_state.items():
        x, y = pos
        for blizzard in blizzards:
            x_delta = 0
            y_delta = 0
            if blizzard == '>':
                x_delta = 1
                if (x + 1) == width - 1:
                    x_delta = 3 - width
            elif blizzard == '<':
                x_delta = -1
                if (x - 1) == 0:
                    x_delta = width - 3
            elif blizzard == '^':
                y_delta = -1
                if (y - 1) == 0:
                    y_delta = height - 3
            elif blizzard == 'v':
                y_delta = 1            
                if (y + 1) == height - 1:
                    y_delta = 3 - height
            move_to = (x + x_delta, y + y_delta)
            new_state[move_to] = new_state.get(move_to, '') + blizzard
    return new_state

def print_blizzard_state(state, width, height, active_paths = None):
    path_spots = []
    if active_paths is not None:
        path_spots = [p[-1] for p in active_paths]
    for y in range(height):
        for x in range(width):
            to_print = state.get((x, y), '.')
            if to_print == '.' and (x, y) in path_spots:
                to_print = 'E'
            if len(to_print) > 1:
                print(len(to_print), end='')
            else:
                print(to_print, end='')
        print('')

# Only append a path to the processing stack if another path has not already reached the same spot in the same minute
def append_path(active_paths, path, all_paths):    
    same_length_spots = [p[len(path) - 1] for p in all_paths if len(p) >= len(path)]
    if path[-1] not in same_length_spots:
        active_paths.append(path)    
        all_paths.append(path)


def navigate_valley(blizzard_state, width, height, start_pos, end_pos):
    all_paths = []
    
    timestate = {1: blizzard_state.copy()}
    active_paths = [[start_pos]]
    #print(f"Starting navigation at {start_pos}, target is {end_pos}")
    #print_blizzard_state(blizzard_state, width, height, active_paths)
    loop_count = 0
    shortest_solved_length = 99999999999999
    while len(active_paths) > 0:        
        loop_count += 1
        x_y_coords = [p[-1] for p in active_paths]
        score = [abs(end_pos[0] - x) + abs(end_pos[1] - y) for x, y in x_y_coords]
        # We've picked the path that has run the closest, now it needs processing
        closest_path = active_paths.pop(score.index(min(score)))
        clos_x, clos_y = closest_path[-1]
        min_possible_moves = abs(end_pos[0] - clos_x) + abs(end_pos[1] - clos_y)
        if len(closest_path) + min_possible_moves >= shortest_solved_length:
            # Best path cannot be solved in fewer paths than the shortest solved path, disregard it
            #print('path excluded by total moves')
            continue
        next_move_minute = len(closest_path) + 1
        if next_move_minute in timestate:
            blizzard_state = timestate[next_move_minute]
        else:
            minute = max(timestate.keys())
            blizzard_state = timestate[max(timestate.keys())]
            while minute < next_move_minute:
                blizzard_state = move_blizzards(blizzard_state, width, height)
                minute += 1
                timestate[minute] = blizzard_state.copy()

        current_pos = closest_path[-1]
        # Is waiting an option?
        if current_pos not in blizzard_state:
            append_path(active_paths, closest_path + [current_pos], all_paths)
        curx, cury = current_pos
        # Check all move options
        for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            newx = curx + move[0]
            newy = cury + move[1]
            new_pos = (newx, newy)
            # Is this a solution?
            if new_pos == end_pos:
                shortest_solved_length = len(closest_path)
                print("Solve candidate", shortest_solved_length)
            else:
                # This move would hit a wall, disregard it
                if newx <= 0 or newx >= width - 1 or newy <= 0 or newy >= height - 1:
                    continue
                new_pos = (newx, newy)
                # Not a solution, add it the active paths if the move does not hit a blizzard
                if new_pos not in blizzard_state:                
                    append_path(active_paths, closest_path + [new_pos], all_paths)
        #os.system('cls')
        if loop_count % 1000 == 0:
            print("Minute", next_move_minute, "active paths", len(active_paths), "shortest solved", shortest_solved_length, "(", loop_count, "loops)")
        #print_blizzard_state(blizzard_state, width, height, active_paths)
        #sleep(1)
    return shortest_solved_length, timestate[shortest_solved_length]

shortest_solved_length, next_path_state = navigate_valley(blizzard_state, width, height, (0,1), (width - 2, height - 1))
print("Answer 1: Shortest path takes", shortest_solved_length, "minutes")
shortest_solved_length_2, last_path_state = navigate_valley(next_path_state, width, height, (width - 2, height - 1), (0,1))
shortest_solved_length_3, _ = navigate_valley(last_path_state, width, height, (0,1), (width - 2, height - 1))
print ("Answer 2: Shortest path takes", shortest_solved_length + shortest_solved_length_2 - 1 + shortest_solved_length_3 - 1, "minutes")
