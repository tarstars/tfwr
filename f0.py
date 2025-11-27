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

def plant_tree():
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size() - 1, -1, -1)][x % 2]:
			navigate(x, y)
			harvest()
			if (x + y) % 2 == 0:
				plant(Entities.Tree)
				if get_water() < 0.3:
					use_item(Items.Water)
			

def harvest_tree():
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size() - 1, -1, -1)][x % 2]:
			navigate(x, y)
			if can_harvest():
				harvest()

def mine_trees():
	while True:
		for x in range(get_world_size()):
			for y in [range(get_world_size()), range(get_world_size() - 1, -1, -1)][x % 2]:
				if random() < 0.8:
					continue
				navigate(x, y)
				if can_harvest():
					harvest()
				while get_water() < 0.8:
						use_item(Items.Water)
				r = random()
				if get_ground_type() == Grounds.Soil:
					if r < 0.5:
						plant(Entities.Sunflower)
					else:
						plant(Entities.Tree)
				

	
def mine_grass():
	while True:
		for x in range(2):
			if x % 2 == 0:
				for y in range(6):
					navigate(x, y)
					harvest()
			else:
				for y in range(5, -1, -1):
					navigate(x, y)
					harvest()

def till_field():
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			till()

def plant_cacti():
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			plant(Entities.Cactus)
			

def harvest_field():
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			harvest()
			
				
def mine_carrot():
	while True:
		for x in range(get_world_size()):
			for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
				navigate(x, y)
				harvest()
				r = random()
				if get_ground_type() == Grounds.Grassland:
					harvest()
					if r < 0.5:
						plant(Entities.Tree)
				else:
					if r < 0.1:
						plant(Entities.Sunflower)
					else:
						plant(Entities.Carrot)
					

def plant_pumpkin():
	todo = True
	while todo:
		todo = False
		for x in range(get_world_size()):
			for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
				navigate(x, y)
				if not can_harvest():
					plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)	
					todo = True
	harvest()


def mine_pumpkin():			
	while True:
		plant_pumpkin()

def till_small_patch():		
	for x in range(2):
		for y in [range(3), range(2, -1, -1)][x%2]:
			navigate(x,y)
			till()

def grass_small_patch():		
	for x in range(2):
		for y in [range(3), range(2, -1, -1)][x%2]:
			navigate(x,y)
			harvest()

def mine_grass():
	while True:
		grass_small_patch()

def till_random(percent):
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			r = random()
			if r < percent:
				till()

def set_earth_type(t):
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			if get_ground_type() != t:
				till() 
				

def measure_field():
	heights = {}
	for x in range(get_world_size()):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			heights[(y,x)] = measure()
	return heights
					
def hor_scan():
	move = False
	for x in range(get_world_size()-1):
		for y in [range(get_world_size()), range(get_world_size()-1, -1, -1)][x % 2]:
			navigate(x, y)
			if measure() > measure(East):
				swap(East)
				move = True

	return move

def ver_scan():
	move = False
	for x in range(get_world_size()):
		for y in [range(get_world_size()-1), range(get_world_size()-2, -1, -1)][x % 2]:
			navigate(x, y)
			if measure() > measure(North):
				swap(North)
				move = True

	return move


def mine_cacti():
	a = measure_field()
	while hor_scan() or ver_scan():
		pass
	navigate(0,0)	
	harvest()

def apple_hunt_turn():
	for x in range(get_world_size()):
		for y in [range(1, get_world_size()), range(get_world_size(), 0, -1)][x % 2]:
			navigate(x,y)
	for x in range(get_world_size() - 1, -1, -1):
		navigate(x, 0)

def apple_hunt():
	while True:
		apple_hunt_turn()	


	
opposite = {East: West, West: East, North: South, South: North}
	
def dfs(visited, stop):		
	if stop[0]:
		return

	visited[(get_pos_x(), get_pos_y())] = 1
	
	def dfs_bound(v=visited, s=stop):
		dfs(v, s)
			
	if get_entity_type() == Entities.Treasure:
		harvest()
		stop[0] = True
		return
		
	for dir in [East, West, South, North]:
		if stop[0]:
			return
		if can_move(dir):
			move(dir)
			npos = (get_pos_x(), get_pos_y())
			if npos not in visited:
				visited[npos] = 1
				if num_drones() < max_drones():
					spawn_drone(dfs_bound)
				else:
					dfs(visited, stop)
			if stop[0]:
				return		
			move(opposite[dir])
	if not stop[0]:
		visited[(get_pos_x(), get_pos_y())] = 2


def spawn_maze():
	navigate(10, 10)
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	visited = {}
	stop = [False]
	dfs(visited, stop)

navigate(20, 0)

def travel_north():
	for _ in range(100):
		if can_harvest():
			harvest()
		if get_ground_type() == Grounds.Soil:
			plant(Entities.Sunflower)
		move(North)

def mine_grass():
	while True:
		for _ in range(10):
			move(West)
			harvest()
			if num_drones() < max_drones():
				spawn_drone(travel_north)


def multy_tree():
	navigate(0, 0)
	while num_drones() < max_drones():
		spawn_drone(mine_trees)
		move(East)
		move(East)
	mine_trees()			
			
multy_tree()					
#spawn_maze()

#visited = {}
#stop = [False]
#dfs(visited, stop)
	
	
	#while True:	
#	spawn_maze()

				
							
#change_hat(Hats.Dinosaur_Hat)	
#apple_hunt()
#change_hat(Hats.Cactus_Hat)		
#plant_cacti()
#set_earth_type(Grounds.Soil)							
#till_random(0.3)
#harvest_field()
#mine_pumpkin()						
#till_field()					
#mine_carrot()				
#mine_trees()
#mine_grass()
#till_small_patch()
