from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class Adaptive(Player):
    name = "Adaptive"

    @staticmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        # Start with a cooperative strategy
        if not turn_history:
            return 2

        last_turn = turn_history[-1]
        opponent_last_action = last_turn.actions[1 - your_number]

        # Analyze opponent's behavior
        opponent_aggression = sum(turn.actions[1 - your_number] > 2 for turn in turn_history) / len(turn_history)

        # Self-play recognition
        if all(turn.actions[0] == turn.actions[1] for turn in turn_history):
            # Optimize self-play score
            return 2 if len(turn_history) % 2 == 0 else 3

        # Adjust strategy based on opponent's past behavior
        if opponent_aggression > 0.5:
            # If opponent is aggressive, play defensively
            return 2
        else:
            # Otherwise, aim for a balanced approach
            if opponent_last_action in [0, 1]:
                return 5 - opponent_last_action
            elif opponent_last_action in [4, 5]:
                return 1  # Play conservatively to avoid point loss
            else:
                # Continue cooperating if it seems beneficial
                return 2 if opponent_last_action >= 3 else 3
