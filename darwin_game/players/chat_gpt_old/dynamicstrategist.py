from random import Random

from darwin_game.models.player import Player, PlayerNumber, TurnResult


class DynamicStrategistBot(Player):
    name = "DynamicStrategistBot"

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> int:
        if not turn_history:
            return rng.choice([2, 3])

        last_opponent_action = turn_history[-1].actions[1 - your_number]

        if len(turn_history) < 5:
            return last_opponent_action

        if len(turn_history) < 10:
            return rng.choice([1, 2, 3, 4])

        if last_opponent_action in [2, 3]:
            return 3 if rng.random() > 0.5 else 2
        else:
            return 2 if last_opponent_action > 3 else 3
