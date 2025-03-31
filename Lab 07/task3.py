import math


class MiniMax:
    def __init__(self, game):
        self.game = game

    def get_best_move(self, state, turn, depth):
        scored_moves = []
        alpha = -math.inf
        beta = math.inf

        for move in self.game.get_moves(state, "W" if turn == 1 else "B"):
            new_state = self.game.make_move(state, move, "W" if turn == 1 else "B")
            new_value = self.minimax(new_state, turn * -1, depth - 1, alpha, beta)
            scored_moves.append((move, new_value))
            if turn == 1:
                alpha = max(alpha, new_value)
            else:
                beta = min(beta, new_value)

        if not scored_moves:
            return None

        scored_moves.sort(key=lambda x: -x[1] if turn == 1 else x[1])
        return scored_moves[0][0]

    def minimax(self, state, turn, depth, alpha, beta):
        terminated, result = self.game.is_terminal(state)
        if terminated:
            return result
        if depth == 0:
            return self.game.evaluate_board(state)

        if turn == 1:
            value = -math.inf
            for move in self.game.get_moves(state, "W" if turn == 1 else "B"):
                child_state = self.game.make_move(
                    state, move, "W" if turn == 1 else "B"
                )
                value = max(
                    value,
                    self.minimax(
                        child_state,
                        turn * -1,
                        depth - 1,
                        alpha,
                        beta,
                    ),
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        else:
            value = math.inf
            for move in self.game.get_moves(state, "W" if turn == 1 else "B"):
                child_state = self.game.make_move(
                    state, move, "W" if turn == 1 else "B"
                )
                value = min(
                    value,
                    self.minimax(
                        child_state,
                        turn * -1,
                        depth - 1,
                        alpha,
                        beta,
                    ),
                )
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value


class Chess:
    @staticmethod
    def get_initial_state():
        board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P"] * 8,
            [" "] * 8,
            [" "] * 8,
            [" "] * 8,
            [" "] * 8,
            ["p"] * 8,
            ["r", "n", "b", "q", "k", "b", "n", "r"],
        ]
        return board

    @staticmethod
    def print_board(state):
        def color(piece):
            return (
                f"\033[94m{piece}\033[0m"
                if piece.isupper()
                else f"\033[91m{piece}\033[0m" if piece.islower() else " "
            )

        print("   a b c d e f g h")
        print(" +-----------------+")
        for i, row in enumerate(state):
            print(f"{8-i}|", end=" ")
            for cell in row:
                print(color(cell), end=" ")
            print(f"|{8-i}")
        print(" +-----------------+")
        print("   a b c d e f g h")
        print()

    @staticmethod
    def check_winner(state):
        white_king = any("K" in row for row in state)
        black_king = any("k" in row for row in state)
        if not white_king:
            return "B"
        if not black_king:
            return "W"
        return None

    @staticmethod
    def is_terminal(state):
        winner = Chess.check_winner(state)
        if winner:
            return True, (1 if winner == "W" else -1) * 1000
        return False, 0

    @staticmethod
    def is_white_piece(piece):
        return piece.isupper()

    @staticmethod
    def is_opponent_piece(piece, player):
        if player == "W":
            return piece.islower()
        else:
            return piece.isupper() and piece != " "

    @staticmethod
    def get_moves(state, player):
        moves = []
        for i in range(8):
            for j in range(8):
                piece = state[i][j]
                if piece != " ":

                    is_white = Chess.is_white_piece(piece)
                    if (player == "W" and is_white) or (player == "B" and not is_white):
                        moves.extend(Chess.get_piece_moves(state, i, j, piece, player))
        return moves

    @staticmethod
    def get_piece_moves(state, row, col, piece, player):
        moves = []
        piece_type = piece.upper()

        if piece_type == "P":
            direction = -1 if piece.islower() else 1

            new_row = row + direction
            if 0 <= new_row < 8 and state[new_row][col] == " ":
                moves.append(((row, col), (new_row, col)))

                if (row == 1 and piece.isupper()) or (row == 6 and piece.islower()):
                    double_row = row + 2 * direction
                    if 0 <= double_row < 8 and state[double_row][col] == " ":
                        moves.append(((row, col), (double_row, col)))

            for dc in [-1, 1]:
                new_col = col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = state[new_row][new_col]
                    if target != " " and Chess.is_opponent_piece(target, player):
                        moves.append(((row, col), (new_row, new_col)))

        elif piece_type in ["R", "B", "Q"]:
            directions = []
            if piece_type in ["R", "Q"]:
                directions.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])
            if piece_type in ["B", "Q"]:
                directions.extend([(1, 1), (-1, -1), (1, -1), (-1, 1)])

            for dr, dc in directions:
                for dist in range(1, 8):
                    new_row, new_col = row + dr * dist, col + dc * dist
                    if not (0 <= new_row < 8 and 0 <= new_col < 8):
                        break

                    target = state[new_row][new_col]
                    if target == " ":
                        moves.append(((row, col), (new_row, new_col)))
                    elif Chess.is_opponent_piece(target, player):
                        moves.append(((row, col), (new_row, new_col)))
                        break
                    else:
                        break

        elif piece_type == "N":
            knight_moves = [
                (2, 1),
                (2, -1),
                (-2, 1),
                (-2, -1),
                (1, 2),
                (1, -2),
                (-1, 2),
                (-1, -2),
            ]
            for dr, dc in knight_moves:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = state[new_row][new_col]
                    if target == " " or Chess.is_opponent_piece(target, player):
                        moves.append(((row, col), (new_row, new_col)))

        elif piece_type == "K":
            king_moves = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (-1, -1),
                (1, -1),
                (-1, 1),
            ]
            for dr, dc in king_moves:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = state[new_row][new_col]
                    if target == " " or Chess.is_opponent_piece(target, player):
                        moves.append(((row, col), (new_row, new_col)))

        return moves

    @staticmethod
    def make_move(state, move, player):
        (row, col), (new_row, new_col) = move
        new_state = [r[:] for r in state]
        new_state[new_row][new_col] = new_state[row][col]
        new_state[row][col] = " "
        return new_state

    @staticmethod
    def evaluate_board(state):

        piece_values = {
            "P": 1,
            "p": -1,
            "N": 3,
            "n": -3,
            "B": 3,
            "b": -3,
            "R": 5,
            "r": -5,
            "Q": 9,
            "q": -9,
            "K": 100,
            "k": -100,
        }

        value = 0
        for row in state:
            for piece in row:
                if piece in piece_values:
                    value += piece_values[piece]

        return value


