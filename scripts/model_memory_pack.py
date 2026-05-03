#!/usr/bin/env python3
"""Pack model memory artifacts for the given tag via AutoGen tool registration."""
import subprocess
from autogen import register_function, ConversableAgent


def aurekai_model_memory_pack(tag: str = "latest") -> str:
    """Pack model memory artifacts for the given tag"""
    out = subprocess.run(
        ["akai", "pack", "--tag", tag, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


if __name__ == "__main__":
    print(aurekai_model_memory_pack(tag="latest"))
