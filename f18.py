def go(d, pos, neg):
	if d > 0:
		for _ in range(d):
			move(pos)
	else:
		for _ in range(-d):
			move(neg)

def nav(x2, y2):
	x1, y1 = get_pos_x(), get_pos_y()
	dx, dy = x2 - x1, y2 - y1
	go(dx, East, West)
	go(dy, North, South)


def drone_job(x, y):
	nav(x, y)
	for _ in range(32):
		do_a_flip()

def bind(f, x, y):
	def g():
		f(x, y)
	return g
	
for x in range(4):
	for y in range(8):
		spawn_drone(bind(drone_job, x, y))