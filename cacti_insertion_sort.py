def best_move(n1, d1, n2, d2):
    n, d = [(n1, d1), (n2, d2)][n2 < n1]
    for _ in range(n):
        move(d)

def nav(x2, y2):
    n = get_world_size()
    x1, y1 = get_pos_x(), get_pos_y()
    best_move((x2 - x1)%n, East, (x1 - x2)%n, West)
    best_move((y2 - y1)%n, North, (y1 - y2)%n, South)

def insert_iteration(xc, yc, n):
    nav(xc, yc)
    while True:
        cell, val = 'current', measure()
        if yc + 1 < n and measure(North) < val:
            cell, val = North, measure(North)
        if xc + 1 < n and measure(East) < val:
            cell, val = East, measure(East)
        
        if cell == 'current':
            break

        swap(cell)
        move(cell)
        xc, yc = get_pos_x(), get_pos_y()

n = get_world_size()

for y in range(n):
    for x in range(n):
        nav(x, y)
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Cactus)

for y in range(n - 1, -1, -1):
    for x in range(n - 1, -1, -1):
        insert_iteration(x, y, n)
