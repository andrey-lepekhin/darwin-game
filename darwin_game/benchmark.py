"""Profile tournament throughput. Requires native arm64 Python on Apple Silicon."""

import platform
import subprocess
import sys
from pathlib import Path

PROFILE_PATH = Path("tournament.profile")


def check_native_arm64() -> None:
    machine = platform.machine()
    print(machine, sys.version)
    if sys.platform == "darwin" and machine != "arm64":
        print(
            f"Expected arm64, got {machine}. Python is likely running under Rosetta.",
            file=sys.stderr,
        )
        sys.exit(1)


def run_profile() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "cProfile",
            "-o",
            str(PROFILE_PATH),
            "-m",
            "darwin_game.run_tournament",
            "--quiet",
        ],
        check=True,
    )


def print_profile_stats() -> None:
    import pstats

    stats = pstats.Stats(str(PROFILE_PATH))
    stats.sort_stats("time")
    stats.print_stats(30)


def main() -> None:
    check_native_arm64()
    run_profile()
    print_profile_stats()


if __name__ == "__main__":
    main()