def chess_coordinates_to_indices(coord):
    """Convert chess coordinates (e.g., 'e4') to board indices (row, col)"""
    col = ord(coord[0].lower()) - ord("a")
    row = 8 - int(coord[1])
    return row, col


def indices_to_chess_coordinates(row, col):
    """Convert board indices to chess coordinates"""
    return f"{chr(col + ord('a'))}{8 - row}"


def parse_user_move(move_str):
    """Parse a move in algebraic notation, e.g., 'e2e4'"""
    if len(move_str) == 4:
        from_coord = move_str[0:2]
        to_coord = move_str[2:4]
        from_row, from_col = chess_coordinates_to_indices(from_coord)
        to_row, to_col = chess_coordinates_to_indices(to_coord)
        return ((from_row, from_col), (to_row, to_col))
    return None


def main():
    game = Chess()
    agent = MiniMax(game)
    state = game.get_initial_state()
    turn = 1

    game.print_board(state)
    while True:
        terminated, result = game.is_terminal(state)
        if terminated:
            if result:
                print(f"The winner is player {'White' if result == 1 else 'Black'}")
            else:
                print("The game is a draw")
            break

        current_player = "W" if turn == 1 else "B"
        print(f"Current player: {'White' if turn == 1 else 'Black'}")

        if turn == 1:
            print("AI is thinking...")
            move = agent.get_best_move(state, turn, 4)
            if move is None:
                print("AI has no valid moves. Game over.")
                break

            from_coord = indices_to_chess_coordinates(move[0][0], move[0][1])
            to_coord = indices_to_chess_coordinates(move[1][0], move[1][1])
            print(f"AI moves: {from_coord} to {to_coord}")
        else:
            while True:
                try:
                    move_str = input("Enter your move (e.g., e7e5): ")
                    move = parse_user_move(move_str)

                    if move is None:
                        print("Invalid format. Use format 'e7e5'.")
                        continue

                    if move not in game.get_moves(state, current_player):
                        print("Invalid move. Try again.")
                        continue

                    break
                except ValueError:
                    print("Invalid input. Use format 'e7e5'.")
                    continue

        state = game.make_move(state, move, current_player)
        game.print_board(state)
        turn *= -1


if __name__ == "__main__":
    main()
