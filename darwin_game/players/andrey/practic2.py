from random import Random
from collections import Counter, defaultdict

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from line_profiler import profile


class Practic2(Player):
    name = "Practic2"

    """
        
    ___________.__    .__         .__               ___.    _____                     __  .__               
    \__    ___/|  |__ |__| ______ |__| ______   ____\_ |___/ ____\_ __   ____ _____ _/  |_|__| ____   ____  
    |    |   |  |  \|  |/  ___/ |  |/  ___/  /  _ \| __ \   __\  |  \_/ ___\\__  \\   __\  |/  _ \ /    \ 
    |    |   |   Y  \  |\___ \  |  |\___ \  (  <_> ) \_\ \  | |  |  /\  \___ / __ \|  | |  (  <_> )   |  \
    |____|   |___|  /__/____  > |__/____  >  \____/|___  /__| |____/  \___  >____  /__| |__|\____/|___|  /
                    \/        \/          \/             \/                 \/     \/                    \/ 
        in case you don't wanna see the code








































































































    """

    @profile
    def make_turn(self, turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        def most_common_action(actions: list[Action]) -> Action:
            """Return the most common action from a list of actions. In case of a tie, the first action is returned."""
            counts = Counter(actions)
            most_common_element, _ = counts.most_common(1)[0]
            return most_common_element

        turn_num = len(turn_history)

        # If it's the first turn, return a random action
        if turn_num == 0:
            return rng.choice([2, 3])

        # Detect if we're in a start deadlock (both players played the same action in all turns so far)
        for turn in turn_history:
            if turn.actions[0] != turn.actions[1]:
                break
        else:
            return rng.choice([2, 3])

        # Cooperate if opponent cooperated in the last turn and we profited from it
        if turn_history[-1].actions[your_number] == 3 and turn_history[-1].actions[1 - your_number] == 2:
            if sum(turn.results[your_number] for turn in turn_history) < sum(
                turn.results[1 - your_number] for turn in turn_history
            ):
                logger.debug("Opponent is trying to make us cooperate after defecting and not paying the price first")
                return 3
            logger.debug("Cooperate if opponent cooperated in the last turn and we profited from it")
            return 2

        # Calculate how many turns since we're out of start deadlock
        for i, turn_result in enumerate(turn_history):
            if turn_result.actions[0] != turn_result.actions[1]:
                break
        turns_since_non_identical_action = turn_num - i

        # Expecting reciprocal cooperation for 2-3 alternation
        we_cooperated = turn_history[-1].actions[your_number] == 2
        if turn_num > 2:
            we_cooperated = we_cooperated or (
                turn_history[-2].actions[your_number] == 2 and turn_history[-1].actions[your_number] == 3
            )

        # If we cooperated and the opponent profited, it's our turn to profit
        if turn_history[-1].actions[1 - your_number] == 3 and we_cooperated:
            logger.debug("We cooperated and the opponent profited, it's our turn to profit")
            return 3

        cooperation_evaluation_length = turns_since_non_identical_action + 1
        # Calculate how cooperative the opponent was for the last cooperation_evaluation_length turns
        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history[-cooperation_evaluation_length:]]
        opponent_cooperated_times = sum(1 for action in opponent_actions if action in [0, 1, 2])
        # If the opponent was cooperative enough, we expect them to cooperate
        if opponent_cooperated_times >= int(cooperation_evaluation_length / 2):
            logger.debug("If the opponent was cooperative enough, we expect them to cooperate")
            if turn_history[-1].actions[your_number] == 3:
                return 2
            else:
                return 3
            # return 5 - most_common_action(opponent_actions)
        # If the opponent was not cooperative enough
        else:
            # Does opponent change their action?
            if len(set(opponent_actions)) > 1:
                logger.debug("The opponent was not cooperative enough, and changes their action")
                # We assume they are smart enough to change their action
                return 3

        opponent_actions = [turn.actions[1 - your_number] for turn in turn_history]
        opponent_most_common_action = most_common_action(opponent_actions)

        if opponent_most_common_action == 3:
            return 2
        elif opponent_most_common_action == 2:
            return 3
        elif opponent_most_common_action == 1:
            return 4
        elif opponent_most_common_action == 4:
            return 3
        else:
            return 5


# def predict_randomness_efficient(opponent_turns):
#     # Define the subsets of interest
#     subsets = {
#         '(1, 2, 3)': set([1, 2, 3]),
#         '(2, 3)': set([2, 3]),
#         '(1, 2, 3, 4, 5)': set([1, 2, 3, 4, 5]),
#         '(3, 4, 5)': set([3, 4, 5])
#     }

#     # Calculate observed frequencies for each possible turn (0-5)
#     observed_freq = [opponent_turns.count(i) for i in range(6)]

#     # Prepare a dictionary to hold deviation scores for each subset
#     deviation_scores = {}

#     for subset_label, subset_numbers in subsets.items():
#         # Calculate the total number of turns that fall within the subset
#         total_subset_turns = sum(observed_freq[i] for i in subset_numbers)

#         # The expected frequency for each turn in the subset, if randomly distributed
#         expected_freq_per_turn = total_subset_turns / len(subset_numbers)

#         # Calculate the deviation score as the sum of absolute differences
#         # between observed and expected frequencies for turns in the subset
#         deviation_score = sum(abs(observed_freq[i] - expected_freq_per_turn) for i in subset_numbers)

#         # Normalize the deviation score by the total number of turns
#         if total_subset_turns > 0:
#             deviation_scores[subset_label] = deviation_score / total_subset_turns
#         else:
#             deviation_scores[subset_label] = float('inf')  # Impossibly high score if no turns fall within the subset

#     # Return the subset with the minimum deviation score
#     min_deviation_subset = min(deviation_scores, key=deviation_scores.get)
#     return min_deviation_subset, deviation_scores

# # Example usage with a hypothetical set of turns
# predict_randomness_efficient(example_turns)


"""boop"""
