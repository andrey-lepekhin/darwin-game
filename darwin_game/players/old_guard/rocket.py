from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class Rocket(Player):
    name = "Rocket"

    @staticmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        my_signal = [2, 3, 2]
        if len(turn_history) < 3:
            return my_signal[len(turn_history)]
        his_signal = [turn.actions[1 - your_number] for turn in turn_history[:3]]
        copy_of_myself = his_signal == my_signal

        if len(turn_history) > 3:
            my_previous_turn, his_previous_turn = (
                turn_history[-1].actions[your_number],
                turn_history[-1].actions[1 - your_number],
            )
            if copy_of_myself:
                if my_previous_turn + his_previous_turn == 5:
                    return my_previous_turn
            else:
                if my_previous_turn == his_previous_turn:
                    return rng.choice([2, 3])
        return rng.choice([2, 3])
