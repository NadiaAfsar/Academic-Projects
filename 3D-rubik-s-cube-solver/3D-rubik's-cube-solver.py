import random
from collections import deque
from queue import PriorityQueue
import math
import datetime

class Cuby:
    def __init__(self, x, y, z, xp, yp, zp, cube):
        self.x = x
        self.y = y
        self.z = z
        self.cube = cube
        self.colors_and_faces = {}
        self.set_color(xp, yp, zp)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}, {self.colors_and_faces}"

    def set_color(self, xp, yp, zp):
        if self.x == 0:
            self.colors_and_faces['x'] = ["g", 5]
            self.cube.state[self.cube.sides[5] + self.z * yp + self.y] = "g"
        if self.x == xp - 1:
            self.colors_and_faces['x'] = ["r", 6]
            self.cube.state[self.cube.sides[6] + self.z * yp + self.y] = "r"
        if self.y == 0:
            self.colors_and_faces['y'] = ["w", 3]
            self.cube.state[self.cube.sides[3] + self.z * xp + self.x] = "w"
        if self.y == yp - 1:
            self.colors_and_faces['y'] = ["b", 1]
            self.cube.state[self.cube.sides[1] + self.z * xp + self.x] = "b"
        if self.z == 0:
            self.colors_and_faces['z'] = ["y", 2]
            self.cube.state[self.cube.sides[2] + self.y * xp + self.x] = "y"
        if self.z == zp - 1:
            self.colors_and_faces['z'] = ["o", 4]
            self.cube.state[self.cube.sides[4] + self.y * xp + self.x] = "o"


def move(movable, state, x, y, z, cubies, sides):
    length = len(movable)
    new_state = state.copy()
    for i in range(int(length / 2)):
        movable1 = cubies[movable[i][0]][movable[i][1]][movable[i][2]]
        movable2 = cubies[movable[length - 1 - i][0]][movable[length - 1 - i][1]][movable[length - 1 - i][2]]
        for direct in movable1.colors_and_faces:
            colors1 = movable1.colors_and_faces
            colors2 = movable2.colors_and_faces
            match direct:
                case "x":
                    index1 = sides[colors1["x"][1]] + movable1.z * y + movable1.y
                    index2 = sides[colors2["x"][1]] + movable2.z * y + movable2.y
                    new_state[index1] = state[index2]
                    new_state[index2] = state[index1]
                case "y":
                    index1 = sides[colors1["y"][1]] + movable1.z * x + movable1.x
                    index2 = sides[colors2["y"][1]] + movable2.z * x + movable2.x
                    new_state[index1] = state[index2]
                    new_state[index2] = state[index1]
                case "z":
                    index1 = sides[colors1["z"][1]] + movable1.y * x + movable1.x
                    index2 = sides[colors2["z"][1]] + movable2.y * x + movable2.x
                    new_state[index1] = state[index2]
                    new_state[index2] = state[index1]
    return new_state


def heuristic_move(movable, state, x, y, z, cubies, h, sides):
    length = len(movable)
    new_state = state.copy()
    new_h = h
    for i in range(int(length / 2)):
        movable1 = cubies[movable[i][0]][movable[i][1]][movable[i][2]]
        movable2 = cubies[movable[length - 1 - i][0]][movable[length - 1 - i][1]][movable[length - 1 - i][2]]
        for direct in movable1.colors_and_faces:
            colors1 = movable1.colors_and_faces
            colors2 = movable2.colors_and_faces
            match direct:
                case "x":
                    index1 = sides[colors1["x"][1]] + movable1.z * y + movable1.y
                    index2 = sides[colors2["x"][1]] + movable2.z * y + movable2.y
                    new_state[index1] = state[index2]
                    new_state[index2] = state[index1]
                case "y":
                    index1 = sides[colors1["y"][1]] + movable1.z * x + movable1.x
                    index2 = sides[colors2["y"][1]] + movable2.z * x + movable2.x
                    new_state[index1] = state[index2]
                    new_state[index2] = state[index1]
                case "z":
                    index1 = sides[colors1["z"][1]] + movable1.y * x + movable1.x
                    index2 = sides[colors2["z"][1]] + movable2.y * x + movable2.x
                    new_state[index1] = state[index2]
                    new_state[index2] = state[index1]
            before = 0
            after = 0
            match colors1[direct][0]:
                case "b":
                    before = 0 if colors2[direct][1] == 1 else 1
                    after = 0 if colors1[direct][1] == 1 else 1
                case "y":
                    before = 0 if colors2[direct][1] == 2 else 1
                    after = 0 if colors1[direct][1] == 2 else 1
                case "w":
                    before = 0 if colors2[direct][1] == 3 else 1
                    after = 0 if colors1[direct][1] == 3 else 1
                case "o":
                    before = 0 if colors2[direct][1] == 4 else 1
                    after = 0 if colors1[direct][1] == 4 else 1
                case "g":
                    before = 0 if colors2[direct][1] == 5 else 1
                    after = 0 if colors1[direct][1] == 5 else 1
                case "r":
                    before = 0 if colors2[direct][1] == 6 else 1
                    after = 0 if colors1[direct][1] == 6 else 1
            if after - before > 0:
                new_h += 1
    return [new_state, new_h]


