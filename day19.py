class Blueprint:
        def __init__(self, line):
            #Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
            parts = line.split(':')
            self.id = int(parts[0].split(' ')[1].strip(':'))
            bot_costs = [s.strip() for s in parts[1].split('.')]
            self.ore_bot_cost = int(bot_costs[0].split(' ')[4])
            self.clay_bot_cost = int(bot_costs[1].split(' ')[4])
            self.obsidian_bot_cost_ore = int(bot_costs[2].split(' ')[4])            
            self.obsidian_bot_cost_clay = int(bot_costs[2].split(' ')[7])
            self.geode_bot_cost_ore = int(bot_costs[3].split(' ')[4])
            self.geode_bot_cost_obsidian = int(bot_costs[3].split(' ')[7])

        def __str__(self):
            return f"Blueprint {self.id}: \n  Each ore robot costs {self.ore_bot_cost} ore.\n  Each clay robot costs {self.clay_bot_cost} ore.\n  Each obisidian robot costs {self.obsidian_bot_cost_ore} ore and {self.obsidian_bot_cost_clay} clay\n  Each geode robot costs {self.geode_bot_cost_ore} ore and {self.geode_bot_cost_obsidian} obsidian"

class MineState:
    def __init__(self, blueprint):
        self.geodes = 0
        self.ore = 0
        self.obsidian = 0
        self.clay = 0
        self.ore_bot_count = 1
        self.clay_bot_count = 0
        self.obsidian_bot_count = 0
        self.geode_bot_count = 0
        self.blueprint = blueprint
        self.building_ore_bot = False
        self.building_clay_bot = False
        self.building_obsidian_bot = False
        self.building_geode_bot = False

    def copy_values(self, copy_from):
        self.geodes = copy_from.geodes
        self.ore = copy_from.ore
        self.obsidian = copy_from.obsidian
        self.clay = copy_from.clay
        self.ore_bot_count = copy_from.ore_bot_count
        self.clay_bot_count = copy_from.clay_bot_count
        self.obsidian_bot_count = copy_from.obsidian_bot_count
        self.geode_bot_count = copy_from.geode_bot_count
        self.blueprint = blueprint
        self.building_ore_bot = copy_from.building_ore_bot
        self.building_clay_bot = copy_from.building_clay_bot
        self.building_obsidian_bot = copy_from.building_obsidian_bot
        self.building_geode_bot = copy_from.building_geode_bot
    
    def full_state_hash_key(self):
        return f"{self.ore},{self.obsidian},{self.clay},{self.bot_state_hash_key()}"

    def bot_state_hash_key(self):
        return f"{self.ore_bot_count}-{self.building_ore_bot},{self.clay_bot_count}-{self.building_clay_bot},{self.obsidian_bot_count}-{self.building_obsidian_bot},{self.geode_bot_count}-{self.building_geode_bot}"

    def can_manufacture_ore_bot(self):
        return self.ore >= self.blueprint.ore_bot_cost

    def can_manufacture_clay_bot(self):
        return self.ore >= self.blueprint.clay_bot_cost

    def can_manufacture_obsidian_bot(self):
        return self.ore >= self.blueprint.obsidian_bot_cost_ore and self.clay >= self.blueprint.obsidian_bot_cost_clay

    def can_manufacture_geode_bot(self):
        return self.ore >= self.blueprint.geode_bot_cost_ore and self.obsidian >= self.blueprint.geode_bot_cost_obsidian

    def manufacture_ore_bot(self):
        self.ore -= self.blueprint.ore_bot_cost
        self.building_ore_bot = True
    
    def manufacture_clay_bot(self):
        self.ore -= self.blueprint.clay_bot_cost
        self.building_clay_bot = True

    def manufacture_obsidian_bot(self):
        self.ore -= self.blueprint.obsidian_bot_cost_ore
        self.clay -= self.blueprint.obsidian_bot_cost_clay
        self.building_obsidian_bot = True

    def manufacture_geode_bot(self):    
        self.ore -= self.blueprint.geode_bot_cost_ore
        self.obsidian -= self.blueprint.geode_bot_cost_obsidian
        self.building_geode_bot = True

    def mine(self):
        self.ore += self.ore_bot_count
        self.clay += self.clay_bot_count
        self.obsidian += self.obsidian_bot_count
        self.geodes += self.geode_bot_count
        if self.building_ore_bot:
            self.ore_bot_count += 1
            self.building_ore_bot = False
        if self.building_clay_bot:
            self.clay_bot_count += 1
            self.building_clay_bot = False
        if self.building_obsidian_bot:
            self.obsidian_bot_count += 1
            self.building_obsidian_bot = False
        if self.building_geode_bot:
            self.geode_bot_count += 1
            self.building_geode_bot = False
            

