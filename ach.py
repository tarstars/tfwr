def go(direction, steps):
	for _ in range(steps):
		move(direction)

def go_best(l, r, sl, sr):
	if sl < sr:
		go(l, sl)
	else:
		go(r, sr)

def nav(x2, y2):
	n = get_world_size()
	x1, y1 = get_pos_x(), get_pos_y()
	xe, xw = (x2 - x1) % n, (x1 - x2) % n
	yn, ys = (y2 - y1) % n, (y1 - y2) % n
	go_best(East, West, xe, xw)
	go_best(North, South, yn, ys)

def fall(f):
	n = get_world_size()
	for x in range(n):
		for y in range(n):
			nav(x, y)
			f()

def pc():
	plant(Entities.Cactus)

def ss():
	n, x, y = get_world_size(), get_pos_x(), get_pos_y()
	if x:
		if measure() > measure(West):
			swap(West)
	if y:
		if measure() > measure(South):
			swap(South)

def main():
	set_world_size(3)

	fall(till)
	fall(pc)
	
	for _ in range(3):
		fall(ss)

	while True:
		pass

main()
