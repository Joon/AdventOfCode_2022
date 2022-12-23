ids = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Elf:
    elf_count = 1
    def __init__(self, x, y):
        self.id = ids[Elf.elf_count % len(ids)]
        self.x = x
        self.y = y
        self.direction = ''
        self.overlapped = False
        Elf.elf_count += 1

    def check_elf(self, deltas, elves):
        match_count = 0
        for elf in elves:
            for d in deltas:
                if elf.x == self.x + d[0] and elf.y == self.y + d[1]:
                    match_count += 1
                    return True
        return False

    def consider_move(self, elves, move_intentions):
        border_cell_offsets = [ (-1, -1), (-1, 0), (-1, 1), 
                                (0, 1), (0, -1), 
                                (1, 1), (1, 0), (1, -1)]
        have_neighbour = False
        for d in border_cell_offsets:
            for e in elves:
                if e.x == self.x + d[0] and e.y == self.y + d[1]:
                    have_neighbour = True
                    break
        if not have_neighbour:
            self.direction = ''
            return
        for dir in move_intentions:
            if dir == 'N':
                if not self.check_elf([(1, -1), (0, -1), (-1, -1)], elves):
                    self.direction = 'N'
                    return
            elif dir == 'S':
                if not self.check_elf([(1, 1), (0, 1), (-1, 1)], elves):
                    self.direction = 'S'
                    return
            elif dir == 'E':
                if not self.check_elf([(1, -1), (1, 0), (1, 1)], elves):
                    self.direction = 'E'
                    return
            elif dir == 'W':
                if not self.check_elf([(-1, -1), (-1, 0), (-1, 1)], elves):
                    self.direction = 'W'
                    return
        # Nowhere is clear, no move in next round
        self.direction = ''

    def check_overlap(self, elves):
        for elf in elves:
            if elf.move_intention() == self.move_intention() and elf != self:
                self.overlapped = True
                elf.overlapped = True

    def move_intention(self):
        if self.direction == 'N':
            return (self.x, self.y - 1)
        elif self.direction == 'S':
            return (self.x, self.y + 1)
        elif self.direction == 'E':
            return (self.x + 1, self.y)
        elif self.direction == 'W':
            return (self.x - 1, self.y)
        else:
            return (self.x, self.y)

    def move(self):
        if self.direction == '':
            return False
        newx, newy = self.move_intention()
        if not self.overlapped:
            self.x = newx
            self.y = newy
            self.overlapped = False
            return True        
        self.overlapped = False
        return False

def print_elfgrid(elves):
    grid_left = min([elf.x for elf in elves]) 
    grid_right = max([elf.x for elf in elves])
    grid_top = max([elf.y for elf in elves])
    grid_bottom = min([elf.y for elf in elves])
    for y in range(grid_bottom, grid_top + 1):
        for x in range(grid_left, grid_right + 1):
            printed = False
            for elf in elves:
                if elf.x == x and elf.y == y:
                    print(elf.id, end='')
                    printed = True
                    break
            if not printed:
                print('.', end='')
        print('')

def print_diagnostics(elves, id):
    elf = [e for e in elves if e.id == id][0]
    print("Elf", elf.id, "at", elf.x, elf.y, "planned move direction", 
            elf.direction, "overlapped", elf.overlapped, 
            "move intention", elf.move_intention())

file = open('day23_input.txt', 'r')
lines = [s.strip() for s in file.readlines()]

elves = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '#':
            elves.append(Elf(x, y))

#print ("INITIAL STATE")
#print_elfgrid(elves)
#print("")
move_intentions = ['N', 'S', 'W', 'E']
any_move = True
round = 0
while any_move:
    move_count = 0
    round += 1
    any_move = False
    print("Performing move round", round)
    for elf in elves:
        elf.consider_move(elves, move_intentions)
    for elf in elves:
        elf.check_overlap(elves)
    for elf in elves:
        if elf.move():
            move_count += 1
            any_move = True
    #print("Completing round", round)
    #print_elfgrid(elves)
    #print("")
    rotate_dir = move_intentions.pop(0)
    move_intentions.append(rotate_dir)
    print(f"Round {round} completed with {move_count} moves")
    if round == 10:
        grid_left = min([elf.x for elf in elves]) 
        grid_right = max([elf.x for elf in elves])
        grid_top = max([elf.y for elf in elves])
        grid_bottom = min([elf.y for elf in elves])
        grid_width = grid_right - grid_left + 1
        grid_height = grid_top - grid_bottom + 1

        print("Answer 1:", (grid_width * grid_height) - len(elves))

print("Answer 2:", round)