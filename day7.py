file = open('day7_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

def calc_folder(input, current_folder):
    if input.startswith('/'):
        return input
    parts = current_folder.split('/')

    if current_folder == '/':
        parts = ['']

    if input == '..':
        parts.pop()
    else:
        parts.append(input)
    if len(parts) == 1:
        return '/'

    return '/'.join(parts)

def parent_folder(folder):
    key_parts = folder.split('/')
    key_parts.pop()
    if len(key_parts) == 1:
        return '/'
    return '/'.join(key_parts)

def add_empty_parents(dicto):
    found_empty = True
    while found_empty:
        found_empty = False
        folders = [k for k in dicto.keys()]
        for k in folders:
            parent = parent_folder(k)
            if not parent in dicto:
                dicto[parent] = 0
                found_empty = True

def roll_up_sizes(dicto):
    folders = [k for k in dicto.keys()]
    folders.sort()
    for k in reversed(folders):
        # root has no parent to add sizes to
        if k == '/':
            continue
        dicto[parent_folder(k)] = dicto[parent_folder(k)] + dicto[k]        

current_folder = ""
folder_sizes = {}

for part in lines:
    # Obey folder change commands
    if part.startswith('$ cd'):
        current_folder = calc_folder(part[5:], current_folder)
    # record file sizes
    if part[0].isnumeric():
        file_size = int(part.split(' ')[0])
        if current_folder in folder_sizes:
            folder_sizes[current_folder] = folder_sizes[current_folder] + file_size
        else:
            folder_sizes[current_folder] = file_size

add_empty_parents(folder_sizes)
roll_up_sizes(folder_sizes)

tot = 0
for v in folder_sizes.values():
    if v <= 100000:
        tot = tot + v

print("Answer 1", tot)

required_space = 70000000 - folder_sizes['/']
delete_size = 30000000 - required_space
vals = [v for v in folder_sizes.values() if v > delete_size]
print("Answer 2", min(vals))