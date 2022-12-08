file = open('day8_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

trees = [[int(t) for t in s] for s in lines]

def tree_visible(x, y, trees, direction_x, direction_y):
    look_at_x = x
    look_at_y = y
    check_heights = []
    while look_at_x > 0 and look_at_x < len(trees[0]) - 1 and look_at_y > 0 and look_at_y < len(trees) - 1:
        look_at_x = look_at_x + direction_x
        look_at_y = look_at_y + direction_y    
        check_heights.append(trees[look_at_y][look_at_x])

    return max(check_heights) < trees[y][x]

def calc_visible(trees):
    visible = [[False for t in row] for row in trees]

    for y in range(len(trees)):
        for x in range(len(trees[0])):
            if x == 0 or y == 0 or x == len(trees) - 1 or y == len(trees[0]) - 1:
                visible[y][x] = True
            else:
                left = tree_visible(x, y, trees, -1, 0)
                right = tree_visible(x, y, trees, 1, 0)
                top = tree_visible(x, y, trees, 0, -1)
                bottom = tree_visible(x, y, trees, 0, 1)
                visible[y][x] = left or right or bottom or top
    return visible

def visible_trees(x, y, trees, direction_x, direction_y):
    look_at_x = x
    look_at_y = y
    check_heights = []
    while look_at_x > 0 and look_at_x < len(trees[0]) - 1 and look_at_y > 0 and look_at_y < len(trees) - 1:
        look_at_x = look_at_x + direction_x
        look_at_y = look_at_y + direction_y    
        check_heights.append(trees[look_at_y][look_at_x])

    for i in range(len(check_heights)):
        if check_heights[i] >= trees[y][x]:
            return i + 1
    return len(check_heights)

def calc_scenic_score(trees):
    scenic_scores = [[0 for t in row] for row in trees]

    for y in range(len(trees)):
        for x in range(len(trees[0])):
            if x == 0 or y == 0 or x == len(trees) - 1 or y == len(trees[0]) - 1:
                visible[y][x] = 0
            else:
                left = visible_trees(x, y, trees, -1, 0)
                right = visible_trees(x, y, trees, 1, 0)
                top = visible_trees(x, y, trees, 0, -1)
                bottom = visible_trees(x, y, trees, 0, 1)
                scenic_scores[y][x] = left * right * bottom * top
    return scenic_scores

def print_grid(grid):
    for y in range(len(trees)):
        print_line = ""
        for x in range(len(trees[0])):
            print_line = print_line + " {}".format(grid[y][x])
        print(print_line)

#print_grid(trees)
#print('-----------')

visible = calc_visible(trees)
total_visible = [[1 if v else 0 for v in line] for line in visible]
#print('-TOTAL VISIBLE-')

#print_grid(total_visible)
print('Answer 1', sum([sum(l) for l in total_visible]))

scenic_scores = calc_scenic_score(trees)
#print('-SCENIC SCORES-')
#print_grid(scenic_scores)
print('Answer 2', max([max(s) for s in scenic_scores]))