file = open('day6_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

line = lines[0]

def unique_char_sequence_position(to_process, sequence_length):
    unique_chars = []
    for i in range(len(to_process)):
        ch = to_process[i]
        if ch in unique_chars:
            unique_chars = unique_chars[unique_chars.index(ch) + 1:]
        unique_chars.append(ch)
        if len(unique_chars) == sequence_length:
            return i + 1
    return -1

print("Answer 1:", unique_char_sequence_position(line, 4))
print("Answer 2:", unique_char_sequence_position(line, 14))


