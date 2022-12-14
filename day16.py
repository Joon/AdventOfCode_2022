import itertools


file = open('day16_input.txt', 'r')
lines = [s.strip('\n') for s in file.readlines()]

flow_rates = {}
paths = {}

for l in lines:
    # Valve BB has flow rate=13; tunnels lead to valves CC, AA
    parts = l.split(' ')
    valve = parts[1]
    flow_rates[valve] = int(parts[4].strip('rate=;'))
    paths[valve] = [v.strip(',') for v in parts[9:]]

processed_paths = list({})

INFINITE = 9999999

def dijkstra(targets, source):
    dist = {}
    previous = {}
    if targets.count(source) == 0:
        targets.append(source)
    for v in targets:
        dist[v] = INFINITE
        previous[v] = None
    dist[source] = 0
    Q = targets.copy()
    while len(Q) > 0:
        target_dist = min([dist[n] for n in Q])
        u = [n for n in Q if dist[n] == target_dist][0]
        Q.remove(u)
        for v in paths[u]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                previous[v] = u
    return previous, dist

def shortest_path(source, target):
    previous, dist = dijkstra(all_valves, source)
    path = []
    u = target
    while previous[u] is not None:
        path.append(u)
        u = previous[u]
    path.append(source)
    path.reverse()
    return path

def path_time(path):
    return len(path) + len([p for p in path if "*" in p])

def all_paths(current_pos, remaining_valves, path):
    # filter out useless valves
    for r in remaining_valves.copy():
        if flow_rates[r] == 0:
            remaining_valves.remove(r)

    if path_time(path) >= 30:
        return [path]

    if remaining_valves == []:
        return [path]
    paths = []
    for candidate in remaining_valves:
        nav_to = candidate
        new_path = path.copy()
        for n in shortest_path(current_pos, nav_to)[1:]:
            new_path.append(n)
            if n == nav_to:
                new_remaining_valves = remaining_valves.copy()
                new_remaining_valves.remove(n)
                new_path[-1] = new_path[-1] + "*"                
                for pt in all_paths(n, new_remaining_valves, new_path):
                    paths.append(pt)    
                
    return paths

def path_flow(path):
    try:
        total_flow = 0
        cumulative_rate = 0
        time = 0
        for p in path:
            time = time + 1
            total_flow = total_flow + cumulative_rate
            if time == 30:
                return total_flow
            if "*" in p:
                time = time + 1
                total_flow = total_flow + cumulative_rate
                cumulative_rate = cumulative_rate + flow_rates[p[:-1]]
                if time == 30:
                    return total_flow
        return total_flow + (30 - time) * cumulative_rate
    except:    
        return 0

# def all_combined_paths(current_human_pos, current_elephant_pos, remaining_valves, human_path, elephant_path):
#     # filter out useless valves
#     for r in remaining_valves.copy():
#         if flow_rates[r] == 0:
#             remaining_valves.remove(r)

#     if path_time(human_path) >= 26:
#         return ([human_path], [elephant_path])

#     if remaining_valves == []:
#         return ([human_path], [elephant_path])
#     paths = ([], [])
#     valve_combos = itertools.combinations(remaining_valves, 2)
#     for candidate in valve_combos:
#         human_nav_to = candidate[0]
#         elephant_nav_to = candidate[1]
#         new_human_path = human_path.copy()
#         new_elephant_path = elephant_path.copy()
#         # TODO: combine paths while either path still has work to do
#         elephant_steps = shortest_path(current_elephant_pos, elephant_nav_to)[1:]
#         human_steps = shortest_path(current_human_pos, human_nav_to)[1:]
#         for n in 
#             new_path.append(n)
#             if n == nav_to:
#                 new_remaining_valves = remaining_valves.copy()
#                 new_remaining_valves.remove(n)
#                 new_path[-1] = new_path[-1] + "*"                
#                 for pt in all_paths(n, new_remaining_valves, new_path):
#                     paths.append(pt)    
                
#     return paths

all_valves = [k for k in flow_rates.keys() if k != 'AA']
print("Calculating all possible paths that open all valves or reach 30 minutes")
all_paths = all_paths('AA', all_valves.copy(), [])
print("Path count", len(all_paths))
max_flow = 0
print("Calculating max flow achieved in each path")

for p in all_paths:    
    if path_flow(p) > max_flow:
        max_flow = path_flow(p)
print("Answer 1", max_flow)
