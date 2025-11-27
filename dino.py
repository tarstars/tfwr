def go(s, d):
	for _ in range(s):
		move(d)

def nav(x, y):
	n = get_world_size()
	a, b = get_pos_x(), get_pos_y()
	e_st = (x - a) % n
	n_st = (y - b) % n
	w_st = n - e_st
	s_st = n - n_st
	if e_st < w_st:
		go(e_st, East)
	else:
		go(w_st, West)
	if n_st < s_st:
		go(n_st, North)
	else:
		go(s_st, South)

def gen_bones():
	nav(0, 0)
	change_hat(Hats.Dinosaur_Hat)

def epoch():
	n = get_world_size()
	if not move(North):
		return False

	hn = n // 2
	for x in range(hn):
		for _ in range(n - 2):
			if not move(North):
				return False
		if not move(East):
			return False
		for _ in range(n - 2):
			if not move(South):
				return False
		if x != hn - 1:
			if not move(East):
				return False
	if not move(South):
		return False
	for _ in range(n-1):
		if not move(West):
			return False
	
	return True

while True:
	gen_bones()
	while epoch():
		pass
	change_hat(Hats.Carrot_Hat)
