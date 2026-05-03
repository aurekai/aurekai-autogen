#!/usr/bin/env python3
"""Export a verifiable proof bundle of the current pipeline state via AutoGen tool registration."""
import subprocess
from autogen import register_function, ConversableAgent


def aurekai_proof_bundle_export(output_path: str = "/tmp/aurekai-proof-bundle.tar.gz") -> str:
    """Export a verifiable proof bundle of the current pipeline state"""
    out = subprocess.run(
        ["akai", "proof", "export", "--output", output_path],
        capture_output=True, text=True
    )
    return out.stdout + out.stderr


if __name__ == "__main__":
    print(aurekai_proof_bundle_export(output_path="/tmp/aurekai-proof-bundle.tar.gz"))
