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

def wait_forever():
	while True:
		pass


set_world_size(8)
smile = [(0, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7,2), (2,5), (5,5)]

for x,y in smile:
	nav(x, y)
	spawn_drone(wait_forever)
