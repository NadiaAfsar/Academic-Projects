class Board:
    def __init__(self, n):
        self.n = n
        self.v_walls = []
        self.set_v_walls()
        self.h_walls = []
        self.set_h_walls()

    def set_v_walls(self):
        for i in range(self.n):
            v_list = []
            for j in range(self.n - 1):
                v_list.append(False)
            self.v_walls.append(v_list)

    def set_h_walls(self):
        for i in range(self.n - 1):
            h_list = []
            for j in range(self.n):
                h_list.append(False)
            self.h_walls.append(h_list)

    def set_wall(self, x, y, d):
        match d:
            case "h":
                self.h_walls[x][y] = True
                self.h_walls[x][y + 1] = True
            case "v":
                self.v_walls[x][y] = True
                self.v_walls[x + 1][y] = True


