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

def prepare_soil(p):
	if p == Entities.Carrot and get_ground_type() != Grounds.Soil:
		till()  


def leader_loop():
	to_plant = []
	nav(0, 0)
	for y in range(8):
		nav(0, y)
		to_plant.append(get_companion())

	print(to_plant)

	for cur_plant, (x, y) in to_plant:
		if x != 0:
			nav(x, y)
			prepare_soil(cur_plant)
			plant(cur_plant)

	while num_items(Items.Hay) < 100000000:
		harvest()
		move(North)

set_world_size(8)

companions = {}
for x in range(8):
	for y in range(8):
		nav(x, y)
		companions[(x, y)] = get_companion()
print(companions)

while True:
	pass