def generate_random(cube, seed):
    random.seed(seed)
    for _ in range(100):
        rand = random.randrange(len(cube.movables))
        movable = cube.movables[rand]
        new_state = move(movable, cube.state, cube.x, cube.y, cube.z, cube.cubies, cube.sides)
        cube.state = new_state


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cubies = None
        self.movables = []
        self.state = []
        self.expected = ""
        self.sides = {}

    def initialize(self):
        self.set_sides()
        self.state = ["0"] * (2 * self.x * self.y + 2 * self.x * self.z + 2 * self.y * self.z)
        self.set_cubies(self.x, self.y, self.z)
        self.set_expected()
        self.get_movables()

    def set_expected(self):
        self.expected = "".join(self.state)

    def set_cubies(self, x, y, z):
        self.cubies = []
        for i in range(x):
            x_list = []
            for j in range(y):
                y_list = []
                for k in range(z):
                    new_cuby = Cuby(i, j, k, x, y, z, self)
                    y_list.append(new_cuby)
                x_list.append(y_list)
            self.cubies.append(x_list)

    def get_movables(self):
        movables = self.movables
        x = self.x
        y = self.y
        z = self.z
        for i in range(x):
            for j in range(y):
                movable1 = []
                for k in range(z):
                    if i == 0 or i == x - 1 or j == 0 or j == y - 1 or k == 0 or k == z - 1:
                        movable1.append((i, j, k))
                movables.append(movable1)
        for i in range(x):
            for j in range(z):
                movable1 = []
                for k in range(y):
                    if i == 0 or i == x - 1 or j == 0 or j == z - 1 or k == 0 or k == y - 1:
                        movable1.append((i, k, j))
                movables.append(movable1)
        for i in range(y):
            for j in range(z):
                movable1 = []
                for k in range(x):
                    if i == 0 or i == y - 1 or j == 0 or j == z - 1 or k == 0 or k == x - 1:
                        movable1.append((k, i, j))
                movables.append(movable1)

    def is_expected(self):
        current = "".join(self.state)
        return current == self.expected

    def set_sides(self):
        x = self.x
        y = self.y
        z = self.z
        self.sides = {
            1: 0,
            2: x * z,
            3: x * z + x * y,
            4: x * (2 * z + y),
            5: x * 2 * (z + y),
            6: x * 2 * (z + y) + y * z
        }


def print_state(state, x, y, z):
    print("up:")
    for i in range(x):
        for j in range(z):
            print(state[j * x + i], end="")
        print()
    print("front:")
    for i in range(x):
        for j in range(y):
            print(state[x * z + j * x + i], end="")
        print()
    print("down:")
    for i in range(x):
        for j in range(z):
            print(state[x * (y + z) + j * x + i], end="")
        print()
    print("back:")
    for i in range(x):
        for j in range(y):
            print(state[x * (2 * z + y) + j * x + i], end="")
        print()
    print("left:")
    for i in range(y):
        for j in range(z):
            print(state[2 * x * (y + z) + j * y + i], end="")
        print()
    print("right:")
    for i in range(y):
        for j in range(z):
            print(state[2 * x * (y + z) + y * z + j * y + i], end="")
        print()


def print_moves(states, x, y, z):
    counts = len(states) / (2 * x * y + 2 * x * z + 2 * y * z)
    for i in range(int(counts)):
        print(f"-----state {i + 1}-----")
        print_state(states[i * (2 * x * y + 2 * x * z + 2 * y * z): (i + 1) * (2 * x * y + 2 * x * z + 2 * y * z)], x, y, z)


