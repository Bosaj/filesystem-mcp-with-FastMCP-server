# FAQ

**Do I need an OpenAI API key to use this project?**
Only for the Chat tab. The File Browser and Quick Actions tabs work once the MCP server is running, without any LLM involved.

**Can the assistant read or write files outside `workspace/`?**
No — every tool call is validated by `validate_path()`, which rejects absolute paths and any relative path that resolves outside `WORKSPACE_DIR`.

**Is there a PDF summarization feature?**
No. The server code's docstring and startup banner mention a PDF resource and a 9th "health_check" tool, but neither is implemented — only the 8 filesystem tools exist. `pypdf2` is listed as a dependency but is not used anywhere in the code.

**Is there a test suite?**
No. CI runs a syntax compile check (`py_compile`) and a critical-errors-only `flake8` pass, not functional tests.

**Why do I need two terminals?**
The Streamlit UI and the FastMCP server are separate processes communicating over HTTP/SSE — the UI does not import or run the server directly.

**Can I change the workspace location or port?**
Yes — set `MCP_SERVER_PORT` in `.env`, or edit `WORKSPACE_DIR` / `MCP_SERVER_PORT` directly in `server/config.py`.
