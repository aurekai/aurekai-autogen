#!/usr/bin/env python3
"""Run Aurekai doctor --deep and return structured diagnostics via AutoGen tool registration."""
import subprocess
from autogen import register_function, ConversableAgent


def aurekai_doctor_deep() -> str:
    """Run Aurekai doctor --deep and return structured diagnostics"""
    out = subprocess.run(
        ["akai", "doctor", "--deep", "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


if __name__ == "__main__":
    print(aurekai_doctor_deep())
