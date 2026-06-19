import argparse
import logging

from darwin_game.core.import_players import find_import_player_classes
from darwin_game.core.tournament import DarwinGame, MatchupType

PLAYERS_FOLDER = "darwin_game/players"
INCLUDE_DIRS = [
    "simple",
    "chat_gpt_old",
    "andrey",
    "tony",
    "old_guard",
    "chat_gpt_o3_mini",
]


def create_tournament(*, quiet: bool = False, base_seed: int = 0) -> DarwinGame:
    player_classes = find_import_player_classes(PLAYERS_FOLDER, INCLUDE_DIRS)
    return DarwinGame(
        player_classes=player_classes,
        rounds=50,
        initial_player_copies=20,
        game_turns=100,
        matchup_type=MatchupType.RANDOM_PAIRING,
        quiet=quiet,
        base_seed=base_seed,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Darwin Game tournament.")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress player names, per-round results, and progress bars (final standings still printed).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Base seed for reproducible tournaments (pairings, games, population adjustment).",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)  # set to DEBUG for more info. Will break pretty print

    tournament = create_tournament(quiet=args.quiet, base_seed=args.seed)
    results = tournament.run_tournament()
    tournament.pretty_print_results(results)


if __name__ == "__main__":
    main()
