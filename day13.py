import ast

file = open('day13_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

packets = []
list1 = None
list2 = None

for l in lines:
    if l.strip() == "":
        packets.append((list1, list2))
        list1 = None
        list2 = None
    else:
        if list1 == None:
            list1 = ast.literal_eval(l)
        else:
            list2 = ast.literal_eval(l)
packets.append((list1, list2))

EQUAL = 0
LESS_THAN = 1
GREATER_THAN = 2

def compare_packets(packet, indent):
    if type(packet[0]) == list or type(packet[1]) == list:
        # recursive call - convert to list if required
        if type(packet[0]) == list:
            left = packet[0]
        else:
            #print(indent + "left {} was not a list, converting to one".format(packet[0]))
            left = [packet[0]]
        if type(packet[1]) == list:
            right = packet[1]
        else:
            #print(indent + "right {} was not a list, converting to one".format(packet[1]))
            right = [packet[1]]
        #print(indent + "comparing {} and {}".format(left, right))
        for p in range(len(left)):
            if p == len(right):
                #print(indent + "Right ran out of packets - left is GREATER THAN")
                return GREATER_THAN
            comp = compare_packets((left[p], right[p]), indent + "  ")
            if comp != EQUAL:
                return comp
        if (len(right) > len(left)):
            #print(indent + "Left ran out of packets, left is LESS THAN")
            return LESS_THAN
        return EQUAL
    else:
        #print(indent + "comparing numbers. Left: " + str(packet[0]) + " right: " + str(packet[1]))
        if (packet[0] == packet[1]):
            #print(indent + "They are EQUAL")
            return EQUAL
        if (packet[0] > packet[1]):
            #print(indent + "LEFT Greater than RIGHT")
            return GREATER_THAN
        if (packet[0] < packet[1]):
            #print(indent + "LEFT Less than RIGHT")
            return LESS_THAN

true_indexes = []
for p in range(len(packets)):
   compare = compare_packets(packets[p], "")
   #print("")
   #print("")
   if compare == EQUAL or compare == LESS_THAN:
       true_indexes.append(p + 1)

print("Answer 1: " + str(sum(true_indexes)))

allpackets = []

for l in lines:
    if l.strip() != "":
        allpackets.append(ast.literal_eval(l))

allpackets.append([[2]])
allpackets.append([[6]])

# Bubble sort... I feel dirty
difference_found = True
while difference_found:
    difference_found = False
    for i in range(1, len(allpackets)):
        diff = compare_packets((allpackets[i - 1], allpackets[i]), "")
        if diff == GREATER_THAN:
            temp = allpackets[i - 1]
            allpackets[i - 1] = allpackets[i]
            allpackets[i] = temp
            difference_found = True

index1 = 0
index2 = 0
for p in range(len(allpackets)):
    if allpackets[p] == [[2]]:
        index1 = p + 1
    if allpackets[p] == [[6]]:
        index2 = p + 1

print("Answer 2: {}".format(index1 * index2))