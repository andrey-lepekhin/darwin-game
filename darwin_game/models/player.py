"""Abstract class for players"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from random import Random
from typing import Literal

AllowedNumbers = Literal[0, 1, 2, 3, 4, 5]

Action = AllowedNumbers  # An action a player can take

Result = AllowedNumbers  # The result of an action for a player


@dataclass(slots=True, frozen=True)
class TurnResult:
    # Result of a turn for consumption by a specific player.
    # Used in Player.make_turn() to make decisions.
    actions: tuple[Action, Action]
    results: tuple[Result, Result]


class PlayerNumber(IntEnum):
    # Your player's position in TurnResult
    PLAYER1 = 0
    PLAYER2 = 1


class Player(ABC):
    """Abstract class for players"""

    name: str  # The name of the player

    @staticmethod
    @abstractmethod
    def make_turn(turn_history: list[TurnResult], your_number: PlayerNumber, rng: Random) -> Action:
        """
        Choose an action to play. You're allowed to use ONLY the information in input params.
        Do not store any information between turns.

        Args:
            turn_history (list[TurnResult]): The results of the previous turns.
            New results are appended to the end of the list.

            your_number (PlayerNumber): Your player's position in TurnResult. "0" if you are player1,
            "1" if you are player2. I.e. turn_history[-1].actions[your_number] is your action in the last turn,
            and turn_history[-1].actions[1 - your_number] is your opponent's action.
            Do not use your_number to coordinate with e.g. copies of yourself.
            Columns are random for each player in the same game.

            rng (Random): A per-game random number generator. Use this instead of the global random module.
        """
        # The only code you need to write is in this method
        ...


# See /players for examples of how to implement a player
