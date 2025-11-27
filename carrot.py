def go(nstep, direction):
	for _ in range(nstep):
		move(direction)

def nav(x1, y1):
	x0, y0 = get_pos_x(), get_pos_y()
	
	n = get_world_size()

	xe = (x1 - x0) % n
	xw = n - xe

	yn = (y1 - y0) % n
	ys = n - yn

	if xe < xw:
		go(xe, East)
	else:
		go(xw, West)
	
	if yn < ys:
		go(yn, North)
	else:
		go(ys, South)

count_not_ready = [0]

def drone_carrot(count_not_ready, x, y):
	nav(x, y)
	count_not_ready[0] -= 1
	while count_not_ready[0]:
		_ = measure()
	while True:
		while get_water() < 0.5:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		r = random()
		if r < 0.7:
			plant(Entities.Carrot)
		elif r < 0.8:
			plant(Entities.Tree)
		else:
			plant(Entities.Sunflower)
		move(North)

def bind(count_not_ready, f, a, b):
	def g(cnr=count_not_ready):
		f(cnr, a, b)
	return g

n = get_world_size()
nav(0, 0)
for x in range(n):
	if x == 0:
		continue
	if num_drones() < max_drones():
		count_not_ready[0] += 1
		spawn_drone(bind(count_not_ready, drone_carrot, x, 0))
count_not_ready[0] += 1
drone_carrot(0, 0)
