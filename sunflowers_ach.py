def go_best(ld, rd, ln, rn):
	d, n = ld, ln
	if rn < ln:
		d, n = rd, rn
	for _ in range(n):
		move(d)


def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	go_best(West, East, (x1 - x2) % n, (x2 - x1)%n)
	go_best(South, North, (y1 - y2) % n, (y2 - y1)%n)


def till_soil():
	if get_ground_type() != Grounds.Soil:
		till()
		  

def each_column(f):
	drone_jobs = []

	for _ in range(max_drones()):
		drone_jobs.append([])
	
	for q in range(get_world_size()):
		drone_jobs[q % len(drone_jobs)].append(q)

	def drone_job(columns):
		def g():
			for q in columns:
				for p in range(get_world_size()):
					nav(q, p)
					f()
		return g
	
	while drone_jobs:
		while drone_jobs and num_drones() < max_drones():
			current = drone_jobs.pop()
			spawn_drone(drone_job(current))
		if drone_jobs:
			current = drone_jobs.pop()
			drone_job(current)()

 
def plant_sunflowers():
	drone_jobs = []

	for _ in range(max_drones()):
		drone_jobs.append([])
	
	for q in range(get_world_size()):
		drone_jobs[q % len(drone_jobs)].append(q)

	def drone_job(columns):
		def g():
			heights = dict()
			for q in columns:
				for p in range(get_world_size()):
					nav(q, p)
					plant(Entities.Sunflower)
					heights[(q, p)] = measure()
			return heights
		return g
	
	drones = []
	field_height = {}
	while drone_jobs:
		while drone_jobs and num_drones() < max_drones():
			current = drone_jobs.pop()
			drones.append(spawn_drone(drone_job(current)))
		if drone_jobs:
			current = drone_jobs.pop()
			result = drone_job(current)()
			for k in result:
				field_height[k] = result[k]
		for current_drone in drones:
			result = wait_for(current_drone)
			for k in result:
				field_height[k] = result[k]
	
	return field_height

def gather_all(cells):
	drone_jobs = []

	for _ in range(max_drones()):
		drone_jobs.append([])
	
	ind = 0
	for c in cells:
		drone_jobs[ind % len(drone_jobs)].append(c)
		ind += 1

	def drone_job(cells):
		def g():
			for q, p in cells:
					nav(q, p)
					while not can_harvest():
						pass
					harvest()
		return g
	
	while drone_jobs:
		while drone_jobs and num_drones() < max_drones():
			current = drone_jobs.pop()
			spawn_drone(drone_job(current))
		if drone_jobs:
			current = drone_jobs.pop()
			drone_job(current)()

each_column(till_soil)
while True:
	height_map = plant_sunflowers()
	height2cell = dict()
	for k in height_map:
		h = height_map[k]
		if h not in height2cell:
			height2cell[h] = []
		height2cell[h].append(k)
	for h in range(max(height2cell), min(height2cell) - 1, -1):
		if h in height2cell:
			gather_all(height2cell[h])
