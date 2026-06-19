"""Profile or time tournament throughput. Requires native arm64 Python on Apple Silicon."""

import argparse
import platform
import subprocess
import sys
import time
from pathlib import Path

PROFILE_PATH = Path("tournament.profile")
DEFAULT_SEED = 12345


def check_native_arm64() -> None:
    machine = platform.machine()
    print(machine, sys.version)
    if sys.platform == "darwin" and machine != "arm64":
        print(
            f"Expected arm64, got {machine}. Python is likely running under Rosetta.",
            file=sys.stderr,
        )
        sys.exit(1)


def tournament_argv(*, seed: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "darwin_game.run_tournament",
        "--quiet",
        "--seed",
        str(seed),
    ]


def run_profile(*, seed: int) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "cProfile",
            "-o",
            str(PROFILE_PATH),
            *tournament_argv(seed=seed)[1:],
        ],
        check=True,
    )


def run_timed(*, seed: int) -> float:
    from darwin_game.run_tournament import create_tournament

    start = time.perf_counter()
    tournament = create_tournament(quiet=True, base_seed=seed)
    tournament.run_tournament()
    return time.perf_counter() - start


def print_profile_stats() -> None:
    import pstats

    stats = pstats.Stats(str(PROFILE_PATH))
    stats.sort_stats("time")
    stats.print_stats(30)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Darwin Game tournament throughput.")
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Base seed for reproducible tournament runs (default: %(default)s).",
    )
    parser.add_argument(
        "--time",
        action="store_true",
        help="Print wall-clock seconds only; skip cProfile.",
    )
    args = parser.parse_args()

    check_native_arm64()
    if args.time:
        elapsed = run_timed(seed=args.seed)
        print(f"elapsed_seconds={elapsed:.2f} seed={args.seed}")
        return

    run_profile(seed=args.seed)
    print_profile_stats()


if __name__ == "__main__":
    main()
