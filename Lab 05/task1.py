import chess
import random


def evaluate_board(board):
    if board.is_checkmate():
        return -10000 if board.turn else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000,
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

    return score


def generate_random_position(moves=20):
    board = chess.Board()
    for _ in range(moves):
        if board.legal_moves:
            move = random.choice(list(board.legal_moves))
            board.push(move)
    return board


def beam_search(board, beam_width, depth_limit):
    if depth_limit == 0:
        return [], evaluate_board(board)

    candidates = []
    for move in board.legal_moves:
        board_copy = board.copy()
        board_copy.push(move)
        score = evaluate_board(board_copy)
        candidates.append((move, score))

    candidates.sort(key=lambda x: x[1], reverse=not board.turn)
    candidates = candidates[:beam_width]

    best_sequence = []
    best_score = float("-inf") if board.turn else float("inf")

    for move, _ in candidates:
        board_copy = board.copy()
        board_copy.push(move)

        subsequent_sequence, score = beam_search(
            board_copy, beam_width, depth_limit - 1
        )

        if (board.turn and score > best_score) or (
            not board.turn and score < best_score
        ):
            best_score = score
            best_sequence = [move] + subsequent_sequence

    return best_sequence, best_score


def predict_best_move(beam_width, depth_limit):
    board = generate_random_position(20)
    print("Initial Random Board:")
    print(board)

    move_sequence, evaluation = beam_search(board, beam_width, depth_limit)
    move_sequence_str = [move.uci() for move in move_sequence]
    [board.push(move) for move in move_sequence]

    print("\nBoard after Beam Search:")
    print(board)

    return move_sequence_str, evaluation


if __name__ == "__main__":
    beam_width = 5
    depth_limit = 5

    best_sequence, score = predict_best_move(beam_width, depth_limit)
    print(f"\nBest move sequence: {best_sequence}")
    print(f"Evaluation score: {score}")
