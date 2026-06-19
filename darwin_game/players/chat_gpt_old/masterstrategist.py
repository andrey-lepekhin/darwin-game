from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class MasterStrategist(Player):
    name = "MasterStrategist"

    def __init__(self):
        self.random_factor = 0.1

    def analyze_opponent_behavior(
        self, turn_history, your_number, rng: Random
    ) -> Action:
        if len(turn_history) < 5:
            return rng.randint(2, 3)

        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        my_actions = [turn.actions[your_number] for turn in turn_history]

        opponent_aggressiveness = sum(action > 2 for action in opponent_actions) / len(opponent_actions)

        game_phase = len(turn_history)
        if game_phase <= 20:
            return 3 if rng.random() > self.random_factor else 2
        elif game_phase <= 40:
            if opponent_aggressiveness > 0.5:
                self.random_factor = min(self.random_factor + 0.1, 0.5)
                return 2 if rng.random() > opponent_aggressiveness else 3
            else:
                return 2 if rng.random() > 0.5 else 3
        else:
            self.random_factor = 0
            if sum(my_actions) / len(my_actions) > sum(opponent_actions) / len(opponent_actions):
                return 2
            else:
                return 3 if rng.random() > 0.5 else 2

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        return self.analyze_opponent_behavior(turn_history, your_number, rng)
