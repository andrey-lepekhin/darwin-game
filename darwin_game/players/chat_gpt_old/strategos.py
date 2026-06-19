from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class StrategosBot(Player):
    """A strategic player that adapts to opponent's behavior."""

    name: str = "StrategosBot"

    @staticmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        if not turn_history:
            return rng.choice([2, 3])

        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        opponent_last_action = opponent_actions[-1]

        if len(turn_history) >= 4 and all(a == b for a, b in zip(opponent_actions[-4:], [2, 3, 2, 3])):
            return 3 if (len(turn_history) + 1) % 2 == 0 else 2

        if opponent_last_action in [0, 1, 2]:
            return 3
        elif opponent_last_action in [3, 4, 5]:
            return 2

        return 2
