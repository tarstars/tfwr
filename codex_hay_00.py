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


def harvest_left_column():
	nav(0, 0)
	while num_items(Items.Hay) < 100000000:
		if can_harvest():
			harvest()
		move(North)


harvest_left_column()
