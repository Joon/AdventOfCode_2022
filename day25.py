file = open('day25_input.txt', 'r')
lines = [s.strip() for s in file.readlines()]

snafu_symbol = {
    2: '2',
    1: '1',
    0: '0',
    -1: '-',
    -2: '='
}

snafu_symbol_to_power = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

def snafu_to_decimal(snafu):
    powers_of_five = [snafu_symbol_to_power[s] for s in snafu]
    powers_of_five.reverse()
    val = 0
    for power, num in enumerate(powers_of_five):
        val += num * pow(5, power)
    return val

def decimal_to_snafu(decimal):
    if decimal == 0:
        return '0'
    snafu = ''
    # To convert to SNAFU, first we unpack the decimal number into powers of 5. We just cheat and hardcode 
    # an array size here, if the number is larger than 5^32, we will have a problem.
    powers_of_five = [0] * 32
    for poors in range(len(powers_of_five) - 1, -1, -1):
        current_divisor = pow(5, poors)
        power_val = decimal // current_divisor
        decimal = decimal - (power_val * current_divisor)
        powers_of_five[poors] = power_val

    # The SNAFU format requires that the power of 5 get transferred to the next power of 5 for values
    # greater than 2, because it does not allow the numbers 4 or 3 to be represented. Therefore, we
    # walk through from the smallest to largest power of 5, and if the value is greater than 2, we
    # increment the next power of 5, and decrement the current power of 5 by 5.
    # For example:
    # decimal 20 in powers of 5 is 0 ones and 4 fives
    # because 4 is not allowed, this becomes 1 25's and -1 5's
    for p, val in enumerate(powers_of_five):
        if p == len(powers_of_five) - 1:
            break
        if val >= 3:
            powers_of_five[p] = val -5
            powers_of_five[p + 1] += 1
    highest_power = max([i for i, p in enumerate(powers_of_five) if p != 0])
    for i in range(highest_power + 1):
        v = powers_of_five[i]
        snafu = snafu_symbol[v] + snafu
    return snafu

total = 0
for l in lines:
    total += snafu_to_decimal(l)

print("Part 1", decimal_to_snafu(total))