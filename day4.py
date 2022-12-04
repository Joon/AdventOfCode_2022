file = open('day4_input.txt', 'r')
lines = [s.strip() for s in file.readlines()]

def parse_assignment(assignment):
    parts = assignment.split('-')
    return [int(parts[0]), int(parts[1])]

def parse_assignments(assignments):
    parts = assignments.split(',')
    return (parse_assignment(parts[0]), parse_assignment(parts[1]))

def overlaps(left, right):
    if left[0] >= right[0] and left[1] <= right[1]:
        return True
    if right[0] >= left[0] and right[1] <= left[1]:
        return True
    return False

def partial_overlap(left, right):
    if (left[0] >= right[0] and left[0] <= right[1]) or (right[0] >= left[0] and right[0] <= left[1]):
        return True
    return False

assignments = [parse_assignments(l) for l in lines]
overlaps = [a for a in assignments if overlaps(a[0], a[1])]
print("Part 1: {}".format(len(overlaps)))

partial_overlaps = [a for a in assignments if partial_overlap(a[0], a[1])]
print("Part 2: {}".format(len(partial_overlaps)))