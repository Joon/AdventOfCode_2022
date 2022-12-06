file = open('day6_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

line = lines[0]

def process_string(to_process, sequence_length):
    processed = []
    for i in range(len(to_process)):
        ch = to_process[i]
        if ch in processed:
            processed = processed[processed.index(ch) + 1:]
        processed.append(ch)
        if len(processed) == sequence_length:
            print(i+1)
            break

print("Answer 1:")
process_string(line, 4)
print("Answer 2:")
process_string(line, 14)


