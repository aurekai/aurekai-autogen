<p align="center">
  <img src="https://raw.githubusercontent.com/aurekai/aurekai/main/assets/aurekai-logo.svg" alt="Aurekai" width="520" />
</p>

# `aurekai-autogen` · v0.8.0-alpha.5

Official AutoGen integration for Aurekai — multi-agent group chat with 8 specialist agents across all capability families.

## Agents

| Agent | Family | Tools |
|---|---|---|
| `AurekaiCoordinator` | orchestration | delegates to all specialists |
| `RuntimeAgent` | runtime | `akai_doctor` |
| `MediaAgent` | intake/publish | `akai_transcribe`, `akai_brief` |
| `MemoryAgent` | memory | `akai_fpq_compress`, `akai_sae_audit`, `akai_vec_search` |
| `ProofAgent` | proof | `akai_proof_bundle` |
| `CommerceAgent` | commerce | `akai_invoice` |
| `WireAgent` | wire | `akai_wire_report` |
| `ReleaseAgent` | substrate | `akai_release_gate` |

## Quick Start

```python
from aurekai_autogen import build_aurekai_group_chat, build_manager
import autogen

group_chat = build_aurekai_group_chat()
manager = build_manager(group_chat)
user_proxy = next(a for a in group_chat.agents if a.name == "UserProxy")

user_proxy.initiate_chat(
    manager,
    message="Transcribe audio.wav, generate a brief, export proof bundle, then run release gate."
)
```


Aurekai integration surface for Autogen.

Status: active
Type: agent

## Core Template Set

- doctor-deep
- manifest-verify
- model-memory-pack
- sae-audit
- semantic-cache-bench
- proof-bundle-export
- release-gate

## Canonical References

- Platform: https://github.com/aurekai/aurekai
- Native runtime: https://github.com/aurekai/native-runtime
- Integration registry: https://github.com/aurekai/aurekai/blob/main/registry/integrations.json
- Ecosystem map: https://github.com/aurekai/aurekai/blob/main/ECOSYSTEM_NAMES.md
