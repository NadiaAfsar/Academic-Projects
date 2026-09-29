import Player
from collections import deque


visited = 0
pruned = 0


def get_actions(x, y, opx, opy, v_walls, h_walls, n, remained_walls, final_x, op_final):
    actions = []
    moves = possible_moves(x, y, opx, opy, v_walls, h_walls)
    actions.extend(moves)
    if remained_walls > 0:
        walls = possible_walls(x, y, opx, opy, v_walls, h_walls, n, final_x, op_final)
        actions.extend(walls)
    return actions


def possible_moves(x, y, opx, opy, v_walls, h_walls):
    moves = []
    xs = [1, -1, 0, 0, 2, -2, 0, 0, 1, 1, -1, -1]
    ys = [0, 0, 1, -1, 0, 0, 2, -2, 1, -1, 1, -1]
    for i in range(len(xs)):
        x2 = x + xs[i]
        y2 = y + ys[i]
        if 0 <= x2 <= 8 and 0 <= y2 <= 8:
            if Player.valid_move(x, y, x2, y2, v_walls, h_walls, opx, opy):
                if x2 != opx or y2 != opy:
                    moves.append((x2, y2))
    return moves


def possible_walls(x, y, opx, opy, v_walls, h_walls, n, final_x, op_final):
    walls = []
    for i in range(n - 1):
        for j in range(n - 1):
            if not (h_walls[i][j] or h_walls[i][j + 1]):
                h_walls[i][j] = True
                h_walls[i][j + 1] = True
                if not (Player.is_blocked(x, y, h_walls, v_walls, n, final_x) or
                        Player.is_blocked(opx, opy, h_walls, v_walls, n, op_final)):
                    walls.append((i, j, "h"))
                h_walls[i][j] = False
                h_walls[i][j + 1] = False
    for i in range(n - 1):
        for j in range(n - 1):
            if not (v_walls[i][j] or v_walls[i + 1][j]):
                v_walls[i][j] = True
                v_walls[i + 1][j] = True
                if not (Player.is_blocked(x, y, h_walls, v_walls, n, final_x) or
                        Player.is_blocked(opx, opy, h_walls, v_walls, n, op_final)):
                    walls.append((i, j, "v"))
                v_walls[i][j] = False
                v_walls[i + 1][j] = False
    walls = sorted(walls, key=lambda wall: (abs(wall[0] - opx) + abs(wall[1] - opy), wall[1]))
    return walls


def distance(x, y, h_walls, v_walls, n, final_x):
    visited = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(False)
        visited.append(row)
    queue = deque()
    queue.append((x, y, 0))
    while len(queue) > 0:
        position = queue.popleft()
        if position[0] == final_x:
            return position[2]
        new_x = position[0] - 1
        new_y = position[1]
        if 0 <= new_x < n:
            if not h_walls[new_x][new_y]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, position[2] + 1))
        new_x = position[0] + 1
        new_y = position[1]
        if 0 <= new_x < n:
            if not h_walls[position[0]][new_y]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, position[2] + 1))
        new_x = position[0]
        new_y = position[1] - 1
        if 0 <= new_y < n:
            if not v_walls[new_x][new_y]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, position[2] + 1))
        new_x = position[0]
        new_y = position[1] + 1
        if 0 <= new_y < n:
            if not v_walls[new_x][position[1]]:
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, position[2] + 1))
    return float('inf')


def center_bonus(x1, y1, x2, y2, n):
    center_row, center_col = int(n / 2), int(n / 2)
    my_center_dist = abs(x1 - center_row) + abs(y1 - center_col)
    opp_center_dist = abs(x2 - center_row) + abs(y2 - center_col)
    bonus = (opp_center_dist - my_center_dist)
    return bonus


