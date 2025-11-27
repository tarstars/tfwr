set_world_size(3)


def go(steps, direction):
	for _ in range(steps):
		move(direction)


def nav(x, y):
	n = get_world_size()
	x0 = get_pos_x()
	y0 = get_pos_y()

	dx = (x - x0) % n
	dx_alt = (x0 - x) % n
	dy = (y - y0) % n
	dy_alt = (y0 - y) % n

	if dx <= dx_alt:
		go(dx, East)
	else:
		go(dx_alt, West)

	if dy <= dy_alt:
		go(dy, North)
	else:
		go(dy_alt, South)


def ensure_ground(entity):
	if entity == Entities.Carrot and get_ground_type() != Grounds.Soil:
		till()


def wait_tree_ready():
	while get_entity_type() == Entities.Tree and not can_harvest():
		move(North)
		move(South)


def plant_and_harvest_trees():
	if get_entity_type() != Entities.Tree:
		plant(Entities.Tree)
	wait_tree_ready()
	if get_entity_type() == Entities.Tree and can_harvest():
		harvest()


def satisfy_center_companion():
	nav(1, 1)
	info = get_companion()
	if info == None:
		return
	entity, (tx, ty) = info
	nav(tx, ty)
	if entity == Entities.Carrot:
		if get_entity_type() == Entities.Tree and can_harvest():
			harvest()
		elif get_entity_type() == Entities.Tree and not can_harvest():
			wait_tree_ready()
			if get_entity_type() == Entities.Tree and can_harvest():
				harvest()
	ensure_ground(entity)
	if get_entity_type() != entity:
		plant(entity)


def harvest_center_grass():
	nav(1, 1)
	while num_items(Items.Hay) < 100000000:
		if can_harvest():
			harvest()
		move(North)
		move(South)


plant_and_harvest_trees()
satisfy_center_companion()
harvest_center_grass()
