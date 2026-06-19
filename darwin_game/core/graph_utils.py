import hashlib
import os
from itertools import product

from termcolor import RESET, colored

from darwin_game.models.player import Player

try:
    terminal_width, _ = os.get_terminal_size(0)
except OSError:
    terminal_width = 80
graph_width = terminal_width - 10

# List of terminal-safe colors
available_colors = [
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
]
highlight_colors = [
    "on_grey",
    "on_red",
    "on_green",
    "on_yellow",
    "on_blue",
    "on_magenta",
    "on_cyan",
    "on_light_grey",
    "on_dark_grey",
    "on_light_red",
    "on_light_green",
    "on_light_yellow",
    "on_light_blue",
    "on_light_magenta",
    "on_light_cyan",
]
symbols = ["●", "♠", "▪", "✦", "◆", "●", "▪", "♦"]
# symbols = ["★", "▘",    "▙",    "▚",    "▛",    "▜", "□", "▪", "♥"]


class PlayerColorAssigner:
    def __init__(
        self,
        available_colors: list[str],
        highlight_colors: list[str],
        symbols: list[str],
    ) -> None:
        self.available_colors = available_colors
        self.highlight_colors = highlight_colors
        self.symbols = symbols
        self.all_combinations = list(product(available_colors, highlight_colors, symbols))
        self.player_combinations: dict[str, tuple] = {}

    def hash_name(self, name: str) -> int:
        return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16)

    def get_player_colors(self, name: str) -> tuple:
        if name in self.player_combinations:
            return self.player_combinations[name]

        hash_val = self.hash_name(name)
        index = hash_val % len(self.all_combinations)

        # Ensure uniqueness by attempting to find an unused combination.
        used_combinations = set(self.player_combinations.values())
        while self.all_combinations[index] in used_combinations:
            index = (index + 1) % len(self.all_combinations)

        self.player_combinations[name] = self.all_combinations[index]
        return self.all_combinations[index]


assigner = PlayerColorAssigner(available_colors, highlight_colors, symbols)


def colored_player_names(players: list[type[Player]]) -> str:
    names = ""
    for player in players:
        color, background_color, symbol = assigner.get_player_colors(player.name)
        names += (
            colored(
                f"{symbol} {player.name}",
                color,
                attrs=["bold"],
                on_color=background_color,
            )
            + " "
        )
    return names


def colored_player_names_for_pbar(round_results: dict[type[Player], int]) -> str:
    names = ""
    # sort by points first
    round_results = dict(sorted(round_results.items(), key=lambda item: item[1], reverse=True))
    for player, _ in round_results.items():
        color, background_color, symbol = assigner.get_player_colors(player.name)
        names += (
            colored(
                f"{symbol} {player.name}",
                color,
                attrs=["bold"],
                on_color=background_color,
            )
            + " "
        )

        if len(names) > terminal_width - 10:
            names += RESET + "..."
            break
    return names


def colored_single_round_results(round_result: dict[type[Player], int], graph_width: int = graph_width) -> str:
    bar = ""
    total_points = sum(round_result.values())
    errors = []
    symbol_counts = {}

    # Calculate initial symbol counts and track errors
    for player, points in round_result.items():
        proportion = points / total_points
        exact_length = proportion * graph_width
        initial_length = int(exact_length)
        error = exact_length - initial_length
        symbol_counts[player] = initial_length
        errors.append((player, error))

    # Sort players by rounding error, largest first
    errors.sort(key=lambda x: x[1], reverse=True)

    # Allocate extra symbols based on rounding error
    extra_symbols = graph_width - sum(symbol_counts.values())
    for i in range(extra_symbols):
        symbol_counts[errors[i][0]] += 1

    # Build the bar with corrected symbol counts
    for player, points in round_result.items():
        color, background_color, symbol = assigner.get_player_colors(player.name)
        symbols = symbol * symbol_counts[player]
        bar += colored(symbols, color, on_color=background_color)

    return bar
