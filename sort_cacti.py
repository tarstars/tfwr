def best_move(dl, dr, l, r):
	d, n = dl, l
	if r < n:
		d, n = dr, r
	for _ in range(n):
		move(d)

def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	best_move(East, West, (x2 - x1) % n, (x1 - x2)%n)
	best_move(North, South, (y2 - y1)%n, (y1 - y2)%n)

set_world_size(16)
nav(6, 6)

n = get_world_size()

# prepare soil for cacti
for y in range(n):
	nav(0, y)
	if get_ground_type() != Grounds.Soil:
		till()


# plant cacti
for y in range(n):
	nav(0, y)
	plant(Entities.Cactus)

# bubble sort
for y_upper in range(n - 1, 0, -1): # the last cell to swap with
	for y in range(y_upper):
		nav(0, y)
		if measure() > measure(North):
			swap(North) 


while True:
	pass
