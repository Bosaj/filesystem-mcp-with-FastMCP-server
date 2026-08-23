# MCP Filesystem Assistant

AI-powered filesystem manager built on the Model Context Protocol (MCP), with a FastMCP server, a Streamlit web UI, and OpenAI function-calling for natural-language file operations.

![Lint](https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Overview

This project demonstrates a full MCP client/server stack:

- A **FastMCP server** (`server/filesystem_mcp_server.py`) that exposes 8 filesystem tools over SSE transport, sandboxed to a `workspace/` directory with path-traversal protection.
- A **Streamlit host application** (`host/app.py`) with a chat tab (OpenAI GPT function-calling drives tool selection), a file browser tab, and a quick-actions tab for direct file operations without going through the LLM.
- An **MCP connector** (`host/mcp_connector.py`) that discovers tools from the server, converts their schemas to OpenAI's function-calling format, and executes tool calls over a fresh SSE client connection per call.

It was built as a learning project for understanding how MCP servers, MCP clients, and an LLM front-end fit together in practice.

## Features

- **8 filesystem tools**: `read_file`, `write_file`, `append_file`, `delete_file`, `list_directory`, `create_directory`, `move_file`, `get_file_info` — all implemented in `server/filesystem_mcp_server.py`.
- **Sandboxed workspace**: every tool call resolves its path against `WORKSPACE_DIR` and rejects absolute paths or any path that resolves outside the workspace (`validate_path()`).
- **Natural-language interface**: the Streamlit chat tab sends user messages to OpenAI with the MCP tools exposed as function-calling tools; when the model requests a tool call, the connector executes it against the live MCP server and feeds the result back for a final answer.
- **File browser tab**: lists workspace contents in a table, with buttons to view file content or inspect metadata (size, created/modified timestamps).
- **Quick actions tab**: create a file, create a directory, or delete a file directly through the UI, bypassing the LLM.
- **Connection status + tool discovery in the sidebar**, plus a manual "check connection" and "refresh files" control.

### Not implemented

The server module's docstring and startup banner mention a 9th tool (`health_check`) and a PDF resource — neither is actually present in the code. `requirements.txt` includes `pypdf2` but no PDF-handling code exists anywhere in the repository. This README describes only what is actually implemented (the 8 tools above); the extra banner text in `filesystem_mcp_server.py` is left as-is but should not be taken as a feature list.

## Tech Stack

| Layer | Technology |
|---|---|
| MCP server framework | [FastMCP](https://github.com/jlowin/fastmcp) |
| Transport | SSE (Server-Sent Events) |
| LLM | OpenAI (`gpt-4-turbo-preview` by default, via function calling) |
| Web UI | Streamlit |
| Data display | pandas |
| Config | python-dotenv |

## Architecture

```
┌──────────────────┐        ┌───────────────────┐        ┌────────────────────┐
│  Streamlit UI     │  SSE   │  FastMCP server    │  I/O   │  workspace/         │
│  host/app.py       │◄─────►│  server/filesystem_ │◄─────►│  sandboxed files    │
│  + mcp_connector.py│        │  mcp_server.py      │        │                    │
└─────────┬─────────┘        └───────────────────┘        └────────────────────┘
          │
          │ function-calling
          ▼
   ┌───────────────┐
   │  OpenAI API    │
   └───────────────┘
```

The Streamlit app and the MCP server are **separate processes** that must both be running — the UI talks to the server over HTTP/SSE, not via direct function calls.

## Getting Started

### Prerequisites

- Python 3.10+
- An OpenAI API key (only required for the chat tab; the file browser and quick actions tabs work without it once the MCP server is running)

### Installation

```bash
git clone https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server.git
cd filesystem-mcp-with-FastMCP-server

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your key:

```env
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=8000
OPENAI_API_KEY=your_api_key_here
```

### Run

**Terminal 1 — start the MCP server:**
```bash
python server/filesystem_mcp_server.py
```

**Terminal 2 — launch the Streamlit UI:**
```bash
streamlit run host/app.py
```

The UI opens at `http://localhost:8501`; the MCP server listens on `http://127.0.0.1:8000` (SSE endpoint at `/sse`).

## Testing / CI

There is no automated test suite in this repository. CI (`.github/workflows/ci.yml`) runs a lightweight, fast check on every push/PR:

- `python -m py_compile` over every Python module (catches syntax errors)
- `flake8 --select=E9,F63,F7,F82` (catches undefined names and other critical errors, without enforcing style)

Both checks were run locally before this workflow was added and pass cleanly.

## Project Structure

```
filesystem-mcp-with-FastMCP-server/
├── host/
│   ├── app.py               # Streamlit UI (3 tabs: chat, file browser, quick actions)
│   ├── mcp_connector.py     # MCP client + OpenAI function-calling glue
│   └── ui_components.py     # UI rendering helpers / custom CSS
├── server/
│   ├── filesystem_mcp_server.py  # FastMCP server, 8 filesystem tools
│   └── config.py             # Env-driven configuration
├── workspace/                # Sandboxed sample files used by the tools
├── docs/wiki-draft/          # Draft wiki pages (see below)
├── requirements.txt
├── .env.example
└── CHANGELOG.md
```

## Documentation

A draft GitHub Wiki lives in [`docs/wiki-draft/`](docs/wiki-draft/) (Home, Getting Started, Architecture, FAQ) — see that folder's note on how to publish it.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Security

No committed secrets were found in this repository's tracked files or git history. `.env` is correctly git-ignored and only `.env.example` (with a placeholder key) is tracked.

## License

[MIT](LICENSE)

## Contributors

- [chakorabdellatif](https://github.com/chakorabdellatif)
- [Bosaj](https://github.com/Bosaj)
- [yassinebenacha](https://github.com/yassinebenacha)
