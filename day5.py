file = open('day5_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

def print_stacks(stacks):
    highest_stack = max([len(s) for s in stacks])
    print(' 1 2 3 4 5 6 7 8 9')
    for i in range(highest_stack):
        print_line = ''
        for s in stacks:
            append_char = ' '
            if len(s) > i:
                append_char = s[i]
            print_line = '{} {}'.format(print_line, append_char)
        print(print_line)

def build_stacks(lines):
    stacks = [[] for _ in range(9)] 
    for l in reversed(lines):
        for i in range(9):
            space_count = i
            prev_set_count = i * 3 if i > 0 else 0
            set_start = space_count + prev_set_count
            char_index = set_start + 1
            if l[char_index] != ' ':
                stacks[i].append(l[char_index])
    return stacks

def move_cratemover9000(stacks, command):
    command_tokens = command.split(' ')
    move_count = int(command_tokens[1])
    move_from = int(command_tokens[3])
    move_to = int(command_tokens[5])

    from_stack = stacks[move_from - 1]
    to_stack = stacks[move_to - 1]
    for i in range(move_count):
        crate = from_stack.pop()
        to_stack.append(crate)

def move_cratemover9001(stacks, command):
    command_tokens = command.split(' ')
    move_count = int(command_tokens[1])
    move_from = int(command_tokens[3])
    move_to = int(command_tokens[5])

    from_stack = stacks[move_from - 1]
    to_stack = stacks[move_to - 1]
    move_items = from_stack[(move_count * -1):]
    del from_stack[-move_count:]
    for crate in move_items:
        to_stack.append(crate)

orig_stacks = build_stacks(lines[0:8])

print("___ORIGINAL STACKS___")
print_stacks(orig_stacks)
for command in lines[10:]:
    move_cratemover9000(orig_stacks, command)

print("")
print("")

print("___STACKS MOVED BY CRATEMOVER 9000___")
print_stacks(orig_stacks)

print("")
print("")

print("Answer 1: ", "".join([s[-1] for s in orig_stacks]))

new_stacks = build_stacks(lines[0:8])
for command in lines[10:]:
    move_cratemover9001(new_stacks, command)

print("")
print("")

print("___STACKS MOVED BY CRATEMOVER 9001___")
print_stacks(new_stacks)

print("")
print("")

print("Answer 2: ", "".join([s[-1] for s in new_stacks]))

