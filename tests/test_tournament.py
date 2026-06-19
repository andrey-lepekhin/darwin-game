import platform
from unittest.mock import patch

from darwin_game.core.import_players import find_import_player_classes
from darwin_game.core.tournament import DarwinGame
from darwin_game.benchmark import check_native_arm64


def test_run_tournament_quiet(capsys):
    tournament = DarwinGame(
        player_classes=find_import_player_classes("darwin_game/players/simple"),
        rounds=2,
        initial_player_copies=4,
        game_turns=10,
        lowest_pool_percent_for_player=None,
        quiet=True,
    )
    results = tournament.run_tournament()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert sum(results.values()) == tournament.total_exemplars


def test_check_native_arm64_passes_on_arm64():
    with patch.object(platform, "machine", return_value="arm64"):
        check_native_arm64()


def test_check_native_arm64_fails_on_rosetta(capsys):
    with (
        patch.object(platform, "machine", return_value="x86_64"),
        patch("darwin_game.benchmark.sys.platform", "darwin"),
        patch("darwin_game.benchmark.sys.exit") as mock_exit,
    ):
        check_native_arm64()
        mock_exit.assert_called_once_with(1)
        assert "Rosetta" in capsys.readouterr().err
