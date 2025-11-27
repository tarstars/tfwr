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
				
				
navigate(0, 0)
harvest()