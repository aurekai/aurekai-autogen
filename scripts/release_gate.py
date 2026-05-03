#!/usr/bin/env python3
"""Run the release gate check for the given version via AutoGen tool registration."""
import subprocess
from autogen import register_function, ConversableAgent


def aurekai_release_gate(version: str = "0.8.0-alpha.4") -> str:
    """Run the release gate check for the given version"""
    out = subprocess.run(
        ["akai", "release", "gate", "--version", version, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


if __name__ == "__main__":
    print(aurekai_release_gate(version="0.8.0-alpha.4"))
