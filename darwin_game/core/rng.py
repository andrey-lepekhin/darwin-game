"""Deterministic RNG seeds for tournaments and games."""

from random import Random

GAME_INDEX_STRIDE = 1_000_000
BATCH_GAME_INDEX = 0  # shuffle + population adjustment within a round


def batch_seed(base_seed: int, round_index: int) -> int:
    """Seed for round-level batch RNG (pairing shuffle, population top-up)."""
    return base_seed + round_index * GAME_INDEX_STRIDE + BATCH_GAME_INDEX


def game_seed(base_seed: int, round_index: int, game_index: int) -> int:
    """Seed for a single game. Pairing games use game_index 1..N; 0 is reserved for batch ops."""
    return base_seed + round_index * GAME_INDEX_STRIDE + game_index


def local_rng(seed: int) -> Random:
    return Random(seed)
