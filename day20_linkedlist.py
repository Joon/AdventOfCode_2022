file = open('day20_testinput.txt', 'r')
file_numbers = [int(s.strip('\n')) for s in file.readlines()]

distinct_numbers = set(file_numbers)
print(f"file count: {len(file_numbers)}, distinct count: {len(distinct_numbers)}")

class Node:
    seen_value_occurrence_count = {}

    def reset_tracking():
        Node.seen_value_occurrence_count = {}

    def __init__(self, value):
        self.value = value
        self.search_key = str(value) + '_' + str(Node.seen_value_occurrence_count.get(value, 0))
        Node.seen_value_occurrence_count[value] = Node.seen_value_occurrence_count.get(value, 0) + 1
        self.next = None
        self.previous = None

def find_node(search_key, head):
    node = head
    max_search = len(file_numbers)
    search = 0
    while node.search_key != search_key:
        node = node.next
        search += 1
        if search > max_search:
            raise Exception('search exceeded max')
    return node

def unlink_node(node):
    before = node.previous
    after = node.next
    before.next = after
    after.previous = before
    node.previous = None
    node.next = None

def scroll_nodes(base_node, move_amount):
    scroll_node = base_node
    if (move_amount == 0):
        return scroll_node

    if (move_amount > 0):
        for i in range(move_amount):
            scroll_node = scroll_node.next
            if (scroll_node.search_key == base_node.search_key):
                scroll_node = scroll_node.next
    else:
        for i in range(abs(move_amount)):
            scroll_node = scroll_node.previous
            if (scroll_node.search_key == base_node.search_key):
                scroll_node = scroll_node.previous
    return scroll_node


def move_node(node, move_amount):
    if move_amount == 0:
        return

    target_node = scroll_nodes(node, move_amount)
    if (target_node.search_key == node.search_key):
        print(f"target_node is node - no action for {move_amount}")
        return
    # Isolate node from its current position
    unlink_node(node)
    if (move_amount > 0):
        # Link node into its new position after target_node
        node.next = target_node.next
        node.previous = target_node
    else:
        # Link node into its new position before target_node
        node.next = target_node
        node.previous = target_node.previous
    node.next.previous = node
    node.previous.next = node       

def unpack_nodes(head):
    node = head.next
    unpacked = [head]
    while node.search_key != head.search_key:
        unpacked.append(node.value)
        node = node.next
    return unpacked

head = None
tail = None

for i in range(len(file_numbers)):
    node = Node(file_numbers[i])
    if head is None:
        head = node
        tail = node
    else:
        node.previous = tail
        tail.next = node
        tail = node

tail.next = head
head.previous = tail

process_count = {}
for i in range(len(file_numbers)):
    #print("Processing", file_numbers[i])
    search_key = str(file_numbers[i]) + '_' + str(process_count.get(file_numbers[i], 0))
    process_count[file_numbers[i]] = process_count.get(file_numbers[i], 0) + 1
    node = find_node(search_key, head)
    move_node(node, file_numbers[i])

result = unpack_nodes(head)
print(list(set(file_numbers) - set(result)))

result = 0
base_node = find_node("0_0", head)

for i in [1000, 2000, 3000]:
    found_node = scroll_nodes(base_node, i)
    decoded_number = found_node.value
    print(f"Number at {i}: {decoded_number}")
    result += decoded_number

print("Answer 1: ", result)

Node.reset_tracking()

head = None
tail = None

for i in range(len(file_numbers)):
    node = Node(file_numbers[i] * 811589153)
    if head is None:
        head = node
        tail = node
    else:
        node.previous = tail
        tail.next = node
        tail = node

tail.next = head
head.previous = tail

keys = {}
second_process_count = {}
for i in range(len(file_numbers)):
    search_key = str(file_numbers[i] * 811589153) + '_' + str(second_process_count.get(file_numbers[i] * 811589153, 0))
    second_process_count[file_numbers[i] * 811589153] = second_process_count.get(file_numbers[i] * 811589153, 0) + 1
    keys[i] = search_key

for process_range in range(10): 
    for i in range(len(file_numbers)):
        search_key = keys[i]
        node_to_move = find_node(search_key, head)
        move_node(node_to_move, file_numbers[i] * 811589153)

base_node = find_node("0_0", head)
result = 0
for i in [1000, 2000, 3000]:
    found_node = scroll_nodes(base_node, i)
    decoded_number = found_node.value
    print(f"Number at {i}: {decoded_number}")
    result += decoded_number

print("Answer 1: ", result)