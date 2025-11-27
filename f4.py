#set_world_size(8)
#set_execution_speed(8)

def nav(xd, yd):
	n = get_world_size()
	xc, yc = get_pos_x(), get_pos_y()
	dx = abs(xd - xc)
	dy = abs(yd - yc)	

	xdir = East
	if (xd < xc) != (n - dx < dx):
		xdir = West
	
	ydir = North
	if (yd < yc) != (n - dy < dy):
		ydir = South
	
	for _ in range(min(dx, n - dx)):
		move(xdir)
	
	for _ in range(min(dy, n - dy)):
		move(ydir)
	

def drone_job_set_soil_proba(x_offset):
	for y in range(get_world_size()):
		nav(x_offset, y)
		if random() < 0.2:
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()

def drone_job_prepare_for_trees(x_offset):
	for y in range(get_world_size()):
		nav(x_offset, y)
		if random() < 0.7:
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()
				

def drone_job_harvest(x_offset):
	while True:
		for y in range(get_world_size()):
			nav(x_offset, y)
			if random() < 0.1:
				continue

			if can_harvest():
				harvest()

			if get_ground_type() == Grounds.Soil:
				if get_entity_type() == None:
					plant(Entities.Sunflower)
				while get_water() < 0.75:
					use_item(Items.Water)

def drone_job_one_harvest(x_offset):
	for y in range(get_world_size()):
		nav(x_offset, y)
		if can_harvest():
			harvest()



def bound(x, f):
	def g():
		f(x)
	return g

def do_job(j):
	for x in range(1, max_drones()):
		spawn_drone(bound(x, j))

	j(0)			

def grass_sun():
	nav(0, 0)
	do_job(drone_job_set_soil_proba)
	while num_drones() > 1:
		move(East)
		move(West)
	do_job(drone_job_harvest)		

def one_harvest():
	do_job(drone_job_one_harvest)

do_job(drone_job_prepare_for_trees)	

# one_harvest()
#grass_sun()

#nav(3, 2)
#print(get_entity_type())