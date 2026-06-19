from darwin_game.core.import_players import find_import_player_classes
from darwin_game.core.rng import batch_seed, game_seed
from darwin_game.core.tournament import DarwinGame


def test_game_seed_formula():
    assert game_seed(7, 2, 3) == 7 + 2 * 1_000_000 + 3
    assert batch_seed(7, 2) == 7 + 2 * 1_000_000


def test_tournament_same_seed_same_results():
    player_classes = find_import_player_classes("darwin_game/players/simple")
    kwargs = dict(
        player_classes=player_classes,
        rounds=3,
        initial_player_copies=4,
        game_turns=10,
        lowest_pool_percent_for_player=None,
        quiet=True,
        base_seed=12345,
    )
    results_a = DarwinGame(**kwargs).run_tournament()
    results_b = DarwinGame(**kwargs).run_tournament()
    assert results_a == results_b
