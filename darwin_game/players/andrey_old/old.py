from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class OldAndrey(Player):
    name = "OldAndrey"

    @staticmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        def antideadlock():
            rnd = rng.random()
            if rnd <= 0.12:
                return 1
            if rnd <= 0.6:
                return 2
            return 3

        turn_num = len(turn_history) + 1

        if turn_num == 1:
            return antideadlock()

        friend_previous_turn = turn_history[-1].actions[1 - your_number]
        our_previous_turn = turn_history[-1].actions[your_number]
        opponent_points = sum(turn.results[1 - your_number] for turn in turn_history)
        our_points = sum(turn.results[your_number] for turn in turn_history)

        threshold = 5
        if turn_num > threshold:
            opponent_is_superior = False
            if turn_num > threshold * 2 and opponent_points > our_points + 3:
                opponent_is_superior = True

            if opponent_is_superior:
                if opponent_points - our_points > 5:
                    return 5
                return opponent_points - our_points

        for turn in turn_history:
            if turn.actions[0] != turn.actions[1]:
                break
        else:
            return antideadlock()

        if friend_previous_turn == our_previous_turn:
            if opponent_points > our_points:
                return 3
            if opponent_points < our_points:
                return 2
            if turn_num > threshold * 2:
                return 3

        if opponent_points > our_points:
            return 3
        if opponent_points < our_points:
            return 2
        if opponent_points == our_points:
            if our_previous_turn == 2:
                return 3
            if our_previous_turn == 3:
                return 2

        return antideadlock()