class State:
    def __init__(self, seen, state):
        self.seen = seen
        self.state = state

    def __lt__(self, other):
        return len(self.seen) > len(other.seen)


class StateWithDepth:
    def __init__(self, seen, state, depth):
        self.seen = seen
        self.state = state
        self.depth = depth


class HeuristicState:
    def __init__(self, seen, state, h):
        self.seen = seen
        self.state = state
        self.h = h

    def __lt__(self, other):
        return len(self.seen) > len(other.seen)


class AStarState:
    def __init__(self, seen, state, h, cost):
        self.seen = seen
        self.state = state
        self.h = h
        self.cost = cost

    def __lt__(self, other):
        return len(self.seen) > len(other.seen)


class RBFSState:
    def __init__(self, seen, state, h, cost, best_f):
        self.seen = seen
        self.state = state
        self.h = h
        self.cost = cost
        self.best_f = best_f


def get_position(i, x, y, z):
    i += 1
    xp = 0
    yp = 0
    zp = 0
    if i <= (x * z):
        yp = y
        zp = int(i / z) + 1
        xp = i % z
        if xp == 0:
            xp = x
            zp -= 1
    elif i <= (x * (z + y)):
        i -= x * z
        zp = 1
        yp = int(i / y) + 1
        xp = i % y
        if xp == 0:
            xp = x
            yp -= 1
    elif i <= x * (2 * z + y):
        i -= x * (z + y)
        yp = 1
        zp = int(i / z) + 1
        xp = i % z
        if xp == 0:
            xp = x
            zp -= 1
    elif i <= x * 2 * (z + y):
        i -= x * (2 * z + y)
        zp = z
        yp = int(i / y) + 1
        xp = i % y
        if xp == 0:
            xp = x
            yp -= 1
    elif i <= x * 2 * (z + y) + z * y:
        i -= x * 2 * (z + y)
        xp = 1
        zp = int(i / z) + 1
        yp = i % z
        if yp == 0:
            yp = y
            zp -= 1
    elif i <= x * 2 * (z + y) + z * y * 2:
        i -= x * 2 * (z + y) + z * y
        xp = x
        zp = int(i / z) + 1
        yp = i % z
        if yp == 0:
            yp = y
            zp -= 1
    return xp, yp, zp


def get_heuristic(state, x, y, z):
    h = 0
    is_seen = {}
    for i in range(len(state)):
        xp, yp, zp = get_position(i, x, y, z)
        try:
            a = is_seen[(xp, yp)]
            b = is_seen[(xp, zp)]
            c = is_seen[(yp, zp)]
        except KeyError:
            match state[i]:
                case "b":
                    if not (0 <= i < x * z):
                        h += 1
                case "y":
                    if not (x * z <= i < x * z + x * y):
                        h += 1
                case "w":
                    if not (x * z + x * y <= i < x * (2 * z + y)):
                        h += 1
                case "o":
                    if not (x * (2 * z + y) <= i < x * 2 * (z + y)):
                        h += 1
                case "g":
                    if not (x * 2 * (z + y) <= i < x * 2 * (z + y) + y * z):
                        h += 1
                case "r":
                    if not (x * 2 * (z + y) + y * z <= i < x * 2 * (z + y) + y * z * 2):
                        h += 1
            is_seen[(xp, yp)] = True
            is_seen[(xp, zp)] = True
            is_seen[(yp, zp)] = True
    return h


def BFS(cube):
    counter = 0
    seen = {"".join(cube.state): True}
    queue = deque()
    initial_state = State("".join(cube.state), cube.state)
    queue.append(initial_state)
    while len(queue) != 0:
        state = queue.popleft()
        for movable in cube.movables:
            new_state = move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return state.seen + state_str, counter
            try:
                is_seen = seen[state_str]
            except KeyError:
                seen[state_str] = True
                new_new_state = State(state.seen + state_str, new_state)
                queue.append(new_new_state)


def DFS(cube):
    counter = 0
    seen = {"".join(cube.state): True}
    queue = deque()
    initial_state = State("".join(cube.state), cube.state)
    queue.append(initial_state)
    while len(queue) != 0:
        state = queue.pop()
        for movable in cube.movables:
            new_state = move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return state.seen + state_str, counter
            try:
                is_seen = seen[state_str]
            except KeyError:
                seen[state_str] = True
                new_new_state = State(state.seen + state_str, new_state)
                queue.append(new_new_state)


