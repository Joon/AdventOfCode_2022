file1 = open('day3_input.txt', 'r')
lines = [s.strip() for s in file1.readlines()]

def half_string(s):
    return [s[0:int(len(s) / 2)], s[int(len(s) / 2):]]

def match_item(ss):
    for i in range(len(ss[0])):
        if ss[0][i] in ss[1]:
            return ss[0][i]

def match_item3(sss):
    for i in range(len(sss[0])):
        if sss[0][i] in sss[1] and sss[0][i] in sss[2]:
            return sss[0][i]


def score(c):
    if c == c.lower():
        return (ord(c) - ord('a')) + 1
    else:
        return (ord(c) - ord('A')) + 27

halves = [half_string(s) for s in lines]
matched = [match_item(h) for h in halves]

# Mad bit of code I found at https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n
# Explanation from Tomas G (https://stackoverflow.com/users/9047701/tomas-g)
# (iter(the_list),) is a tuple. (iter(the_list),)*3 is a tuple with three references to 
# the same iterator. We use a starred expression *(...) to pass the three references to 
# the iterators to zip as arguments. zip basically does a matrix transpose of the 
# arguments given.
group_lines = [s for s in zip(*(iter(lines),) * 3)]

badges = [match_item3(sss) for sss in group_lines]

print("Answer 1: {}".format(sum([score(m) for m in matched])))

print("Answer 2: {}".format(sum([score(b) for b in badges])))