def check_branches(mine_state, branch_hashes):
    new_states = []
    if mine_state.can_manufacture_geode_bot():
        new_state = MineState(mine_state.blueprint)
        new_state.copy_values(mine_state)
        new_state.manufacture_geode_bot()
        if (new_state.full_state_hash_key() not in branch_hashes):
            branch_hashes.add(new_state.full_state_hash_key())
            new_states.append(new_state)
    if mine_state.can_manufacture_obsidian_bot():
        new_state = MineState(mine_state.blueprint)
        new_state.copy_values(mine_state)
        new_state.manufacture_obsidian_bot()
        if (new_state.full_state_hash_key() not in branch_hashes):
            branch_hashes.add(new_state.full_state_hash_key())
            new_states.append(new_state)
    if mine_state.can_manufacture_ore_bot():
        new_state = MineState(mine_state.blueprint)
        new_state.copy_values(mine_state)
        new_state.manufacture_ore_bot()
        if (new_state.full_state_hash_key() not in branch_hashes):
            branch_hashes.add(new_state.full_state_hash_key())
            new_states.append(new_state)
    if mine_state.can_manufacture_clay_bot():
        new_state = MineState(mine_state.blueprint)        
        new_state.copy_values(mine_state)
        new_state.manufacture_clay_bot()
        if (new_state.full_state_hash_key() not in branch_hashes):
            branch_hashes.add(new_state.full_state_hash_key())
            new_states.append(new_state)
                
    return new_states

def prune_poor_branches(active_branches, min_geodes):
    result = []
    for branch in active_branches:
        if branch.geodes >= min_geodes:
            result.append(branch)
    return result

def run_simulation(blueprint, minutes, trim_offset):
    start_state = MineState(blueprint)
    branch_hashes = set()
    active_branches = [start_state]
    branch_hashes.add(start_state.bot_state_hash_key())
    for time in range(minutes):
        max_geodes = 0
        for branch in active_branches:
            if branch.geodes > max_geodes:
                max_geodes = branch.geodes
        print("Max geodes: " + str(max_geodes))
        active_branches = prune_poor_branches(active_branches, max_geodes - trim_offset)
        for branch in active_branches.copy():
            new_branches = check_branches(branch, branch_hashes)
            for new_branch in new_branches:
                new_branch.mine()
            branch.mine()
            if len(new_branches) > 0:
                active_branches.extend(new_branches)
        print(f"Minute {time}, {len(active_branches)} branches")
    max_geodes = 0
    for branch in active_branches:
        if branch.geodes > max_geodes:
            max_geodes = branch.geodes
    return max_geodes

file = open('day19_input.txt', 'r')
blueprints = [Blueprint(s.strip('\n')) for s in file.readlines()]

id_geodes = {}
for blueprint in blueprints:
    max_geodes = run_simulation(blueprint, 24, 0)
    id_geodes[blueprint.id] = max_geodes
    print(f"Blueprint {blueprint.id} can produce {max_geodes} geodes")

total_quality_level = 0
for blueprint in blueprints:
    blueprint_quality = blueprint.id * id_geodes[blueprint.id]
    total_quality_level += blueprint_quality

print(f"Answer 1: {total_quality_level}")

id_geodes = {}
total_quality_level = 1
for blueprint in blueprints[:3]:
    max_geodes = run_simulation(blueprint, 32, 2)
    total_quality_level *= max_geodes
    print(f"Blueprint {blueprint.id} can produce {max_geodes} geodes")

print(f"Answer 2: {total_quality_level}")
