file1 = open('day1_input.txt', 'r')
lines = file1.readlines()

max_cal = 0
current_cal = 0
cals = []

for f in lines:
    line = f.strip()
    if line == "":
        if (current_cal > 0):
            cals.append(current_cal)
        current_cal = 0
    else:
        current_cal = current_cal + int(line)

if (current_cal > 0):
    cals.append(current_cal)

cals.sort()
biggest = cals[-3:]

print("Answer 1: {}".format(biggest[2]))
print("Answer 2: {}".format(biggest[0] + biggest[1] + biggest[2]))


