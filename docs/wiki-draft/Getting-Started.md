# Getting Started

## Prerequisites

- Python 3.10+
- An OpenAI API key (only needed for the Chat tab)

## Install

```bash
git clone https://github.com/chakorabdellatif/filesystem-mcp-with-FastMCP-server.git
cd filesystem-mcp-with-FastMCP-server

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Configure

Copy `.env.example` to `.env`:

```env
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=8000
OPENAI_API_KEY=your_api_key_here
```

## Run

Two processes are required, in two terminals.

**Terminal 1 — MCP server:**
```bash
python server/filesystem_mcp_server.py
```

**Terminal 2 — Streamlit UI:**
```bash
streamlit run host/app.py
```

Open `http://localhost:8501`. Use the sidebar "Check Connection" button if the app doesn't detect the server automatically.

## Try It

In the Chat tab, once connected:
- "List all files in the workspace"
- "Read notes.txt"
- "Create a file called hello.txt with 'Hello World!'"

Or use the Quick Actions tab to create/delete files without going through the LLM.

## Common Issues

- **"Please start the MCP server first!"** — Terminal 1 isn't running, or the port doesn't match `.env`.
- **OpenAI errors** — check `OPENAI_API_KEY` in `.env` and restart Streamlit (env vars are loaded at process start).
- **Port already in use** — change `MCP_SERVER_PORT` in `.env`, or stop the process holding port 8000.
