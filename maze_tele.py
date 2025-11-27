def go_best(d1, d2, l1, l2):
	d, l = d1, l1
	if l2 < l1:
		d, l = d2, l2
	for _ in range(l):
		move(d)


def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	go_best(East, West, (x2 - x1)%n, (x1 - x2)%n)
	go_best(North, South, (y2 - y1)%n, (y1 - y2)%n)

def apply_proper_substance():
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


set_world_size(8)
nav(3, 3)
plant(Entities.Bush)
apply_proper_substance()

DIRECTIONS=[East, North, South, West]
OPPOSITE={East:West, West:East, North:South, South:North}

def dfs(visited):
	if (get_pos_x(), get_pos_y()) in visited:
		return

	if get_entity_type() == Entities.Treasure:
		return
   
	visited.add((get_pos_x(), get_pos_y()))

	for dir_to_move in DIRECTIONS:
		if can_move(dir_to_move):
			move(dir_to_move)
	
			dfs(visited)
			if get_entity_type() == Entities.Treasure:
				return

			move(OPPOSITE[dir_to_move])

for _ in range(30):
	visited = set()
	dfs(visited)
	apply_proper_substance()

visited = set()
dfs(visited)
harvest()

while True:
	pass
