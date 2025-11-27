set_world_size(8)


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


def harvest_tree_for_wood():
	if get_entity_type() != Entities.Tree:
		plant(Entities.Tree)
	while get_entity_type() == Entities.Tree and not can_harvest():
		move(North)
		move(South)
	if get_entity_type() == Entities.Tree and can_harvest():
		harvest()


def plant_companions_for_left_column():
	n = get_world_size()
	for y in range(n):
		nav(0, y)
		info = get_companion()
		if info != None:
			entity, (tx, ty) = info
			if tx != 0:
				nav(tx, ty)
				if entity == Entities.Carrot:
					harvest_tree_for_wood()
				ensure_ground(entity)
				plant(entity)


def harvest_left_column():
	nav(0, 0)
	plant_companions_for_left_column()
	nav(0, 0)
	while num_items(Items.Hay) < 100000000:
		if can_harvest():
			harvest()
		move(North)


harvest_left_column()
