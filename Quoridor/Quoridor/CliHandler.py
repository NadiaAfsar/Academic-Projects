import Player


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_state(player1, player2, board, moves_count, current_player):
    x1 = player1.x
    y1 = player1.y
    x2 = player2.x
    y2 = player2.y
    v_walls = board.v_walls
    h_walls = board.h_walls
    n = board.n
    print("\n" + "=" * 40)
    print(Colors.BLUE + f"Move {moves_count} | Player {current_player}'s turn" + Colors.RESET)
    print("=" * 40)
    print("    " + " ".join(f"{i:3}" for i in range(n)))
    print("  ┌" + "─" * (n * 3 + 12) + "┐")
    for row in range(n):
        row_str = f"{row:2}│   "
        for col in range(n):
            cell = ". "
            # set players
            if row == x1 and col == y1:
                cell = Colors.GREEN + "P1" + Colors.RESET
            elif row == x2 and col == y2:
                cell = Colors.YELLOW + "P2" + Colors.RESET
            if col < n - 1:
                if v_walls[row][col]:
                    if cell != ".":
                        cell += " "
                    cell += "│"
                else:
                    cell += "  "
            row_str += f"{cell:4}"
        row_str += "│"
        print(row_str)
        row_str = f"  │   "
        for col in range(n):
            cell = ""
            if row < n - 1:
                if h_walls[row][col]:
                    cell += "━━"
            row_str += f"{cell:4}"
        row_str += "│"
        print(row_str)

    print("  └" + "─" * (n * 3 + 12) + "┘")
    print("\n" + "=" * 40)
    print(Colors.BLUE + "Remained Walls:" + Colors.RESET)
    print(Colors.GREEN + f"Player 1: {player1.remained_walls}" + Colors.RESET)
    print(Colors.YELLOW + f"Player 2: {player2.remained_walls}" + Colors.RESET, end="")
    print("\n" + "=" * 40)


def get_action(player1, player2, board):
    n = board.n
    while True:
        action_type = input("choose the type of action (m for move, h for setting horizontal wall, v for setting "
                            "vertical wall): ")
        if not (action_type == "m" or action_type == "h" or action_type == "v"):
            print("Invalid command!")
        elif (action_type == "h" or action_type == "v") and player1.remained_walls == 0:
            print("No walls remained!")

        else:
            i = int(input("i: "))
            j = int(input("j: "))
            if action_type == "m":
                if 0 <= i <= n - 1 and 0 <= j <= n - 1:
                    if Player.valid_move(player1.x, player1.y, i, j, board.v_walls, board.h_walls, player2.x,
                                         player2.y):
                        return (i, j)
                print("Invalid move!")
            elif action_type == "h":
                if 0 <= i <= n - 2 and 0 <= j <= n - 2:
                    if not (board.h_walls[i][j] or board.h_walls[i][j + 1]):
                        board.h_walls[i][j] = True
                        board.h_walls[i][j + 1] = True
                        if Player.is_blocked(player1.x, player1.y, board.h_walls, board.v_walls, board.n,
                                             player1.final_x) or \
                                Player.is_blocked(player2.x, player2.y, board.h_walls, board.v_walls, board.n,
                                                  player2.final_x):
                            board.h_walls[i][j] = False
                            board.h_walls[i][j + 1] = False
                            print("This wall blocks the opponent's way!")
                        else:
                            board.h_walls[i][j] = False
                            board.h_walls[i][j + 1] = False
                            return (i, j, action_type)
                print("Invalid position!")
            elif action_type == "v":
                if 0 <= i <= n - 2 and 0 <= j <= n - 2:
                    if not (board.v_walls[i][j] or board.v_walls[i + 1][j]):
                        board.v_walls[i][j] = True
                        board.v_walls[i + 1][j] = True
                        if Player.is_blocked(player1.x, player1.y, board.h_walls, board.v_walls, board.n,
                                             player1.final_x) or \
                                Player.is_blocked(player2.x, player2.y, board.h_walls, board.v_walls, board.n,
                                                  player2.final_x):
                            board.v_walls[i][j] = False
                            board.v_walls[i + 1][j] = False
                            print("This wall blocks the opponent's way!")
                        else:
                            board.v_walls[i][j] = False
                            board.v_walls[i + 1][j] = False
                            return (i, j, action_type)
                print("Invalid position!")


def announce_winner(winner):
    print(f"Player {winner} won!")
