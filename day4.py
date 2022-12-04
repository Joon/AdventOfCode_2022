file = open('day4_input.txt', 'r')
lines = [s.strip() for s in file.readlines()]

def expand_assignment(assignment):
    parts = assignment.split('-')
    return list(range(int(parts[0]), int(parts[1]) + 1))

def parse_assignments(assignments):
    parts = assignments.split(',')
    return (expand_assignment(parts[0]), expand_assignment(parts[1]))

def overlaps(left, right):
    if left[0] >= right[0] and left[0] <= right[-1] and left[-1] >= right[0] and left[-1] <= right[-1]:
        return True
    if right[0] >= left[0] and right[0] <= left[-1] and right[-1] >= left[0] and right[-1] <= left[-1]:
        return True
    return False

def partial_overlap(left, right):
    if (left[0] >= right[0] and left[0] <= right[-1]) or (right[0] >= left[0] and right[0] <= left[-1]):
        return True
    return False

assignments = [parse_assignments(l) for l in lines]
overlaps = [a for a in assignments if overlaps(a[0], a[1])]
print(len(overlaps))

partial_overlaps = [a for a in assignments if partial_overlap(a[0], a[1])]
print(len(partial_overlaps))