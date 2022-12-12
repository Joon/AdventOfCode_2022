from colorama import Fore
from colorama import Style

file = open('day12_input.txt', 'r')

grid = [list(l.strip()) for l in file.readlines()]
target_x = -1
target_y = -1
start_x = -1
start_y = -1
a_nodes = []
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if (grid[y][x] == 'a'):
            a_nodes.append((x, y))
        if (grid[y][x] == 'E'):
            target_x = x
            target_y = y
            a_nodes.append((x, y))
        if (grid[y][x] == 'S'):
            start_x = x
            start_y = y

grid[start_y][start_x] = 'a'
grid[target_y][target_x] = 'z'

INFINITY = 999999999999

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path

def calc_score(node):
    return abs(node[0] - target_x) + abs(node[1] - target_y)

def lowest_score_node(open, score):
    lowestScore = INFINITY
    node = None
    for o in open:
        if score[o] < lowestScore:
            lowestScore = score[o]
            node = o
    if node == None:
        raise KeyError()
    return node

def traversible(source_char, target_char):
    source_int = ord(source_char)
    target_int = ord(target_char)
    if source_int > target_int:
        return True
    # the elevation of the destination square can be at most one higher than the
    # elevation of your current square
    if target_int - source_int > 1:
        return False
    return True

print(traversible("a", "b"))
print(traversible("a", "c"))
print(traversible("c", "b"))
print(traversible("c", "a"))

def calc_neighbours(current):
    neighbours = []
    current_char = grid[current[1]][current[0]]
    for neighbour_moves in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        target_x = current[0] + neighbour_moves[0]
        target_y = current[1] + neighbour_moves[1]
        if target_y >= 0 and target_x >= 0 and target_y < len(grid) and target_x < len(grid[target_y]):
            target_char = grid[target_y][target_x]
            if traversible(current_char, target_char):
                neighbours.append((target_x, target_y))
    return neighbours
    
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
def A_Star(start, goal):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = {}
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore = {}
    fScore[start] = calc_score(start)

    while len(openSet) > 0:
        #current := the node in openSet having the lowest fScore[] value
        current = lowest_score_node(openSet, fScore)
        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)

        for n in calc_neighbours(current):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            #tentative_gScore := gScore[current] + d(current, neighbor)
            # Part 1: All steps are worth one
            tentative_gScore = gScore[current] + 1
            gScore.setdefault(n, INFINITY)
            if tentative_gScore < gScore[n]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + calc_score(n)
                if n not in openSet:
                    openSet.add(n)

    # Open set is empty but goal was never reached
    raise TabError()

shortest_path = A_Star((start_x, start_y), (target_x, target_y))
print("Answer 1: " + str(len(shortest_path) - 1))

a_routes = []
fail_count = 0
for n in a_nodes:
    try:
        path = A_Star(n, (target_x, target_y))    
        a_routes.append(len(path) - 1)
    except:
        # do nothing
        fail_count = fail_count + 1
print(a_routes)
print("Answer 2: " + str(min([a for a in a_routes if a > 0])))