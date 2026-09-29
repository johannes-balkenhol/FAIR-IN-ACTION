# Local AI for sensitive data — keeping everything on the machine

*For open data, cloud AI (Claude, Claude Code, ChatGPT) is fine. For patient/identifying
data, no data may leave the controlled environment — so cloud AI is out. Use a LOCAL model.
The FAIR-in-action bundle (all markdown) works identically with a local model.*

## The rule

Claude Code, the Claude chat, ChatGPT, Gemini all **send your prompts and file contents to
their servers**. There is no local-only mode. So:

- **open data** → cloud AI is fine
- **pseudonymised / identifying / patient data** → **local model only.** Even pseudonymised
  genetic data is personal data under GDPR. Confirm with your DPO.

## Local, fully-offline options (nothing leaves the machine)

| Tool | What | Runs on |
|---|---|---|
| **Ollama** + a model (Llama 3, Qwen 2.5, Mistral) | open model, local | your workstation / HPC |
| **LM Studio** | desktop app, local models, chat UI | workstation |
| **continue.dev** + Ollama | a Claude-Code-like coding agent on a local model | editor + local |
| **Open WebUI** + Ollama | a self-hosted ChatGPT-like interface | server / HPC |

`continue.dev + Ollama` is the closest local alternative to Claude Code: an agent that
reads/edits your files, backed by a model on your own hardware — nothing sent out.

## Setup sketch (Ollama, the simplest)

```bash
# on the workstation/HPC (once)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:14b        # or llama3.1:8b (lighter) / qwen2.5:32b (stronger)
ollama run qwen2.5:14b         # a local chat, offline

# with continue.dev in VS Code: point it at the local Ollama endpoint
# → a local coding agent that follows STACK.md, on data that never leaves
```

## The honest trade-off

A local 8B–32B model is **weaker** than Claude — more hallucinations (exactly the kind you
must catch), slower. So the realistic group policy is **split by sensitivity**:

```
open projects      → Claude / Claude Code   (best quality)
sensitive projects → local Ollama+continue  (weaker, but compliant)
```

The bundle's standard applies to both — `STACK.md`, the SOPs, the schemas are markdown a
local model reads the same way. Only the model changes; the FAIR/GDPR method does not.

## What does NOT change with a local model

- the anti-hallucination rules (STACK.md §2b) matter MORE with a weaker model — the human
  keeps it honest, always
- the gates (G1/G2), the DPO sign-off, the EGA controlled-access deposition — unchanged
- the local model still must never be treated as authorising sensitive-data handling