def heuristic(x, y, opx, opy, remained_walls, op_remained_walls, h_walls, v_walls, n, goal, op_goal):
    dist_me = distance(x, y, h_walls, v_walls, n, goal)
    if remained_walls == 0:
        return 9 - dist_me
    dist_opp = distance(opx, opy, h_walls, v_walls, n, op_goal)
    center_score = center_bonus(x, y, opx, opy, n)
    walls_score = remained_walls
    score = -12 * dist_me + 10 * dist_opp + 0.5 * center_score + walls_score * 0.3
    return score


def Minimax(player, board, opponent):
    v, move = max_value(player.x, player.y, opponent.x, opponent.y, player.remained_walls, opponent.remained_walls,
                        board.v_walls, board.h_walls, board.n, 3, player.final_x, opponent.final_x)
    return move


def max_value(x, y, opx, opy, remained_walls, op_remained_walls, v_walls, h_walls, n, depth, goal, op_goal):
    if depth == 0:
        return heuristic(x, y, opx, opy, remained_walls, op_remained_walls, h_walls, v_walls, n, goal, op_goal), None
    actions = get_actions(x, y, opx, opy, v_walls, h_walls, n, remained_walls, goal, op_goal)
    move = None
    v = float('-inf')
    for a in actions:
        v2 = float('inf')
        # if action is move
        if len(a) == 2:
            new_x = a[0]
            new_y = a[1]
            v2, a2 = min_value(opx, opy, new_x, new_y, op_remained_walls, remained_walls, v_walls, h_walls, n,
                               depth - 1,
                               op_goal, goal)
        # if action is to set walls
        elif len(a) == 3:
            match a[2]:
                case "h":
                    h_walls[a[0]][a[1]] = True
                    h_walls[a[0]][a[1] + 1] = True
                    v2, a2 = min_value(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                       depth - 1, op_goal, goal)
                    h_walls[a[0]][a[1]] = False
                    h_walls[a[0]][a[1] + 1] = False
                case "v":
                    v_walls[a[0]][a[1]] = True
                    v_walls[a[0] + 1][a[1]] = True
                    v2, a2 = min_value(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                       depth - 1, op_goal, goal)
                    v_walls[a[0]][a[1]] = False
                    v_walls[a[0] + 1][a[1]] = False
        if v2 > v:
            v, move = v2, a
    return v, move


def min_value(x, y, opx, opy, remained_walls, op_remained_walls, v_walls, h_walls, n, depth, goal, op_goal):
    if depth == 0:
        return heuristic(x, y, opx, opy, remained_walls, op_remained_walls, h_walls, v_walls, n, goal, op_goal), None
    actions = get_actions(x, y, opx, opy, v_walls, h_walls, n, remained_walls, goal, op_goal)
    move = None
    v = float('inf')
    for a in actions:
        v2 = float('inf')
        # if action is move
        if len(a) == 2:
            new_x = a[0]
            new_y = a[1]
            v2, a2 = max_value(opx, opy, new_x, new_y, op_remained_walls, remained_walls, v_walls, h_walls, n,
                               depth - 1,
                               op_goal, goal)
        # if action is to set walls
        elif len(a) == 3:
            match a[2]:
                case "h":
                    h_walls[a[0]][a[1]] = True
                    h_walls[a[0]][a[1] + 1] = True
                    v2, a2 = max_value(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                       depth - 1, op_goal, goal)
                    h_walls[a[0]][a[1]] = False
                    h_walls[a[0]][a[1] + 1] = False
                case "v":
                    v_walls[a[0]][a[1]] = True
                    v_walls[a[0] + 1][a[1]] = True
                    v2, a2 = max_value(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                       depth - 1, op_goal, goal)
                    v_walls[a[0]][a[1]] = False
                    v_walls[a[0] + 1][a[1]] = False
        if v2 < v:
            v, move = v2, a
    return v, move


def get_action(player, board, opponent):
    return Alpha_Beta(player, board, opponent)


