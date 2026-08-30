# Architecture

## Components

| Component | File | Responsibility |
|---|---|---|
| MCP server | `server/filesystem_mcp_server.py` | Exposes 8 filesystem tools via FastMCP over SSE; validates every path against the `workspace/` sandbox. |
| Server config | `server/config.py` | Loads `.env`, resolves `WORKSPACE_DIR`, exposes host/port and the OpenAI key. |
| MCP connector | `host/mcp_connector.py` | Connects to the server's SSE endpoint, lists available tools, converts tool schemas to OpenAI function-calling format, and executes tool calls (using a fresh client per call to avoid SSE re-entrancy issues). |
| Streamlit UI | `host/app.py` | Three tabs: Chat (LLM + tools), File Browser (direct listing), Quick Actions (direct tool calls, no LLM). |
| UI helpers | `host/ui_components.py` | Custom CSS, header/footer rendering, workspace file listing helpers. |

## Request Flow (Chat Tab)

1. User types a message in the Streamlit chat tab.
2. `MCPConnector.chat()` sends the conversation history plus the available tools (in OpenAI function-calling format) to the OpenAI Chat Completions API.
3. If the model responds with one or more tool calls, `execute_tool()` opens a short-lived MCP client connection and calls the corresponding tool on the FastMCP server.
4. The server validates the path against the workspace sandbox (`validate_path()`), performs the file operation, and returns a result string.
5. Tool results are appended to the conversation and sent back to OpenAI for a final natural-language response.

## Security Model

- `validate_path()` in `server/filesystem_mcp_server.py` rejects absolute paths and resolves every relative path against `WORKSPACE_DIR`, then checks the resolved path still starts with `WORKSPACE_DIR` before allowing any operation — this is the sole guard against path traversal.
- The server and UI are two separate local processes; there is no authentication between them (the SSE endpoint is unauthenticated), so this project is intended for local/learning use, not for exposing the MCP server on an untrusted network.

## Known Gaps

- The server module's docstring and startup banner reference a `health_check` tool and a PDF resource that are **not implemented** in the code — only the 8 tools listed above exist. `pypdf2` is listed in `requirements.txt` but unused.
