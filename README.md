<<<<<<< HEAD
# filesystem-mcp-with-FastMCP-server

![CI Pipeline](https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/actions/workflows/ci_qa_monitoring.yml/badge.svg)
[![GitHub Wiki](https://img.shields.io/badge/Documentation-GitHub%20Wiki-blue.svg)](https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki)
[![Quality Gate](https://img.shields.io/badge/Quality%20Gate-Passed-brightgreen.svg)](docs/MONITORING_AND_QA.md)

---

A beautiful AI-powered file manager built with **Model Context Protocol (MCP)**, featuring a modern web interface, OpenAI integration, and secure filesystem operations.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🎯 What is This?

An AI assistant that can read, write, and manage your files through natural language. Built on the Model Context Protocol (MCP), it demonstrates how to:

- 🤖 Connect AI models to real tools
- 🔒 Safely manage files in a sandboxed environment
- 🎨 Build beautiful interfaces with Streamlit
- 🛠️ Create production-ready MCP servers

Perfect for learning MCP or building your own AI-powered tools!

---

## ✨ Features

### 💬 Natural Language Interface
Ask the AI to manage files in plain English:
- "List all files in the workspace"
- "Read notes.txt and summarize it"
- "Create a backup folder and organize my files"
- "Show me details about data.json"

### 🎨 Beautiful Web Interface
- **Chat Tab** - Talk to the AI assistant
- **File Browser** - Visual workspace explorer
- **Quick Actions** - Direct file operations without AI

### 🛠️ 8 Powerful Tools
| Tool | What it does |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create or overwrite files |
| `append_file` | Add to existing files |
| `delete_file` | Remove files safely |
| `list_directory` | Browse folders |
| `create_directory` | Make new folders |
| `move_file` | Rename or relocate files |
| `get_file_info` | Show file details |

### 🔒 Security First
- All operations sandboxed to `workspace/` folder
- Path traversal protection
- Input validation on every operation

---

## 📁 Project Structure

```
filesystem-mcp-project/
├── host/                      # Streamlit web app
│   ├── app.py                 # Main interface
│   ├── mcp_connector.py       # Connects to MCP server
│   └── ui_components.py       # UI styling
│
├── server/                    # MCP server
│   ├── filesystem_mcp_server.py  # 8 filesystem tools
│   └── config.py              # Settings
│
├── workspace/                 # Your files live here
│   ├── notes.txt             
│   └── data.json             
│
├── requirements.txt           # Python packages
├── .env.example              # Config template
└── README.md                 # You are here!
```

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone or download the project
cd filesystem-mcp-project

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file:

```env
OPENAI_API_KEY=sk-your-key-here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### 3. Run

**Terminal 1 - Start MCP Server:**
```bash
python server/filesystem_mcp_server.py
```

You should see:
```
🚀 MCP Server starting...
📁 Workspace directory: /path/to/workspace
🌐 Server running on http://127.0.0.1:8000
✅ Available tools: 8
```

**Terminal 2 - Launch Web Interface:**
```bash
streamlit run host/app.py
```

Browser opens at `http://localhost:8501` 🎉

---

## 💡 Usage Examples

### Example 1: List Files
**You:** "What files are in the workspace?"

**AI:** *Uses `list_directory` tool*
```
📁 Directory: .

  📄 notes.txt (1.2 KB)
  📄 data.json (856 bytes)
```

### Example 2: Create File
**You:** "Create a file called hello.txt with 'Hello World!'"

**AI:** *Uses `write_file` tool*
```
✅ File written successfully: hello.txt (12 characters)
```

### Example 3: Organize Files
**You:** "Create a backup folder and move old files into it"

**AI:** *Uses `create_directory` and `move_file` tools*
```
✅ Directory created: backup
✅ File moved: old_data.txt → backup/old_data.txt
```

---

## 🏗️ How It Works

```
┌─────────────────┐
│   You (User)    │
│  Ask questions  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit App  │
│  localhost:8501 │  ← Beautiful web interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   OpenAI API    │
│     GPT-4       │  ← AI decides which tools to use
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Server    │
│  localhost:8000 │  ← Executes file operations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   workspace/    │
│   Your Files    │  ← Safe sandbox folder
└─────────────────┘
```

---

## 🔧 Configuration

### Basic Settings (`.env`)

```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults shown)
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=8000
```

### Advanced Settings (`server/config.py`)

```python
# Change workspace location
WORKSPACE_DIR = Path("my_custom_folder")

# Change server port
MCP_SERVER_PORT = 9000
```

---

## 🐛 Troubleshooting

### "Server Not Connected"
1. Check if MCP server is running (Terminal 1)
2. Click "Check Connection" button in sidebar
3. Restart both server and Streamlit

### "OpenAI API Key Error"
1. Make sure `.env` file exists
2. Check your API key is correct
3. Restart Streamlit after updating `.env`

### "Port Already in Use"
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or change port in .env
MCP_SERVER_PORT=8001
```

### "File Not Found"
Remember: All paths are relative to `workspace/`

```python
✅ Correct:   read_file("notes.txt")
❌ Wrong:     read_file("workspace/notes.txt")
❌ Wrong:     read_file("/absolute/path/file.txt")
```

---

## 🛠️ Development

### Add a New Tool

Edit `server/filesystem_mcp_server.py`:

```python
@mcp.tool()
def search_files(query: str) -> str:
    """
    Search for files containing text.
    
    Args:
        query: Text to search for
    
    Returns:
        List of matching files
    """
    # Your implementation here
    return "Found 3 files matching 'query'"
```

Restart the server - that's it! The tool is automatically available.

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Make your changes
4. Test everything works
5. Submit a pull request

---

## 🎓 Workshop Ready

This project is designed for learning and teaching:
- ✅ Clear, commented code
- ✅ Step-by-step setup
- ✅ Real-world example
- ✅ Production patterns
- ✅ Security best practices

Perfect for:
- Learning MCP architecture
- Building AI tools
- Teaching modern Python
- Prototyping ideas

---

**Happy building! 🎉**


## 📊 Monitoring, Controlling, Evaluation & QA

This project includes a standardized 4-Pillar Observability and QA framework:
- **Logs & Prometheus/Grafana Monitoring**: Configured in `monitoring/` with Prometheus scraper configs and Grafana dashboards.
- **Health Controlling & Evaluation**: Liveness/readiness controllers in `monitoring/health.py` and evaluation harness in `scripts/eval_harness.py`.
- **QA & Testing**: Automated Pytest/Vitest integration and CI workflows via `.github/workflows/ci_qa_monitoring.yml`.

For complete instructions, architecture details, and commands, see [docs/MONITORING_AND_QA.md](docs/MONITORING_AND_QA.md).

---

## 📚 Documentation & GitHub Wiki
- 📖 **Official Project Wiki**: [https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki](https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki)
- 🔍 **Architecture & Design**: [https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki/Architecture-and-Design](https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki/Architecture-and-Design)
- 🚀 **Getting Started Guide**: [https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki/Getting-Started](https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server/wiki/Getting-Started)
- 📊 **Monitoring & Observability**: [docs/MONITORING_AND_QA.md](docs/MONITORING_AND_QA.md)
=======
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
>>>>>>> portfolio-docs-cleanup
