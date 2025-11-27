set_world_size(3)

def go(d, pos, neg):
  direction = [pos, neg][d < 0]
  for _ in range(abs(d)):
	move(direction)

def nav(x2, y2):
	x1, y1 = get_pos_x(), get_pos_y()
	go(x2 - x1, East, West)
	go(y2 - y1, North, South)

nav(4, 5)

while True:
	pass