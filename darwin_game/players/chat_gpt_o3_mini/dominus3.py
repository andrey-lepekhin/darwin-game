from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class DominusV3(Player):
    name = "DominusV3"

    @staticmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        opponent = 1 - your_number
        signal = [2, 3, 2]
        if len(turn_history) < 3:
            return signal[len(turn_history)]

        opp_initial = [turn.actions[opponent] for turn in turn_history[:3]]
        rocket_mode = opp_initial == signal

        my_score = sum(turn.results[your_number] for turn in turn_history)
        opp_score = sum(turn.results[opponent] for turn in turn_history)

        opp_moves = [turn.actions[opponent] for turn in turn_history]
        count2 = opp_moves.count(2)
        count3 = opp_moves.count(3)
        exploitation = False
        if count2 > count3 or (opp_score - my_score >= 2):
            exploitation = True

        if rocket_mode:
            last_turn = turn_history[-1]
            my_last = last_turn.actions[your_number]
            opp_last = last_turn.actions[opponent]
            if my_last + opp_last == 5:
                return my_last
            else:
                return 3 if rng.random() < 0.8 else 2

        if exploitation:
            return 3

        last_turn = turn_history[-1]
        my_last = last_turn.actions[your_number]
        opp_last = last_turn.actions[opponent]
        if my_last + opp_last == 5:
            return 3 if my_last == 2 else 2

        if opp_last in [2, 3]:
            return opp_last

        return rng.choice([2, 3])
