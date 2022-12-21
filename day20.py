file = open('day20_input.txt', 'r')
file_numbers = [int(s.strip('\n')) for s in file.readlines()]

distinct_numbers = set(file_numbers)
print(f"file count: {len(file_numbers)}, distinct count: {len(distinct_numbers)}")

def copy_list_track_occurrence(l):
    occurrence_count = {}
    new_list = []
    for i in l:
        new_list.append(str(i) + '_' + str(occurrence_count.get(i, 0) + 1))
        occurrence_count[i] = occurrence_count.get(i, 0) + 1
    return new_list, occurrence_count

target, occurence_count = copy_list_track_occurrence(file_numbers)
for i in range(len(file_numbers)):
    search_key = str(file_numbers[i]) + '_' + str(occurence_count.get(file_numbers[i], 0))
    process_index = target.index(search_key)
    new_index = (process_index + file_numbers[i]) % (len(file_numbers) - 1)
    del target[process_index]
    target.insert(new_index, search_key)

#print(target)

result = 0
base_index = target.index("0_1")
print("First number after 0", target[(base_index + 1) % len(target)])
print("Second number after 0", target[(base_index + 2) % len(target)])
print("Third number after 0", target[(base_index + 3) % len(target)])
print("Fourth number after 0", target[(base_index + 4) % len(target)])
print("Fifth number after 0", target[(base_index + 5) % len(target)])
for i in [1000, 2000, 3000]:
    index = (base_index + i) % len(target)
    print(f"Number at {i}: {target[index]}")
    decoded_number = int(target[index].split('_')[0])
    result += decoded_number

print("Answer 1: ", result)