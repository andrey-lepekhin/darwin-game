from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class P3(Player):
    name = "2 or 3"

    @staticmethod
    def make_turn(turn_history, your_number, rng: Random):
        return rng.choice([2, 3])


class P4(Player):
    name = "Always 3"

    @staticmethod
    def make_turn(turn_history, your_number, rng: Random):
        return 3


class OldMimic(Player):
    name = "OldMimic"

    @staticmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        if not turn_history:
            return rng.choice([2, 3])

        friend_previous_turn = turn_history[-1].actions[1 - your_number]
        our_previous_turn = turn_history[-1].actions[your_number]

        if friend_previous_turn == our_previous_turn:
            return rng.choice([2, 3])

        if friend_previous_turn > our_previous_turn:
            return 3
        if friend_previous_turn < our_previous_turn:
            return 2
        return rng.choice([2, 3])
