from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class DefensiveOptimizer(Player):
    name = "DefensiveOptimizer"

    def calculate_safe_action(self, turn_history, your_number):
        # Determines a safe action based on the opponent's past actions
        if not turn_history:
            return 2  # Default to a conservative start

        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        average_opponent_action = sum(opponent_actions) / len(opponent_actions)

        # Adjust strategy based on the opponent's average action
        if average_opponent_action < 2.5:
            # If the opponent is playing conservatively, play slightly more aggressively
            return 3
        elif average_opponent_action > 2.5:
            # If the opponent is aggressive, play more conservatively to avoid penalties
            return 2
        else:
            # If the opponent is balanced, maintain a conservative strategy
            return 2

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        safe_action = self.calculate_safe_action(turn_history, your_number)

        # Enhance strategy for late game
        game_phase = len(turn_history)
        if game_phase > 50:
            # In the late game, adjust actions to be even more conservative
            # if leading or to take calculated risks if trailing
            if safe_action == 3 and any(turn.actions[1 - your_number] == 0 for turn in turn_history[-5:]):
                # If there's a recent trend of extremely conservative play by the opponent, adjust to ensure scoring
                return 3
            else:
                return 2
        else:
            return safe_action
