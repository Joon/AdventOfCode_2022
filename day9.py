import sys

file = open('day9_input.txt', 'r')
commands = [tuple(s.strip('\n').split(' ')) for s in file.readlines()]

if len(sys.argv) < 2:
    print("Script requires a segment count, and an optional second parm to indicate step printing is required")
    exit(0)

segments = []
for i in range(int(sys.argv[1])):
    segments.append([0, 0])

visited_locations = {"0_0": 0}

def move_tail(head, tail):
    # If the head is ever two steps directly up, down, left, or right from the tail, 
    # the tail must also move one step in that direction so it remains close enough
    if head[0] == tail[0] and tail[1] > (head[1] + 1):
        return [tail[0], tail[1] - 1]
    if head[0] == tail[0] and tail[1] < (head[1] - 1):
        return [tail[0], tail[1] + 1]
    if head[1] == tail[1] and tail[0] > (head[0] + 1):
        return [tail[0] - 1, tail[1]]
    if head[1] == tail[1] and tail[0] < (head[0] - 1):
        return [tail[0] + 1, tail[1]]
    
    # Otherwise, if the head and tail aren't touching and aren't in the same row or column, 
    # the tail always moves one step diagonally to keep up:    
    # not in same row and column
    if head[0] != tail[0] and head[1] != tail[1]:
        # not touching
        if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
            # one step diagonal
            candidate_x_move = head[0] - tail[0]
            x_move = 0
            if candidate_x_move > 0:
                x_move = 1
            if candidate_x_move < 0:
                x_move = -1
            candidate_y_move = head[1] - tail[1]
            y_move = 0
            if candidate_y_move > 0:
                y_move = 1
            if candidate_y_move < 0:
                y_move = -1
            return [tail[0] + x_move, tail[1] + y_move]

    # No change in location
    return tail

# xmax, xmin, ymax, ymin
furthest = [0, 0, 0, 0]

def track_furthest(head, tail, furthest):
    if (head[0] > furthest[0]):
        furthest[0] = head[0]
    if (head[0] < furthest[1]):
        furthest[1] = head[0]
    if (head[1] > furthest[2]):
        furthest[2] = head[1]
    if (head[1] < furthest[3]):
        furthest[3] = head[1]
    if (tail[0] > furthest[0]):
        furthest[0] = tail[0]
    if (tail[0] < furthest[1]):
        furthest[1] = tail[0]
    if (tail[1] > furthest[2]):
        furthest[2] = tail[1]
    if (tail[1] < furthest[3]):
        furthest[3] = tail[1]

def print_positions(segments, furthest):
    if len(sys.argv) < 3:
        return

    for y in range(furthest[2], furthest[3] - 1, -1):
        print_line = ""
        for x in range(furthest[1], furthest[0] + 1):
            print_char = "."
            for si in range(len(segments)):
                if segments[si][0] == x and segments[si][1] == y:
                    if si == 0:
                        print_char = "H"
                    elif si == len(segments) - 1:
                        print_char = "T"
                    else:
                        print_char = str(si)
                    break
            print_line = print_line + print_char
        print(print_line)
    print("")
    print("")

def move_segment(head_location, tail_location, visited_locations, x_move, y_move, furthest):
    new_tail_location = move_tail(head_location, tail_location)
    tail_location[0] = new_tail_location[0]
    tail_location[1] = new_tail_location[1]
    track_furthest(tail_location, head_location, furthest)     

print_positions(segments, furthest)

for command in commands:
    for i in range(int(command[1])):
        x_move = 0
        y_move = 0
        if (command[0] == 'U'):
            y_move = 1
        if (command[0] == 'D'):
            y_move = -1
        if (command[0] == 'L'):
            x_move = -1
        if (command[0] == 'R'):
            x_move = 1

        # move the head
        segments[0][0] = segments[0][0] + x_move
        segments[0][1] = segments[0][1] + y_move
        for si in range(1, len(segments)):
            move_segment(segments[si - 1], segments[si], visited_locations, x_move, y_move, furthest)
        print_positions(segments, furthest)

        location_code = "{}_{}".format(segments[-1][0], segments[-1][1])
        if location_code in visited_locations:
            visited_locations[location_code] = visited_locations[location_code] + 1
        else:
            visited_locations[location_code] = 1

print(len(visited_locations.keys()))