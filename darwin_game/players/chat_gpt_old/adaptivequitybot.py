from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class AdaptiveEquityBot(Player):
    name: str = "AdaptiveEquityBot"

    def assess_opponent_aggression(self, turn_history: list[TurnResult], your_number: PlayerNumber) -> str:
        aggressive_actions = 0
        total_actions = 0
        for turn in turn_history:
            opponent_action = turn.actions[1 - your_number]
            if opponent_action >= 3:
                aggressive_actions += 1
            total_actions += 1

        # Define aggression based on a simple majority of aggressive actions
        if aggressive_actions / total_actions > 0.5:
            return "aggressive"
        elif aggressive_actions / total_actions <= 0.5:
            return "cooperative"
        else:
            return "unknown"

    def last_action(self, your_number: PlayerNumber, turn_history: list[TurnResult]) -> Action:
        if not turn_history:
            return 2  # Default starting action
        return turn_history[-1].actions[your_number]

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        # Start with a cooperative approach
        if not turn_history:
            return 2

        last_turn = turn_history[-1]
        opponent_action = last_turn.actions[1 - your_number]

        # Strategy to adapt based on opponent's behavior
        opponent_aggression_level = self.assess_opponent_aggression(turn_history, your_number)

        if opponent_aggression_level == "cooperative":
            # Alternate between 2 and 3 to aim for fair cooperation
            return 3 if self.last_action(your_number, turn_history) == 2 else 2
        elif opponent_aggression_level == "aggressive":
            # Defensive play against aggression
            return 2  # Lean towards safety, adjust as necessary
        else:
            # Default to a balanced approach for uncertain patterns
            return 2 if opponent_action in [0, 1, 2] else 3


# Example of creating an instance of the player
player = AdaptiveEquityBot()
