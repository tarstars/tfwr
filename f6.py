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

def use_substance():
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def prepare_bush():
	nav(16, 16)
	plant(Entities.Bush)


def simulate_move(m):
	if m == West:
		return (get_pos_x() - 1, get_pos_y())
	if m == North:
		return (get_pos_x(), get_pos_y() + 1)
	if m == South:
		return (get_pos_x(), get_pos_y() - 1)
	if m == East:
		return (get_pos_x() + 1, get_pos_y())

BACK = {East:West, West:East, North:South, South:North}
ALL_DIRS = [East, West, South, North]

def dfs(v, s, h):
	v.add((get_pos_x(), get_pos_y()))
	if get_entity_type() == Entities.Treasure:
		s[0] = True
		if h:
			harvest()
		return
	for d in ALL_DIRS:
		if can_move(d) and simulate_move(d) not in v:
			move(d)
			dfs(v, s, h)
			if s[0]:
				return
			move(BACK[d])

prepare_bush()

for _ in range(29):
	visited = set()
	stop = [False]

	use_substance()
	dfs(visited, stop, False)
harvest()
