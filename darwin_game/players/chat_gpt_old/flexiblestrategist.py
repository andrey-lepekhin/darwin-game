from random import Random

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult


class FlexibleStrategist(Player):
    name = "FlexibleStrategist"

    def predict_opponent_next_action(self, turn_history, your_number):
        if not turn_history:
            return 2
        recent_opponent_actions = [turn.actions[1 - your_number] for turn in turn_history[-3:]]
        return max(set(recent_opponent_actions), key=recent_opponent_actions.count)

    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        if not turn_history:
            return 2

        predicted_opponent_action = self.predict_opponent_next_action(turn_history, your_number)

        game_phase = len(turn_history)
        if game_phase < 20:
            return rng.randint(1, 3)
        elif game_phase < 40:
            if predicted_opponent_action > 2:
                return max(5 - predicted_opponent_action, 1)
            else:
                return min(predicted_opponent_action + 1, 3)
        else:
            if all(turn.actions[1 - your_number] == 2 for turn in turn_history[-5:]):
                return 3
            elif any(turn.actions[1 - your_number] > 3 for turn in turn_history[-5:]):
                return 2
            else:
                return 2 if game_phase % 2 == 0 else 3
