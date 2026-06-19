from collections import Counter
from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class Predictive(Player):
    name = "Predictive"

    def predict_opponent_next_action(self, turn_history, your_number):
        if not turn_history:
            return 2

        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        action_frequencies = Counter(opponent_actions)
        return action_frequencies.most_common(1)[0][0]

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        predicted_opponent_action = self.predict_opponent_next_action(turn_history, your_number)

        if all(turn.actions[0] == turn.actions[1] for turn in turn_history if turn_history):
            return 2 if len(turn_history) % 2 == 0 else 3

        if predicted_opponent_action in [0, 1]:
            return 5 - predicted_opponent_action
        elif predicted_opponent_action in [4, 5]:
            return 1
        else:
            current_phase = len(turn_history) // 10
            if current_phase < 5:
                return 3 if rng.random() > 0.5 else 2
            else:
                return 2
