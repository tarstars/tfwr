def go_best(ld, rd, ln, rn):
	d, n = [(ld, ln), (rd, rn)][rn < ln]
	for _ in range(n):
		move(d)

def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	go_best(West, East, (x1 - x2) % n, (x2 - x1)%n)
	go_best(South, North, (y1 - y2) % n, (y2 - y1)%n)

def set_earth_type(t):
	n = get_world_size()
	for y in range(n):
		for x in range(n):
			nav(x, y)
			if get_ground_type() != t:
				till()

# set_earth_type(Grounds.Soil)

while True:
	n = get_world_size()
	plan = dict()
	for y in range(n):
		for x in range(n):
			nav(x, y)
			plant(Entities.Sunflower)
			v = measure()
			if v not in plan:
				plan[v] = []
			plan[v].append((x, y))

	for v in range(15, 6, -1):
		if v in plan:
			for x, y in plan[v]:
				nav(x, y)
				while not can_harvest():
					pass
				harvest()
