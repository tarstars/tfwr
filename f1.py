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


def vertical_job(hor_offset):
	navigate(hor_offset,0)
	for turns in range(8):
		for x in range(32):
			for y in range(31):
				if measure() > measure(North):
					swap(North)
				move(North)
			move(North)
			move(East)
	
def horizontal_job(ver_offset):
	navigate(0, ver_offset)
	for turns in range(8):
		for y in range(32):
			for x in range(31):
				if measure() > measure(East):
					swap(East)
				move(East)
			move(East)
			move(North)


def vertical_cactus(hor_offset):
	navigate(hor_offset,0)
	for x in range(4):
		for y in range(32):
			plant(Entities.Cactus)
			move(North)
		move(East)
			
def create_job(offset, f):
	def g():
		f(offset)
	return g

def sort_cacti():
	navigate(0,0)
	for t in [vertical_job, horizontal_job]:
		for offset in [8, 16, 24]:
			spawn_drone(create_job(offset, t))
	
	spawn_drone(create_job(0, vertical_job))
	
	horizontal_job(0)

def plant_cacti():
	for x in range(4, 32, 4):
		spawn_drone(create_job(x, vertical_cactus))

	vertical_cactus(0)

while True:
	plant_cacti()
	sort_cacti()
	navigate(0, 0)
	harvest()