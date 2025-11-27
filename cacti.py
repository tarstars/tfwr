
def go(n, direction):
	for _ in range(n):
		move(direction)

def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	xe = (x2 - x1) % n
	xw = n - xe
	yn = (y2 - y1) % n
	ys = n - yn
	if xe < xw:
		go(xe, East)
	else:
		go(xw, West)
	if yn < ys:
		go(yn, North)
	else:
		go(ys, South)

def job_plant_cacti(x):
	nav(x, 0)
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		move(North)

def job_sort_cacti(x):
	nav(x, 0)
	n = get_world_size()
	for _ in range(n):
		for y in range(n):
			if x < n - 1:
				if measure() > measure(East): 
					swap(East)
			if y < n - 1:
				if measure() > measure(North):
					swap(North)
			move(North)
		


def bind1(f, a):
	def g():
		f(a)
	return g

def run_all(f):
	for x in range(1, get_world_size()):
		if num_drones() < max_drones():
			spawn_drone(bind1(f, x))

	f(0)

nav(0, 0)
run_all(job_plant_cacti)
run_all(job_sort_cacti)
nav(0, 0)
harvest()