def UCS(cube):
    counter = 0
    seen = {"".join(cube.state): 0}
    priority_queue = PriorityQueue()
    initial_state = State("".join(cube.state), cube.state)
    priority_queue.put((0, initial_state))
    while priority_queue.qsize() != 0:
        key, state = priority_queue.get()
        for movable in cube.movables:
            new_state = move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return state.seen + state_str, counter
            try:
                is_seen = seen[state_str]
                if is_seen > key + 1:
                    new_new_state = State(state.seen + state_str, new_state)
                    priority_queue.put((key + 1, new_new_state))
            except KeyError:
                seen[state_str] = True
                new_new_state = State(state.seen + state_str, new_state)
                priority_queue.put((key + 1, new_new_state))


def DLS(cube, depth):
    counter = 0
    seen = {"".join(cube.state): True}
    queue = deque()
    initial_state = StateWithDepth("".join(cube.state), cube.state, 0)
    queue.append(initial_state)
    while len(queue) != 0:
        state = queue.pop()
        for movable in cube.movables:
            new_state = move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return state.seen + state_str, counter
            try:
                is_seen = seen[state_str]
            except KeyError:
                if state.depth + 1 < depth:
                    seen[state_str] = True
                    new_new_state = StateWithDepth(state.seen + state_str, new_state, state.depth + 1)
                    queue.append(new_new_state)
    return False, counter


def IDS(cube):
    counter = 0
    depth = 0
    seen = {"".join(cube.state): True}
    queue = deque()
    initial_state = StateWithDepth("".join(cube.state), cube.state, 0)
    queue.append(initial_state)
    while True:
        has_result, result, counter = IDSLoop(queue, cube, seen, depth + 10, counter)
        if has_result:
            return result, counter
        for _ in range(len(result)):
            state = result.pop()
            queue.append(state)


def GBFS(cube):
    counter = 0
    seen = {"".join(cube.state): True}
    h = get_heuristic("".join(cube.state), cube.x, cube.y, cube.z)
    priority_queue = PriorityQueue()
    initial_state = HeuristicState("".join(cube.state), cube.state, h)
    priority_queue.put((h, initial_state))
    while priority_queue.qsize() != 0:
        state = priority_queue.get()[1]
        for movable in cube.movables:
            new_state, h = heuristic_move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, state.h, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return state.seen + state_str, counter
            try:
                is_seen = seen[state_str]
            except KeyError:
                seen[state_str] = True
                new_new_state = HeuristicState(state.seen + state_str, new_state, h)
                priority_queue.put((h, new_new_state))


def WAStar(cube, weight):
    counter = 0
    seen = {"".join(cube.state): True}
    h = get_heuristic("".join(cube.state), cube.x, cube.y, cube.z)
    priority_queue = PriorityQueue()
    initial_state = AStarState("".join(cube.state), cube.state, h, 0)
    priority_queue.put((h * weight, initial_state))
    while priority_queue.qsize() != 0:
        state = priority_queue.get()[1]
        for movable in cube.movables:
            new_state, h = heuristic_move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, state.h, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return state.seen + state_str, counter
            try:
                is_seen = seen[state_str]
            except KeyError:
                seen[state_str] = True
                new_new_state = AStarState(state.seen + state_str, new_state, h, state.cost + 1)
                priority_queue.put((weight * h + new_new_state.cost, new_new_state))


def AStar(cube):
    return WAStar(cube, 1)


def IDAStar(cube):
    counter = 0
    depth = 0
    seen = {"".join(cube.state): True}
    h = get_heuristic("".join(cube.state), cube.x, cube.y, cube.z)
    queue = deque()
    initial_state = AStarState("".join(cube.state), cube.state, h, 0)
    queue.append(initial_state)
    while True:
        has_result, result, counter = IDALoop(queue, cube, seen, depth + 10, h, counter)
        if has_result:
            return result, counter
        for _ in range(len(result)):
            state = result.pop()
            queue.append(state)


def RBFS(cube):
    counter = 0
    current = "".join(cube.state)
    seen = {current: True}
    h = get_heuristic(current, cube.x, cube.y, cube.z)
    initial_state = AStarState(current, cube.state, h, 0)
    state, f, result, counter = recursive(cube, initial_state, math.inf, seen, h, counter)
    return state, counter


