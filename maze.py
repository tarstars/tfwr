def mult_move(dist, direction):
	for _ in range(dist):
		move(direction)

def nav(xd, yd):
	xc, yc = get_pos_x(), get_pos_y()
	n = get_world_size()

	east_dist = xd - xc
	if east_dist < 0:
		east_dist += n
	west_dist = n - east_dist

	north_dist = yd - yc
	if north_dist < 0:
		north_dist += n
	south_dist = n - north_dist

	if east_dist < west_dist:
		mult_move(east_dist, East)
	else:
		mult_move(west_dist, West)
	
	if north_dist < south_dist:
		mult_move(north_dist, North)
	else:
		mult_move(south_dist, South)

def predict_pos(direction):
	xc, yc = get_pos_x(), get_pos_y()
	if direction == East:
		return xc + 1, yc
	if direction == North:
		return xc, yc + 1
	if direction == West:
		return xc - 1, yc
	if direction == South:
		return xc, yc - 1

OPPOSITE = {East: West, West: East, North: South, South: North}

def create_maze():
	nav(16, 16)
	if can_harvest():
		harvest()
	plant(Entities.Bush)
	while not can_harvest():
		pass
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

def apply_proper_substance():
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def dfs(v):
	if (get_pos_x(), get_pos_y()) in v or get_entity_type() == Entities.Treasure:
		return

	v.add((get_pos_x(), get_pos_y()))
	for direction in [East, North, West, South]:
		if can_move(direction) and predict_pos(direction) not in v:
			move(direction)
			dfs(v)
			if get_entity_type() == Entities.Treasure:
				return
			move(OPPOSITE[direction])

def generate_money():
	while True:
		create_maze()
		for _ in range(29):
			dfs(set())
			apply_proper_substance()
		dfs(set())
		harvest()

# generate_money()
dfs(set())
harvest()