def Alpha_Beta(player, board, opponent):
    global visited
    visited = 0
    global pruned
    pruned = 0
    v, move = alpha_beta_max(player.x, player.y, opponent.x, opponent.y, player.remained_walls, opponent.remained_walls,
                             board.v_walls, board.h_walls, board.n, 2, player.final_x, opponent.final_x, float('-inf'),
                             float('inf'))
    print(f"{visited} nodes visited and {pruned} nodes pruned.")
    return move


def alpha_beta_max(x, y, opx, opy, remained_walls, op_remained_walls, v_walls, h_walls, n, depth, goal, op_goal, alpha,
                   beta):
    global visited
    visited += 1
    if depth == 0:
        return heuristic(x, y, opx, opy, remained_walls, op_remained_walls, h_walls, v_walls, n, goal, op_goal), None
    actions = get_actions(x, y, opx, opy, v_walls, h_walls, n, remained_walls, goal, op_goal)
    move = None
    v = float('-inf')
    for a in actions:
        v2 = float('inf')
        # if action is move
        if len(a) == 2:
            new_x = a[0]
            new_y = a[1]
            v2, a2 = alpha_beta_min(opx, opy, new_x, new_y, op_remained_walls, remained_walls, v_walls, h_walls, n,
                                    depth - 1,
                                    op_goal, goal, alpha, beta)
        # if action is to set walls
        elif len(a) == 3:
            match a[2]:
                case "h":
                    h_walls[a[0]][a[1]] = True
                    h_walls[a[0]][a[1] + 1] = True
                    v2, a2 = alpha_beta_min(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                            depth - 1, op_goal, goal, alpha, beta)
                    h_walls[a[0]][a[1]] = False
                    h_walls[a[0]][a[1] + 1] = False
                case "v":
                    v_walls[a[0]][a[1]] = True
                    v_walls[a[0] + 1][a[1]] = True
                    v2, a2 = alpha_beta_min(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                            depth - 1, op_goal, goal, alpha, beta)
                    v_walls[a[0]][a[1]] = False
                    v_walls[a[0] + 1][a[1]] = False
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            global pruned
            pruned += 1
            return v, move
    return v, move


def alpha_beta_min(x, y, opx, opy, remained_walls, op_remained_walls, v_walls, h_walls, n, depth, goal, op_goal, alpha,
                   beta):
    if depth == 0:
        return heuristic(x, y, opx, opy, remained_walls, op_remained_walls, h_walls, v_walls, n, goal, op_goal), None
    actions = get_actions(x, y, opx, opy, v_walls, h_walls, n, remained_walls, goal, op_goal)
    move = None
    v = float('inf')
    for a in actions:
        v2 = float('inf')
        # if action is move
        if len(a) == 2:
            new_x = a[0]
            new_y = a[1]
            v2, a2 = alpha_beta_max(opx, opy, new_x, new_y, op_remained_walls, remained_walls, v_walls, h_walls, n,
                                    depth - 1,
                                    op_goal, goal, alpha, beta)
        # if action is to set walls
        elif len(a) == 3:
            match a[2]:
                case "h":
                    h_walls[a[0]][a[1]] = True
                    h_walls[a[0]][a[1] + 1] = True
                    v2, a2 = alpha_beta_max(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                            depth - 1, op_goal, goal, alpha, beta)
                    h_walls[a[0]][a[1]] = False
                    h_walls[a[0]][a[1] + 1] = False
                case "v":
                    v_walls[a[0]][a[1]] = True
                    v_walls[a[0] + 1][a[1]] = True
                    v2, a2 = alpha_beta_max(opx, opy, x, y, op_remained_walls, remained_walls - 1, v_walls, h_walls, n,
                                            depth - 1, op_goal, goal, alpha, beta)
                    v_walls[a[0]][a[1]] = False
                    v_walls[a[0] + 1][a[1]] = False
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            global pruned
            pruned += 1
            return v, move
    return v, move
