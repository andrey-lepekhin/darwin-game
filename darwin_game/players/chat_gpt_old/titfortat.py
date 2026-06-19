from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class TitForTatPlayer(Player):
    name = "TitForTat"

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        # Start cooperatively
        if not turn_history:
            return 2

        last_turn = turn_history[-1]
        opponent_last_action = last_turn.actions[1 - your_number]

        # Self-play optimization
        if all(turn.actions[0] == turn.actions[1] for turn in turn_history):
            # Alternate between 2 and 3 for maximum self-play score
            return 2 if len(turn_history) % 2 == 0 else 3

        # Mirror opponent's last action with adjustment to prevent the total exceeding 5
        if opponent_last_action <= 2:
            # Aim for mutual cooperation if opponent plays low
            return 3 if opponent_last_action < 2 else 2
        else:
            # Play conservatively if opponent's action could lead to a penalty
            return max(5 - opponent_last_action, 1)
