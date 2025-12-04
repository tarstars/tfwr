def navigate(x, y):
	dx = x - get_pos_x()
	dy = y - get_pos_y()
	if dx:
		if dx > 0:
			for _ in range(dx):
				move(East)
		else:
			for _ in range(-dx):
				move(West)
	if dy:
		if dy > 0:
			for _ in range(dy):
				move(North)
		else:
			for _ in range(-dy):
				move(South)

def ensure_plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Pumpkin)

def create_pieces():
	replant = []
		
	n = get_world_size()
	for x in range(n):
		for y in [range(n), range(n-1, -1, -1)][x%2]:
			replant.append((x,y))
	
	n_drones = max_drones()
	piece_length = len(replant) // n_drones
	
	pieces = []
	
	for piece_index in range(n_drones):
		pieces.append(replant[piece_length * piece_index:[piece_length * (piece_index + 1), len(replant)][piece_index == n_drones - 1]])
	
	return pieces
				
def one_drone_job_pumpkin(piece):	
	while piece:
		x, y = piece.pop(0)
		navigate(x,y)
		if get_entity_type() == Entities.Pumpkin and can_harvest():
			continue
		while get_entity_type() == Entities.Pumpkin and not can_harvest():
			move(East)
			navigate(x,y) 
		ensure_plant_pumpkin()
		piece.append((x,y))

def one_drone_job_sunflower(piece):	
	while True:
		for x, y in piece:
			navigate(x,y)
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() != Entities.Sunflower:
				plant(Entities.Sunflower)
			if can_harvest():
				harvest()
				plant(Entities.Sunflower)
		

def one_drone_job_plant_cactus(piece):	
	for x, y in piece:
		navigate(x,y)
		plant(Entities.Cactus)

def one_drone_job_carrot(piece):	
	while True:
		for x, y in piece:
			navigate(x,y)
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() != Entities.Sunflower:
				plant(Entities.Carrot)
			if can_harvest():
				harvest()
				if random() < 0.2:
					plant(Entities.Sunflower)
				else:
					plant(Entities.Carrot)

def one_drone_job_harvest(piece):	
	for x, y in piece:
		navigate(x,y)
		harvest()													

def one_drone_job_till(piece):	
	for x, y in piece:
		navigate(x,y)
		if get_ground_type() != Grounds.Soil:
			till()													
		

def create_drone_function(piece, f):
	def perform_job():
		f(piece)
	return perform_job

def grow_mega(f):
	farm_pieces = create_pieces()
	
	farm_jobs = []
	for p in farm_pieces:
		farm_jobs.append(create_drone_function(p, f))
	
	for p in farm_jobs[1:]:
		spawn_drone(p)
	
	farm_jobs[0]()
	
	while num_drones() > 1:
		move(East)
		move(West)
	
	harvest()

def fast_harvest():
	farm_pieces = create_pieces()
	
	farm_jobs = []
	for p in farm_pieces:
		farm_jobs.append(create_drone_function(p, one_drone_job_harvest))
	
	for p in farm_jobs[1:]:
		spawn_drone(p)
	
	farm_jobs[0]()
	
	while num_drones() > 1:
		move(East)
		move(West)

def fast_till():
	farm_pieces = create_pieces()
	
	farm_jobs = []
	for p in farm_pieces:
		farm_jobs.append(create_drone_function(p, one_drone_job_till))
	
	for p in farm_jobs[1:]:
		spawn_drone(p)
	
	farm_jobs[0]()
	
	while num_drones() > 1:
		move(East)
		move(West)
		

def mega_harvest(f):
	while True:
		grow_mega(f)

def companion_harvest():
	positions_order = [(get_pos_x(), get_pos_y())]
	posiitons_set = set(positions_order)
	
	if get_companion() == None:
		plant(Entities.Tree)
	
	requirement = {
		Entities.Grass: Grounds.Grassland,
		Entities.Bush: "OK",
		Entities.Carrot: Grounds.Soil,
		Entities.Tree: "OK"
	}
	
	for iter_num in range(100):
		plant_companion, (x,y) = get_companion()
		navigate(x, y)
		if requirement[plant_companion] != "OK" and get_ground_type() != requirement[plant_companion]:
			till()
		positions_order.append((x, y))
		posiitons_set.add((x, y))
		plant(plant_companion)
		
	for x, y in positions_order:
		navigate(x, y)
		while not can_harvest():
			move(West)
			move(East)
		harvest()
		
#move(West)		
#while True:
#	companion_harvest()
mega_harvest(one_drone_job_sunflower)
#harvest()
#fast_harvest()
#fast_till()