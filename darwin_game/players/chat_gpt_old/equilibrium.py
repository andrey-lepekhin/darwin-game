from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class Equilibrium(Player):
    name = "Equilibrium"

    def __init__(self):
        self.last_opponent_action = None

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        if not turn_history:
            # Start cooperatively in the first turn
            return 2

        # Determine the last action of the opponent
        self.last_opponent_action = turn_history[-1].actions[1 - your_number]

        # Evaluate the game phase to adjust strategy
        game_phase = len(turn_history) / 102  # Assuming 102 turns as a rough game length

        if game_phase < 0.3:
            # Early game: Experiment with a mix of cooperation and mild aggression
            strategy = self.early_game_strategy()
        elif game_phase < 0.6:
            # Mid game: Adapt based on opponent's behavior, leaning towards equilibrium
            strategy = self.mid_game_strategy()
        else:
            # Late game: Prioritize maintaining equilibrium, avoid risky moves
            strategy = self.late_game_strategy()

        return strategy

    def early_game_strategy(self):
        # Alternate between cooperation and mild aggression
        return 3 if self.last_opponent_action in [0, 1, 2] else 2

    def mid_game_strategy(self):
        # Tit-for-tat with forgiveness to encourage cooperation
        if self.last_opponent_action in [4, 5]:
            return 1  # Defensive play to avoid overcommitting
        elif self.last_opponent_action == 3:
            return 2  # Mirror mild aggression or cooperation
        else:
            return 3  # Encourage cooperation by showing willingness to cooperate

    def late_game_strategy(self):
        # Avoid actions that could lead to mutual loss, prioritize safe scoring
        if self.last_opponent_action in [3, 4, 5]:
            return 2  # Opt for a safer approach
        else:
            return 3  # Slightly more aggressive if the opponent is playing conservatively
