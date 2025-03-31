import math
import random


class CoinGame:
    def __init__(self, coins):
        self.initial_coins = coins.copy()

    def get_initial_state(self):
        return {"coins": self.initial_coins.copy(), "max_score": 0, "min_score": 0}

    def print_state(self, state):
        print(f"Max's score: {state['max_score']}")
        print(f"Min's score: {state['min_score']}")
        print(f"Remaining coins: {state['coins']}")
        print()

    def is_terminal(self, state):
        return len(state["coins"]) == 0

    def get_moves(self, state):
        if len(state["coins"]) == 0:
            return []
        return ["left", "right"]

    def make_move(self, state, move, player):
        new_state = {
            "coins": state["coins"].copy(),
            "max_score": state["max_score"],
            "min_score": state["min_score"],
        }

        if move == "left":
            coin_value = new_state["coins"].pop(0)
        else:
            coin_value = new_state["coins"].pop(-1)

        if player == "Max":
            new_state["max_score"] += coin_value
        else:
            new_state["min_score"] += coin_value

        return new_state

    def evaluate(self, state):
        return state["max_score"] - state["min_score"]


class AlphaBetaPruning:
    def __init__(self, game):
        self.game = game

    def get_best_move(self, state, is_max_turn, depth=float("inf")):
        best_value = -math.inf if is_max_turn else math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf

        for move in self.game.get_moves(state):
            new_state = self.game.make_move(
                state, move, "Max" if is_max_turn else "Min"
            )
            value = self.minimax(new_state, not is_max_turn, depth - 1, alpha, beta)

            if is_max_turn and value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, best_value)
            elif not is_max_turn and value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, best_value)

        return best_move, best_value

    def minimax(self, state, is_max_turn, depth, alpha, beta):
        if depth == 0 or self.game.is_terminal(state):
            return self.game.evaluate(state)

        if is_max_turn:
            value = -math.inf
            for move in self.game.get_moves(state):
                new_state = self.game.make_move(state, move, "Max")
                value = max(
                    value, self.minimax(new_state, False, depth - 1, alpha, beta)
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for move in self.game.get_moves(state):
                new_state = self.game.make_move(state, move, "Min")
                value = min(
                    value, self.minimax(new_state, True, depth - 1, alpha, beta)
                )
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value


if __name__ == "__main__":
    print("Coin Game with Alpha-Beta Pruning")
    print("=================================")

    coins = [random.randint(1, 9) for _ in range(10)]
    game = CoinGame(coins)
    ai = AlphaBetaPruning(game)
    state = game.get_initial_state()

    while True:
        player_choice = (
            input("Do you want to play as Max or Min? (max/min): ").strip().lower()
        )
        if player_choice in ["max", "min"]:
            break
        print("Invalid choice. Please enter 'max' or 'min'.")

    is_max_turn = player_choice == "max"

    print("\nStarting game with coins:", coins)
    print(
        f"You are {'Max' if is_max_turn else 'Min'}, trying to {'maximize' if is_max_turn else 'minimize'} your score.\n"
    )

    while not game.is_terminal(state):
        game.print_state(state)

        if is_max_turn:
            if player_choice == "max":
                valid_moves = game.get_moves(state)
                while True:
                    move = input("Your turn (Max). Choose 'left' or 'right': ").lower()
                    if move in valid_moves:
                        break
                    print("Invalid move. Try again.")
                state = game.make_move(state, move, "Max")
            else:
                print("Max (AI) is thinking...")
                move, value = ai.get_best_move(state, True)
                print(f"Max chooses {move}")
                state = game.make_move(state, move, "Max")
        else:
            if player_choice == "min":
                valid_moves = game.get_moves(state)
                while True:
                    move = input("Your turn (Min). Choose 'left' or 'right': ").lower()
                    if move in valid_moves:
                        break
                    print("Invalid move. Try again.")
                state = game.make_move(state, move, "Min")
            else:
                print("Min (AI) is thinking...")
                move, value = ai.get_best_move(state, False)
                print(f"Min chooses {move}")
                state = game.make_move(state, move, "Min")

        is_max_turn = not is_max_turn

    print("\nGame Over!")
    print(f"Final scores - Max: {state['max_score']}, Min: {state['min_score']}")
    if state["max_score"] > state["min_score"]:
        print("Max wins!")
    elif state["max_score"] < state["min_score"]:
        print("Min wins!")
    else:
        print("It's a tie!")
