import math


class MiniMax:
    def __init__(self, game):
        self.game = game

    def get_best_move(self, state, turn, depth):
        scored_moves = []
        for move in self.game.get_moves(state):
            new_state = self.game.make_move(
                state, move[0], move[1], "X" if turn == 1 else "O"
            )
            new_value = self.minimax(new_state, turn * -1, depth - 1)
            scored_moves.append((move, new_value))

        scored_moves.sort(key=lambda x: -turn * x[1])
        return scored_moves[0][0]

    def minimax(self, state, turn, depth):
        terminated, result = self.game.is_terminal(state)
        if depth == 0 or terminated:
            return result

        func = max if turn == 1 else min
        value = -turn * math.inf

        for move in self.game.get_moves(state):
            child_state = self.game.make_move(
                state, move[0], move[1], "X" if turn == 1 else "O"
            )
            child_value = self.minimax(child_state, turn * -1, depth - 1)
            value = func(value, child_value)

        return value


class TicTacToe:
    @staticmethod
    def get_initial_state():
        return [[" " for _ in range(3)] for _ in range(3)]

    @staticmethod
    def print_board(state):
        for row in state:
            print("|".join(row))
        print()

    @staticmethod
    def check_winner(state):
        for row in state:
            if row[0] == row[1] == row[2] != " ":
                return row[0]

        for col in range(3):
            if state[0][col] == state[1][col] == state[2][col] != " ":
                return state[0][col]

        if state[0][0] == state[1][1] == state[2][2] != " ":
            return state[0][0]

        if state[0][2] == state[1][1] == state[2][0] != " ":
            return state[0][2]

        return None

    @staticmethod
    def is_terminal(state):
        winner = TicTacToe.check_winner(state)
        if winner:
            return True, 1 if winner == "X" else -1
        if all(cell != " " for row in state for cell in row):
            return True, 0
        return False, 0

    @staticmethod
    def get_moves(state):
        return [(i, j) for i in range(3) for j in range(3) if state[i][j] == " "]

    @staticmethod
    def make_move(state, row, col, player):
        if state[row][col] == " ":
            new_state = [r[:] for r in state]
            new_state[row][col] = player
            return new_state
        return None


game = TicTacToe()
agent = MiniMax(game)
state = game.get_initial_state()
turn = -1  # 1 for X, -1 for O

game.print_board(state)
while True:
    terminated, result = game.is_terminal(state)
    if terminated:
        if result:
            print(f"The winner is player {'X' if result == 1 else 'O'}")
        else:
            print("The game is a draw")
        break

    if turn == -1:
        row, col = agent.get_best_move(state, turn, 8)
    else:
        row, col = map(int, input("Enter your move (row col): ").split())
        if state[row][col] != " ":
            print("Invalid move. Try again.")
            continue

    state = game.make_move(state, row, col, "X" if turn == 1 else "O")
    game.print_board(state)
    turn *= -1
