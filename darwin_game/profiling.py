# type: ignore
"""Deprecated: use `python -m darwin_game.benchmark` instead."""

import warnings

warnings.warn(
    "darwin_game.profiling is deprecated; use `poetry run python -m darwin_game.benchmark`",
    DeprecationWarning,
    stacklevel=1,
)

from darwin_game.benchmark import main

if __name__ == "__main__":
    main()
