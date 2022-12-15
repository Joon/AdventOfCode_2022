from itertools import chain
from itertools import combinations

file = open('day15_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

process_points = []

for l in lines:
    parts = l.split(' ')
    sensor_x = int(parts[2].split('=')[1][:-1])
    sensor_y = int(parts[3].split('=')[1][:-1])
    beacon_x = int(parts[8].split('=')[1][:-1])
    beacon_y = int(parts[9].split('=')[1])
    process_points.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))

sensor_beacon = {}
sensor_range = {}

def tuple_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def tuple_subtract(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1])

def tuple_distance(t1, t2):
    # Calculate manhattan distance for two positions
    distance_components = tuple_subtract(t1, t2)
    return abs(distance_components[0]) + abs(distance_components[1])

processed = 0
tot = len(process_points)
sensors = []
for r in process_points:    
    sensor_beacon[r[0]] = r[1]
    dist = tuple_distance(r[0], r[1])
    sensor_range[r[0]] = dist
    sensors.append(r[0])

def count_no_beacons(line):
    possible_sensors = [s for s in sensor_beacon.keys() if s[1] + tuple_distance(s, sensor_beacon[s]) >= line 
                                                        and s[1] - tuple_distance(s, sensor_beacon[s]) <= line]
    no_beacon = set([])
    beacon = [b[0] for b in sensor_beacon.values() if b[1] == line]
    for line_sensor in [s[0] for s in sensor_beacon.keys() if s[1] == line]:
        no_beacon.add(line_sensor)
    for s in possible_sensors:
        # How far is this sensor from its beacon
        dist = tuple_distance(s, sensor_beacon[s])
        # we only have to cover the range not covered by how far the sensor is away
        to_cover = dist     
        for x in range(s[0] - to_cover, s[0] + to_cover):
            if x in no_beacon:
                continue
            if tuple_distance(s, (x, line)) <= dist:
                if x not in beacon:
                    no_beacon.add(x)
    return len(no_beacon)


print("Counting Answers")
print("Answer 1:", count_no_beacons(2000000))

print("Finding emergency beacon")
MAX_VAL = 4000000

found = False
# Scan a point along the grid
current_point = (0, 0)
while True:
    inside = False
    for i in range(len(sensors)):
        s = sensors[i]
        dist = sensor_range[s]
        if tuple_distance(current_point, s) <= dist:
            inside = True
            if current_point[1] <= s[1]:
                multiplier = 1
            else:
                multiplier = -1
            boundary = s[1] - multiplier * (s[0] + dist)
            x = int((current_point[1] - boundary) / multiplier)
            # Skip the point over the coverage of the sensor
            current_point = (x + 1, current_point[1])
            if current_point[0] >= MAX_VAL:
                # Wrap to the next line
                current_point = (0, current_point[1] + 1)
            break
    if not inside:
        print("Answer 2: " + str(current_point[0] * 4000000 + current_point[1]))
        break