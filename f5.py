

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

shouldWait = [True]

def drone_program(offset, shouldWait):
	shouldWait[0] = True
	nav(offset, 0)
	shouldWait[0] = False
	print("should wait false", shouldWait)
	while True:
		move(East)
		move(West)

def bind(offset, shouldWait, f):
	def g(o=offset, s=shouldWait):
		f(o, s)
	return g

nav(16, 16)
x = 1
while num_drones() < max_drones() - 1:
	shouldWait[0] = True
	spawn_drone(bind(x, shouldWait, drone_program))
	while shouldWait[0]:
		move(East)
		move(West)
	print("got should wait")
	x = x + 1
drone_program(0, shouldWait)

