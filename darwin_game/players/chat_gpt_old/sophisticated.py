from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class SophisticatedPlayer(Player):
    name = "Sophisticated"

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        # Start with a cooperative strategy
        if not turn_history:
            return 2

        # Analyze opponent's past actions
        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        my_actions = [turn.actions[your_number] for turn in turn_history]

        # Strategy adjustment based on opponent's behavior
        cooperation_level = sum(opponent_actions) / len(opponent_actions)
        my_cooperation_level = sum(my_actions) / len(my_actions)

        # Adjust strategy based on the game stage and opponent's behavior
        if cooperation_level > 2.5:
            # If the opponent is aggressive, play defensively
            return max(0, 5 - int(cooperation_level))  # Defensive play
        elif my_cooperation_level < 2.5:
            # If we've been playing too defensively, try to cooperate more
            return 3
        else:
            # Continue cooperation or adjust based on opponent's last action
            last_opponent_action = opponent_actions[-1]
            if last_opponent_action in [2, 3]:
                # If opponent cooperates, reciprocate cooperation
                return 3 if my_actions[-1] == 2 else 2
            else:
                # Adjust strategy to avoid losses
                return 2 if sum([my_actions[-1], last_opponent_action]) > 5 else 3
