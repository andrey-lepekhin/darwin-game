from time import perf_counter
from dataclasses import dataclass, field
import logging

from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult

logger = logging.getLogger(__name__)

# Precomputed (player1_result, player2_result) for each action pair.
PAYOFF: tuple[tuple[tuple[int, int], ...], ...] = tuple(
    tuple((0, 0) if a + b > 5 else (a, b) for b in range(6)) for a in range(6)
)


@dataclass(slots=True)
class Game:
    player1: Player
    player2: Player
    max_turns: int
    debug_per_turn_results: bool = False
    check_timeouts: bool = True
    turn_timeout_seconds: float = 0.0003

    turn_history: list[TurnResult] = field(default_factory=list, init=False)
    turn_number: int = field(default=0, init=False)
    player1_score: int = field(default=0, init=False)
    player2_score: int = field(default=0, init=False)

    def _get_turn_result(self, player1_action: Action, player2_action: Action) -> TurnResult:
        player1_result, player2_result = PAYOFF[player1_action][player2_action]
        return TurnResult(
            (player1_action, player2_action),
            (player1_result, player2_result),  # type: ignore[arg-type]
        )

    def _call_make_turn(
        self,
        make_turn,
        history: list[TurnResult],
        player_number: PlayerNumber,
        player: Player,
    ) -> Action:
        if self.check_timeouts:
            start_time = perf_counter()
            try:
                turn_action = make_turn(history, player_number)
                if perf_counter() - start_time > self.turn_timeout_seconds:
                    raise TimeoutError(
                        f"{player} took more than {self.turn_timeout_seconds} seconds to make a turn."
                    )
            except Exception as e:
                logger.debug(f"{player} failed with error: {e}. Counting that as a 0 action.")
                return 0
        else:
            try:
                turn_action = make_turn(history, player_number)
            except Exception as e:
                logger.debug(f"{player} failed with error: {e}. Counting that as a 0 action.")
                return 0

        if not 0 <= turn_action <= 5:
            logger.debug(f"{player} returned a non-Action object: {turn_action}. Counting that as a 0 action.")
            return 0
        return turn_action

    def _play_turn(self) -> None:
        history = self.turn_history
        player1_action = self._call_make_turn(
            self.player1.make_turn, history, PlayerNumber.PLAYER1, self.player1
        )
        player2_action = self._call_make_turn(
            self.player2.make_turn, history, PlayerNumber.PLAYER2, self.player2
        )
        if self.debug_per_turn_results:
            logger.debug(
                f"{self.turn_number}: {self.player1.name}: {player1_action}, "
                f"{self.player2.name}: {player2_action}"
            )

        player1_result, player2_result = PAYOFF[player1_action][player2_action]
        self.player1_score += player1_result
        self.player2_score += player2_result
        history.append(TurnResult((player1_action, player2_action), (player1_result, player2_result)))  # type: ignore[arg-type]
        self.turn_number += 1

    def _reset_game(self) -> None:
        self.turn_history = []
        self.turn_number = 0
        self.player1_score = 0
        self.player2_score = 0

    def play_game(self) -> dict[Player, int]:
        self._reset_game()

        player1 = self.player1
        player2 = self.player2
        history = self.turn_history
        history_append = history.append
        p1_make_turn = player1.make_turn
        p2_make_turn = player2.make_turn
        max_turns = self.max_turns
        debug = self.debug_per_turn_results
        check_timeouts = self.check_timeouts
        turn_timeout = self.turn_timeout_seconds

        p1_score = 0
        p2_score = 0
        turn_num = 0

        if check_timeouts:
            while turn_num < max_turns:
                player1_action = self._call_make_turn(p1_make_turn, history, PlayerNumber.PLAYER1, player1)
                player2_action = self._call_make_turn(p2_make_turn, history, PlayerNumber.PLAYER2, player2)
                if debug:
                    logger.debug(
                        f"{turn_num}: {player1.name}: {player1_action}, {player2.name}: {player2_action}"
                    )

                player1_result, player2_result = PAYOFF[player1_action][player2_action]
                p1_score += player1_result
                p2_score += player2_result
                history_append(
                    TurnResult((player1_action, player2_action), (player1_result, player2_result))  # type: ignore[arg-type]
                )
                turn_num += 1
        else:
            while turn_num < max_turns:
                try:
                    player1_action = p1_make_turn(history, PlayerNumber.PLAYER1)
                except Exception as e:
                    logger.debug(f"{player1} failed with error: {e}. Counting that as a 0 action.")
                    player1_action = 0
                if not 0 <= player1_action <= 5:
                    player1_action = 0

                try:
                    player2_action = p2_make_turn(history, PlayerNumber.PLAYER2)
                except Exception as e:
                    logger.debug(f"{player2} failed with error: {e}. Counting that as a 0 action.")
                    player2_action = 0
                if not 0 <= player2_action <= 5:
                    player2_action = 0

                if debug:
                    logger.debug(
                        f"{turn_num}: {player1.name}: {player1_action}, {player2.name}: {player2_action}"
                    )

                player1_result, player2_result = PAYOFF[player1_action][player2_action]
                p1_score += player1_result
                p2_score += player2_result
                history_append(
                    TurnResult((player1_action, player2_action), (player1_result, player2_result))  # type: ignore[arg-type]
                )
                turn_num += 1

        self.turn_number = turn_num
        self.player1_score = p1_score
        self.player2_score = p2_score
        return {player1: p1_score, player2: p2_score}
