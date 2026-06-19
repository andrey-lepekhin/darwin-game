from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class QuantumStrategist(Player):
    name = "QuantumStrategist"

    def __init__(self):
        self.strategy_mode = "initial"
        self.prediction_accuracy = 0.75

    def predict_opponent_action(self, turn_history, your_number, rng: Random):
        if not turn_history:
            return 2
        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        most_common_action = max(set(opponent_actions), key=opponent_actions.count)
        if rng.random() > self.prediction_accuracy:
            return rng.randint(0, 5)
        return most_common_action

    def select_strategy(self, turn_history, your_number):
        game_phase = len(turn_history)
        if game_phase < 20:
            self.strategy_mode = "aggressive"
        elif game_phase < 40:
            self.strategy_mode = "adaptive"
        else:
            self.strategy_mode = "conservative"

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        predicted_action = self.predict_opponent_action(turn_history, your_number, rng)
        self.select_strategy(turn_history, your_number)

        if self.strategy_mode == "aggressive":
            return min(predicted_action + 1, 5)
        elif self.strategy_mode == "adaptive":
            if predicted_action <= 2:
                return 3
            else:
                return 2
        else:
            if predicted_action >= 3:
                return 2
            else:
                return predicted_action
