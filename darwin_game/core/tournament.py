from dataclasses import dataclass
import logging
from enum import StrEnum

from tabulate import tabulate  # type: ignore
from tqdm.auto import tqdm

from darwin_game.core.game import Game
from darwin_game.core.graph_utils import (
    colored_player_names,
    colored_player_names_for_pbar,
    colored_single_round_results,
)
from darwin_game.core.rng import batch_seed, game_seed, local_rng
from darwin_game.models.player import Player


logger = logging.getLogger(__name__)


class MatchupType(StrEnum):
    RANDOM_PAIRING = "RandomPairing"
    ROUND_ROBIN = "RoundRobin"


@dataclass
class DarwinGame:
    """A class to run a Darwin Game tournament between a list of Player classes."""

    player_classes: list[type[Player]]
    rounds: int = 100  # Number of rounds to play in the tournament
    initial_player_copies: int = 100  # Number of copies of each player to start with; should be even > 1
    game_turns: int = 100  # Number of turns per game
    matchup_type: MatchupType = MatchupType.RANDOM_PAIRING
    quiet: bool = False  # Suppress live tournament output (progress bars, per-round stats)
    check_timeouts: bool | None = None  # Per-turn timing; defaults to not quiet
    base_seed: int = 0


    lowest_pool_percent_for_player: float | None = (
        0.01  # Players taking up less than this percentage of the pool are taken out
    )

    def __post_init__(self) -> None:
        if self.check_timeouts is None:
            self.check_timeouts = not self.quiet

        self.pool: list[Player] = self.initialize_pool()
        self.pool_exemplars_by_class: dict[type[Player], int] = {
            player_class: 0 for player_class in self.player_classes
        }

        if self.initial_player_copies % 2 != 0:
            raise ValueError("initial_player_copies should be an even number")
        self.total_exemplars: int = self.initial_player_copies * len(self.player_classes)

    def initialize_pool(self) -> list[Player]:
        # Check that player names are unique
        player_names = [player.name for player in self.player_classes]
        if len(player_names) != len(set(player_names)):
            raise ValueError("Player names must be unique")

        # Initialize the pool with equal number of copies of each player
        pool = []
        for player_class in self.player_classes:
            for _ in range(self.initial_player_copies):
                # append a copy instance of the player
                pool.append(player_class())

        return pool

    def _play_single_game_and_update_results(
        self,
        player1: Player,
        player2: Player,
        results: dict[type[Player], int],
        *,
        round_index: int,
        game_index: int,
    ) -> None:
        game = Game(
            player1,
            player2,
            max_turns=self.game_turns,
            seed=game_seed(self.base_seed, round_index, game_index),
            check_timeouts=self.check_timeouts,
        )
        game_result = game.play_game()
        logger.debug([f"{player.name}: {result}" for player, result in game_result.items()])
        for player, points in game_result.items():
            results[player.__class__] += points

    def play_round(self, round_index: int) -> dict[type[Player], int]:
        results = {player_class: 0 for player_class in self.player_classes}
        round_rng = local_rng(batch_seed(self.base_seed, round_index))

        if self.matchup_type == MatchupType.RANDOM_PAIRING:
            round_rng.shuffle(self.pool)
            for game_index, i in enumerate(range(0, len(self.pool), 2), start=1):
                self._play_single_game_and_update_results(
                    self.pool[i],
                    self.pool[i + 1],
                    results,
                    round_index=round_index,
                    game_index=game_index,
                )

        elif self.matchup_type == MatchupType.ROUND_ROBIN:
            game_index = 0
            for i, player1 in enumerate(self.pool[:-1]):  # No need to include the last player in the outer loop
                for player2 in self.pool[i + 1 :]:
                    game_index += 1
                    self._play_single_game_and_update_results(
                        player1,
                        player2,
                        results,
                        round_index=round_index,
                        game_index=game_index,
                    )

        return results

    def adjust_population(self, round_results: dict[type[Player], int], round_index: int) -> None:
        round_rng = local_rng(batch_seed(self.base_seed, round_index))
        self.pool_exemplars_by_class = {player_class: 0 for player_class in self.player_classes}
        total_points = sum(round_results.values())
        new_pool = []
        for player_class, points in round_results.items():
            try:
                num_exemplars = int(self.total_exemplars * (points / total_points))
            except ZeroDivisionError:
                num_exemplars = 0
            self.pool_exemplars_by_class[player_class] += num_exemplars
            if self.lowest_pool_percent_for_player and num_exemplars < int(
                self.lowest_pool_percent_for_player * self.total_exemplars
            ):
                continue  # Skip adding the player to the pool if players' percentage in the pool is too low
            for _ in range(num_exemplars):
                new_pool.append(player_class())

        # If the new pool size < total exemplars due to rounding errors,
        # add exemplars randomly from surviving players.
        while len(new_pool) < self.total_exemplars:
            player_class = round_rng.choice(
                [player_class for player_class, exemplars in self.pool_exemplars_by_class.items() if exemplars > 0]
            )
            new_pool.append(player_class())

        self.pool = new_pool

    def get_results(self) -> dict[type[Player], int]:
        results = {player_class: 0 for player_class in self.player_classes}
        for player in self.pool:
            results[player.__class__] += 1
        return results

    def pretty_print_results(self, results: dict[type[Player], int]) -> None:
        print("Results of the tournament:")
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        table = []
        for player_class, exemplars in sorted_results:
            table.append([player_class.name, exemplars, round(exemplars / self.total_exemplars * 100)])
        print(tabulate(table, headers=["Player", "Copies in the pool", "%"], tablefmt="simple_grid"))

    def _print_tournament_start(self) -> None:
        print(colored_player_names(self.player_classes))
        print(
            colored_single_round_results(
                {player_class: self.initial_player_copies for player_class in self.player_classes}
            )
        )

    def run_tournament(self) -> dict[type[Player], int]:
        if not self.quiet:
            self._print_tournament_start()

        player_stats_bar = tqdm(
            range(1), desc="Top players", bar_format="{desc}", position=0, disable=self.quiet
        )
        pbar = tqdm(range(self.rounds), desc="Playing rounds", position=1, disable=self.quiet)

        for round_index in pbar:
            round_results = self.play_round(round_index)
            if not self.quiet:
                pbar.write(colored_single_round_results(round_results))
                player_stats_bar.set_description("Top: " + colored_player_names_for_pbar(round_results))
            self.adjust_population(round_results, round_index)

            # Stop when the population has converged to a winning strategy.
            # I.e., when all exemplars in the pool are of the same class.
            if len(set(type(player) for player in self.pool)) == 1:
                break

        return self.get_results()