def recursive(cube, state, f_limit, seen, h, counter):
    state_str = "".join(state.state)
    if state_str == cube.expected:
        return state.seen, f_limit, True, counter
    successors = PriorityQueue()
    for movable in cube.movables:
        new_state, new_h = heuristic_move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, h, cube.sides)
        counter += 1
        new_state_str = "".join(new_state)
        if new_state_str == cube.expected:
            return state.seen + new_state_str, f_limit, True, counter
        try:
            is_seen = seen[new_state_str]
        except KeyError:
            seen[new_state_str] = True
            new_new_state = AStarState(state.seen + new_state_str, new_state, new_h, state.cost + 1)
            successors.put((new_h + new_new_state.cost, new_new_state))
    while successors.qsize() != 0:
        f, new_state = successors.get()
        if f > f_limit:
            return state, f, False, counter
        alternative = math.inf
        if successors.qsize() > 0:
            alternative, temp = successors.get()
            successors.put((alternative, temp))
        state, f, result, counter = recursive(cube, new_state, min(f_limit, alternative), seen, new_state.h, counter)
        if result:
            return state, f, True, counter
        else:
            successors.put((f, state))
    return state, f_limit, False, counter


def IDALoop(queue, cube, seen, depth, h, counter):
    frontiers_queue = deque()
    while len(queue) != 0:
        state = queue.pop()
        for movable in cube.movables:
            new_state, h = heuristic_move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, h, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return [True, state.seen + state_str, counter]
            try:
                is_seen = seen[state_str]
            except KeyError:
                seen[state_str] = True
                new_new_state = AStarState(state.seen + state_str, new_state, h, state.cost + 1)
                if state.cost + 1 <= depth:
                    queue.append(new_new_state)
                else:
                    frontiers_queue.append(new_new_state)
    return [False, frontiers_queue, counter]


def IDSLoop(queue, cube, seen, depth, counter):
    frontiers_queue = deque()
    while len(queue) != 0:
        state = queue.pop()
        for movable in cube.movables:
            new_state = move(movable, state.state, cube.x, cube.y, cube.z, cube.cubies, cube.sides)
            counter += 1
            state_str = "".join(new_state)
            if state_str == cube.expected:
                return [True, state.seen + state_str, counter]
            try:
                is_seen = seen[state_str]
            except KeyError:
                seen[state_str] = True
                new_new_state = StateWithDepth(state.seen + state_str, new_state, state.depth + 1)
                if state.depth + 1 <= depth:
                    queue.append(new_new_state)
                else:
                    frontiers_queue.append(new_new_state)
    return [False, frontiers_queue, counter]


def main():
    cube = Cube(2, 2, 3)
    cube.initialize()
    generate_random(cube, 1021)

    start = datetime.datetime.now()
    result, counter = BFS(cube)
    print("-----BFS-----")
    print(f"{counter} nodes expanded")
    print_moves(result, cube.x, cube.y, cube.z)
    print("------------------")
    end = datetime.datetime.now()
    print(f"elapsed time: {end - start}")

    # start = datetime.datetime.now()
    # result, counter = DFS(cube)
    # print("-----DFS-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # result, counter = UCS(cube)
    # print("-----UCS-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # depth = 10
    # result, counter = DLS(cube, depth)
    # print(f"-----DLS(depth = {depth})-----")
    # print(f"{counter} nodes expanded")
    # if result:
    #     print_moves(result, cube.x, cube.y, cube.z)
    # else:
    #     print("no result found")
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # result, counter = IDS(cube)
    # print("-----IDS-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # result, counter = GBFS(cube)
    # print("-----GBFS-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")

    # start = datetime.datetime.now()
    # result, counter = AStar(cube)
    # print("-----A*-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # weight = 3
    # result, counter = WAStar(cube, weight)
    # print(f"-----Weighted A*(weight = {weight})-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # result, counter = IDAStar(cube)
    # print("-----IDA*-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")
    #
    # start = datetime.datetime.now()
    # result, counter = RBFS(cube)
    # print("-----RBFS-----")
    # print(f"{counter} nodes expanded")
    # print_moves(result, cube.x, cube.y, cube.z)
    # print("------------------")
    # end = datetime.datetime.now()
    # print(f"elapsed time: {end - start}")


main()
