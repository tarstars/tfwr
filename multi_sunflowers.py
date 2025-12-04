def go_best(ld, rd, ln, rn):
	d, n = [(ld, ln), (rd, rn)][rn < ln]
	for _ in range(n):
		move(d)

def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	go_best(West, East, (x1 - x2) % n, (x2 - x1)%n)
	go_best(South, North, (y1 - y2) % n, (y2 - y1)%n)
	
	
def f(column):
	def g():
		one_drone_plant_job(column)
	return g

def one_drone_plant_job(column):
	n = get_world_size()
	for y in range(n):
		nav(column, y)
		if can_harvest():
			harvest()
		if get_ground_type() == Grounds.GrassLand:
			till()
		plant(Entities.Sunflower)
	
while True:
	tasks = []
	for t in range(get_world_size()):
		tasks.append(t)	
	  
	while tasks:
		t = tasks.pop()
		while num_drones() == 18: # max_drones():
			pass
		spawn_drone(f(t))
	  
 