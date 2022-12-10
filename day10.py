import sys

file = open('day10_input.txt', 'r')
commands = [tuple(s.strip('\n').split(' ')) for s in file.readlines()]

cycle_count = 0
x_reg = 1

reg_values_at_count = {}
reg_vals_required = [20, 60, 100, 140, 180, 220]

def check_reg(cyc, x, print_lines):
    if cyc in reg_vals_required:
        reg_values_at_count[cyc] = x * cyc
        #print("cyc", cyc, "x reg", x, "sig", x * cyc)
    line = (cyc - 1) // 40
    char = (cyc - 1) % 40
    #print(x, (char + 1))
    if abs(x - char) <= 1:
        print_lines[line][char] = "#"

print_lines = [[" "] * 40, [" "] * 40, [" "] * 40, [" "] * 40, [" "] * 40, [" "] * 40]

for c in commands:
    if c[0] == 'noop':
        cycle_count = cycle_count + 1
        check_reg(cycle_count, x_reg, print_lines)

    if c[0] == 'addx':
        cycle_count = cycle_count + 1
        check_reg(cycle_count, x_reg, print_lines)
        cycle_count = cycle_count + 1
        check_reg(cycle_count, x_reg, print_lines)
        x_reg = x_reg + int(c[1])

print("Answer 1:", sum(reg_values_at_count.values()))
print("Answer 2")
print("\n".join(["".join(l) for l in print_lines]))
