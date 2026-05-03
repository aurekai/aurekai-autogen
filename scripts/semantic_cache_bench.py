#!/usr/bin/env python3
"""Benchmark the Aurekai semantic cache via AutoGen tool registration."""
import subprocess
from autogen import register_function, ConversableAgent


def aurekai_semantic_cache_bench(queries: int = 100) -> str:
    """Benchmark the Aurekai semantic cache"""
    out = subprocess.run(
        ["akai", "cache", "bench", "--queries", str(queries), "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


if __name__ == "__main__":
    print(aurekai_semantic_cache_bench(queries=100))
