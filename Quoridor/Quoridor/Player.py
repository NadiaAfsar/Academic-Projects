from collections import deque


def valid_move(x1, y1, x2, y2, v_walls, h_walls, opx, opy):
    dx = x1 - x2
    dy = y1 - y2

    # Normal adjacent moves
    if abs(dx) == 1 and dy == 0:  # Vertical move
        wall_x = x2 if dx == 1 else x1
        return not h_walls[wall_x][y1]

    if dx == 0 and abs(dy) == 1:  # Horizontal move
        wall_y = y2 if dy == 1 else y1
        return not v_walls[x1][wall_y]

    # Jump over opponent (2-step moves)
    if abs(dx) == 2 and dy == 0 and abs(x1 - opx) == 1 and y1 == opy and dx * (x1 - opx) > 0:
        # Vertical jump
        wall_x = x2 + 1 if dx == 2 else x1
        return not h_walls[wall_x][y1]

    if dx == 0 and abs(dy) == 2 and x1 == opx and abs(y1 - opy) == 1 and dy * (y1 - opy) > 0:
        # Horizontal jump
        wall_y = y2 + 1 if dy == 2 else y1
        return not v_walls[x1][wall_y]

    # Diagonal jumps (only possible when blocked by walls)
    if abs(dx) == 1 and abs(dy) == 1:
        # Check if opponent is adjacent
        if abs(x1 - opx) == 1 and y1 == opy and dx * (x1 - opx) > 0:  # Opponent horizontally adjacent
            # Check if blocked in forward direction and wall allows diagonal
            return (not h_walls[x2][y2]) and h_walls[x2][y1]

        if x1 == opx and abs(y1 - opy) == 1 and dy * (y1 - opy) > 0:  # Opponent vertically adjacent
            # Check if blocked in forward direction and wall allows diagonal
            return (not v_walls[x2][y2]) and v_walls[x1][y2]

    return False


def is_blocked(x, y, h_walls, v_walls, n, final_x):
    visited = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(False)
        visited.append(row)
    queue = deque()
    queue.append((x, y))
    while len(queue) > 0:
        position = queue.popleft()
        if position[0] == final_x:
            return False
        new_x = position[0] - 1
        new_y = position[1]
        if 0 <= new_x < n:
            if not h_walls[new_x][new_y]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y))
        new_x = position[0] + 1
        new_y = position[1]
        if 0 <= new_x < n:
            if not h_walls[position[0]][new_y]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y))
        new_x = position[0]
        new_y = position[1] - 1
        if 0 <= new_y < n:
            if not v_walls[new_x][new_y]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y))
        new_x = position[0]
        new_y = position[1] + 1
        if 0 <= new_y < n:
            if not v_walls[new_x][position[1]]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y))
    return True


class Player:
    def __init__(self, x, y, final_x, player_type):
        self.x = x
        self.y = y
        self.final_x = final_x
        self.remained_walls = 10
        self.won = False
        self.player_type = player_type

    def is_winner(self):
        return self.x == self.final_x

    def move(self, x, y):
        self.x = x
        self.y = y
        self.won = self.is_winner()







