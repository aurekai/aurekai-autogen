"""
aurekai_autogen.py — AutoGen multi-agent system for Aurekai capability families.
"""
from __future__ import annotations

import json
import subprocess
from typing import Any

import autogen


def _run_akai(args: list[str], timeout: int = 300) -> dict[str, Any]:
    result = subprocess.run(
        ["akai", *args, "--json"],
        capture_output=True, text=True, timeout=timeout,
    )
    try:
        return json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return {"raw": result.stdout, "error": result.stderr}


# ── Tool functions (registered with agents) ───────────────────────────────────

def akai_doctor(deep: bool = True) -> str:
    return json.dumps(_run_akai(["doctor", "--deep"] if deep else ["doctor"]))

def akai_transcribe(audio_path: str, language: str = "en") -> str:
    return json.dumps(_run_akai(["transcribe", "audio", "--input", audio_path, "--language", language], timeout=600))

def akai_brief(artifact_id: str) -> str:
    return json.dumps(_run_akai(["brief", "generate", "--artifact", artifact_id]))

def akai_proof_bundle(run_id: str = "") -> str:
    args = ["proof", "bundle"]
    if run_id:
        args += ["--run-id", run_id]
    return json.dumps(_run_akai(args))

def akai_fpq_compress(model_tag: str, bits: int = 8) -> str:
    return json.dumps(_run_akai(["fpq", "compress", "--model", model_tag, "--bits", str(bits)], timeout=600))

def akai_sae_audit(artifact_id: str = "") -> str:
    args = ["sae", "audit"]
    if artifact_id:
        args += ["--artifact", artifact_id]
    return json.dumps(_run_akai(args))

def akai_wire_report(capture_id: str) -> str:
    return json.dumps(_run_akai(["wire", "report", "--capture", capture_id]))

def akai_invoice(client_id: str, period: str = "current") -> str:
    return json.dumps(_run_akai(["pay", "invoice", "--client", client_id, "--period", period]))

def akai_release_gate(strict: bool = True) -> str:
    return json.dumps(_run_akai(["release", "gate", "--strict"] if strict else ["release", "gate"]))

def akai_vec_search(query: str, top_k: int = 10) -> str:
    return json.dumps(_run_akai(["vec", "search", "--query", query, "--top-k", str(top_k)]))


AKAI_TOOLS = [
    {"name": "akai_doctor", "description": "Run Akai deep diagnostics", "function": akai_doctor},
    {"name": "akai_transcribe", "description": "Transcribe audio file", "function": akai_transcribe},
    {"name": "akai_brief", "description": "Generate brief from artifact", "function": akai_brief},
    {"name": "akai_proof_bundle", "description": "Export proof bundle", "function": akai_proof_bundle},
    {"name": "akai_fpq_compress", "description": "FPQ compress a model", "function": akai_fpq_compress},
    {"name": "akai_sae_audit", "description": "SAE feature audit", "function": akai_sae_audit},
    {"name": "akai_wire_report", "description": "Generate wire report", "function": akai_wire_report},
    {"name": "akai_invoice", "description": "Generate client invoice", "function": akai_invoice},
    {"name": "akai_release_gate", "description": "Release gate check", "function": akai_release_gate},
    {"name": "akai_vec_search", "description": "Vec search over model memory", "function": akai_vec_search},
]


# ── LLM config ────────────────────────────────────────────────────────────────

LLM_CONFIG = {
    "config_list": [{"model": "gpt-4o", "api_key": "REPLACE_WITH_KEY"}],
    "temperature": 0,
    "functions": [{"name": t["name"], "description": t["description"],
                   "parameters": {"type": "object", "properties": {}, "required": []}}
                  for t in AKAI_TOOLS],
}


def _make_function_map() -> dict:
    return {t["name"]: t["function"] for t in AKAI_TOOLS}


# ── Specialist agents ─────────────────────────────────────────────────────────

def build_aurekai_group_chat() -> autogen.GroupChat:
    coordinator = autogen.AssistantAgent(
        name="AurekaiCoordinator",
        system_message=(
            "You coordinate Aurekai pipeline tasks across specialists. "
            "Delegate: RuntimeAgent for diagnostics, MediaAgent for audio, "
            "MemoryAgent for FPQ/SAE/vec, ProofAgent for proofs, CommerceAgent for billing, "
            "WireAgent for captures, ReleaseAgent for gates."
        ),
        llm_config=LLM_CONFIG,
    )

    runtime_agent = autogen.AssistantAgent(
        name="RuntimeAgent",
        system_message="You handle Akai runtime diagnostics and manifest verification.",
        llm_config=LLM_CONFIG,
        function_map={"akai_doctor": akai_doctor},
    )

    media_agent = autogen.AssistantAgent(
        name="MediaAgent",
        system_message="You handle audio transcription, transcript cleaning, and brief generation.",
        llm_config=LLM_CONFIG,
        function_map={"akai_transcribe": akai_transcribe, "akai_brief": akai_brief},
    )

    memory_agent = autogen.AssistantAgent(
        name="MemoryAgent",
        system_message="You handle FPQ compression, SAE audits, and vector search.",
        llm_config=LLM_CONFIG,
        function_map={"akai_fpq_compress": akai_fpq_compress,
                      "akai_sae_audit": akai_sae_audit,
                      "akai_vec_search": akai_vec_search},
    )

    proof_agent = autogen.AssistantAgent(
        name="ProofAgent",
        system_message="You handle proof bundle exports and lineage verification.",
        llm_config=LLM_CONFIG,
        function_map={"akai_proof_bundle": akai_proof_bundle},
    )

    commerce_agent = autogen.AssistantAgent(
        name="CommerceAgent",
        system_message="You handle metering events and invoice generation.",
        llm_config=LLM_CONFIG,
        function_map={"akai_invoice": akai_invoice},
    )

    wire_agent = autogen.AssistantAgent(
        name="WireAgent",
        system_message="You handle PCAP captures and wire report generation.",
        llm_config=LLM_CONFIG,
        function_map={"akai_wire_report": akai_wire_report},
    )

    release_agent = autogen.AssistantAgent(
        name="ReleaseAgent",
        system_message="You handle release gate checks and final approvals.",
        llm_config=LLM_CONFIG,
        function_map={"akai_release_gate": akai_release_gate},
    )

    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config=False,
        function_map=_make_function_map(),
    )

    group_chat = autogen.GroupChat(
        agents=[user_proxy, coordinator, runtime_agent, media_agent, memory_agent,
                proof_agent, commerce_agent, wire_agent, release_agent],
        messages=[],
        max_round=30,
    )

    return group_chat


def build_manager(group_chat: autogen.GroupChat) -> autogen.GroupChatManager:
    return autogen.GroupChatManager(groupchat=group_chat, llm_config=LLM_CONFIG)
