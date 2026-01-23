set_world_size(6)

l = {East:North, North:West, West:South, South:East}
r = {East:South, South:West, West:North, North:East}

while True:
	# black magic to conjure the maze
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	dc = East
	while get_entity_type() != Entities.Treasure:
		dc = l[dc]
		while not move(dc):
			dc = r[dc]
	
	harvest()
	