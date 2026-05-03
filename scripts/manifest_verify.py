#!/usr/bin/env python3
"""Verify an Aurekai manifest against the deploy schema via AutoGen tool registration."""
import subprocess
from autogen import register_function, ConversableAgent


def aurekai_manifest_verify(manifest_path: str = "artifact.json") -> str:
    """Verify an Aurekai manifest against the deploy schema"""
    out = subprocess.run(
        ["akai", "verify", "--manifest", manifest_path, "--json"],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


if __name__ == "__main__":
    print(aurekai_manifest_verify(manifest_path="artifact.json"))
