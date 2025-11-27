set_world_size(8)


def go(steps, direction):
	for _ in range(steps):
		move(direction)


def nav(x, y):
	n = get_world_size()
	x0 = get_pos_x()
	y0 = get_pos_y()

	dx = (x - x0) % n
	dx_alt = (x0 - x) % n
	dy = (y - y0) % n
	dy_alt = (y0 - y) % n

	if dx <= dx_alt:
		go(dx, East)
	else:
		go(dx_alt, West)

	if dy <= dy_alt:
		go(dy, North)
	else:
		go(dy_alt, South)


def ensure_ground(entity):
	if entity == Entities.Carrot and get_ground_type() != Grounds.Soil:
		till()


def ensure_tree_here():
	if get_entity_type() != Entities.Tree:
		if can_harvest():
			harvest()
		if get_entity_type() != Entities.Tree:
			plant(Entities.Tree)


def plant_checkered_trees():
	n = get_world_size()
	for x in range(n):
		for y in range(n):
			nav(x, y)
			if (x + y) % 2 == 0:
				ensure_tree_here()


def harvest_checkered_trees():
	n = get_world_size()
	for x in range(n):
		for y in range(n):
			if (x + y) % 2 == 0:
				nav(x, y)
				ensure_tree_here()
				while not can_harvest():
					pass
				harvest()


def gather_companion_map():
	n = get_world_size()
	companions = {}
	for x in range(n):
		for y in range(n):
			nav(x, y)
			info = get_companion()
			if info != None:
				companions[(x, y)] = info
	return companions


def neighbors(coord, size):
	x, y = coord
	nbrs = []
	nbrs.append(((x + 1) % size, y))
	nbrs.append(((x - 1 + size) % size, y))
	nbrs.append((x, (y + 1) % size))
	nbrs.append((x, (y - 1 + size) % size))
	return nbrs


def copy_cycle(cycle):
	new_cycle = []
	for coord in cycle:
		new_cycle.append(coord)
	return new_cycle


def cycles_equal(a, b):
	if len(a) != len(b):
		return False
	for i in range(len(a)):
		ax, ay = a[i]
		bx, by = b[i]
		if ax != bx or ay != by:
			return False
	return True


def cycle_less(a, b):
	for i in range(len(a)):
		ax, ay = a[i]
		bx, by = b[i]
		if ax < bx:
			return True
		if ax > bx:
			return False
		if ay < by:
			return True
		if ay > by:
			return False
	return False


def canonical_cycle(path):
	length = len(path)
	best = None
	for orientation in range(2):
		ordered = []
		if orientation == 0:
			for i in range(length):
				ordered.append(path[i])
		else:
			for i in range(length - 1, -1, -1):
				ordered.append(path[i])
		for start in range(length):
			candidate = []
			index = start
			for _ in range(length):
				candidate.append(ordered[index])
				index += 1
				if index == length:
					index = 0
			if best == None or cycle_less(candidate, best):
				best = copy_cycle(candidate)
	return best


def find_cycle(companion_map):
	size = get_world_size()
	found = []
	seen = []
	for x in range(size):
		for y in range(size):
			start = (x, y)
			if start not in companion_map:
				continue
			entity, target = companion_map[start]
			if target == start:
				continue
			path = [start]
			visited = set([start])
			used_targets = set([target])
			def dfs(current_path, visited_cells, target_cells):
				if found:
					return
				if len(current_path) == 8:
					last = current_path[-1]
					start_cell = current_path[0]
					adjacent = neighbors(last, size)
					close_cycle = False
					for nxt in adjacent:
						if nxt == start_cell:
							close_cycle = True
					if not close_cycle:
						return
					canon = canonical_cycle(current_path)
					duplicate = False
					for saved in seen:
						if cycles_equal(canon, saved):
							duplicate = True
					if not duplicate:
						copy_path = copy_cycle(current_path)
						seen.append(copy_cycle(canon))
						found.append(copy_path)
					return
				current = current_path[-1]
				adjacent = neighbors(current, size)
				for nxt in adjacent:
					if found:
						return
					if nxt == current_path[0]:
						continue
					if nxt not in companion_map:
						continue
					if nxt in visited_cells:
						continue
					entity_next, target_next = companion_map[nxt]
					if target_next in visited_cells:
						continue
					if target_next in target_cells:
						continue
					visited_cells.add(nxt)
					target_cells.add(target_next)
					current_path.append(nxt)
					dfs(current_path, visited_cells, target_cells)
					current_path.pop()
					target_cells.remove(target_next)
					visited_cells.remove(nxt)
			dfs(path, visited, used_targets)
			if found:
				return found[0]
	if found:
		return found[0]
	return None


def prepare_companion_tiles(cycle, companion_map):
	prepared = set()
	for coord in cycle:
		entity, target = companion_map[coord]
		tx, ty = target
		if (tx, ty) in prepared:
			continue
		nav(tx, ty)
		attempts = 0
		while get_entity_type() != entity and not can_harvest() and attempts < 6:
			move(North)
			move(South)
			attempts += 1
		if can_harvest():
			harvest()
		ensure_ground(entity)
		if get_entity_type() != entity:
			plant(entity)
		prepared.add((tx, ty))


def run_cycle_harvest(cycle):
	if not cycle:
		return False
	loops_without_gain = 0
	nav(cycle[0][0], cycle[0][1])
	progress_before = num_items(Items.Hay)
	while num_items(Items.Hay) < 100000000:
		progress = False
		for x, y in cycle:
			nav(x, y)
			if get_entity_type() == Entities.Grass and can_harvest():
				harvest()
				progress = True
		move(East)
		move(West)
		if progress:
			loops_without_gain = 0
		else:
			loops_without_gain += 1
		if loops_without_gain >= 10:
			break
	if num_items(Items.Hay) > progress_before:
		return True
	return False


def fallback_harvest():
	n = get_world_size()
	while num_items(Items.Hay) < 100000000:
		for y in range(n):
			nav(0, y)
			if can_harvest():
				harvest()
		for y in range(n - 1, -1, -1):
			nav(0, y)
			if can_harvest():
				harvest()
		move(East)
		move(West)


plant_checkered_trees()
harvest_checkered_trees()
companions = gather_companion_map()
cycle = find_cycle(companions)
if cycle:
	prepare_companion_tiles(cycle, companions)
	success = run_cycle_harvest(cycle)
	if not success:
		fallback_harvest()
else:
	fallback_harvest()
