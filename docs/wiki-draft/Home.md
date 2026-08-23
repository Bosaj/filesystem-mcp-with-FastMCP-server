# MCP Filesystem Assistant — Wiki

> **Draft note**: GitHub Wikis cannot be reviewed as part of a pull request, so this folder holds the drafted wiki content. If this PR is merged, please copy the contents of each page below into the repository's actual Wiki (Settings → Wiki, or the "Wiki" tab) manually.

Welcome to the wiki for **MCP Filesystem Assistant**, a demo project pairing a [FastMCP](https://github.com/jlowin/fastmcp) server with a Streamlit chat UI to let an LLM manage files in a sandboxed workspace.

## Pages

- [Getting Started](Getting-Started.md) — install, configure, and run the server + UI.
- [Architecture](Architecture.md) — how the Streamlit UI, MCP connector, MCP server, and OpenAI API fit together.
- [FAQ](FAQ.md) — common questions and troubleshooting.

## At a Glance

- **Server**: `server/filesystem_mcp_server.py` — 8 FastMCP tools, SSE transport, sandboxed to `workspace/`.
- **Client/UI**: `host/app.py` — Streamlit app with chat, file browser, and quick-actions tabs.
- **License**: MIT.
