import Agent
import Player
import Board
import CliHandler


class GameManager:
    def __init__(self):
        player1 = Player.Player(0, 4, 8, "a")
        player2 = Player.Player(8, 4, 0, "a")
        self.players = [player1, player2]
        self.board = Board.Board(9)
        self.turn = 0

    def start_game(self):
        moves_count = 1
        players = self.players
        while not (players[0].won or players[1].won):
            CliHandler.print_state(players[0], players[1], self.board, moves_count, self.turn + 1)
            if players[self.turn].player_type == "u":
                move = CliHandler.get_action(players[self.turn], players[(self.turn + 1) % 2], self.board)
            else:
                move = Agent.get_action(players[self.turn], self.board, players[(self.turn + 1) % 2])
            if len(move) == 3:
                self.board.set_wall(move[0], move[1], move[2])
                players[self.turn].remained_walls = players[self.turn].remained_walls - 1
            else:
                players[self.turn].move(move[0], move[1])
            moves_count += 1
            self.turn = (self.turn + 1) % 2
        CliHandler.print_state(players[0], players[1], self.board, moves_count, self.turn + 1)
        CliHandler.announce_winner((self.turn + 1) % 2 + 1)

