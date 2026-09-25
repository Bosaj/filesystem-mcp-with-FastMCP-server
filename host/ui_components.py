"""
UI Components - Reusable Streamlit Components with Clean Light Theme
"""

from datetime import datetime
from pathlib import Path

import streamlit as st


class UIComponents:
    """Reusable UI components for Streamlit application."""

    @staticmethod
    def render_custom_css():
        """Inject custom CSS for clean, simple light theme."""
        st.markdown(
            """
        <style>
            /* ===== CLEAN LIGHT THEME ===== */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            /* Main background - Simple white */
            html, body, [data-testid="stApp"] {
                background: #ffffff;
                color: #1a1a1a !important;
            }

            /* Sidebar - Light gray */
            [data-testid="stSidebar"] {
                background: #f8f9fa;
                border-right: 2px solid #e9ecef;
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
                color: #1a1a1a !important;
            }

            /* Main content area */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                background: #ffffff;
            }

            /* Headers */
            .main-header {
                font-size: 2.5rem;
                font-weight: 700;
                color: #1a1a1a;
                text-align: center;
                margin-bottom: 0.5rem;
                letter-spacing: -0.02em;
            }

            .sub-header {
                font-size: 1.1rem;
                color: #666666;
                text-align: center;
                margin-bottom: 2rem;
                font-weight: 400;
            }

            /* Chat messages - Simple boxes with clear colors */
            .chat-user {
                background: #e3f2fd;
                color: #1a1a1a;
                padding: 1rem 1.25rem;
                border-radius: 8px;
                margin: 0.75rem 0;
                border-left: 4px solid #2196f3;
            }

            .chat-assistant {
                background: #f1f8e9;
                color: #1a1a1a;
                padding: 1rem 1.25rem;
                border-radius: 8px;
                margin: 0.75rem 0;
                border-left: 4px solid #4caf50;
            }

            /* Tool calls */
            .tool-call {
                background: #fff9e6;
                color: #1a1a1a;
                padding: 0.75rem 1rem;
                border-radius: 6px;
                margin: 0.5rem 0;
                font-family: 'SF Mono', 'Monaco', monospace;
                font-size: 0.9rem;
                border-left: 3px solid #ffa726;
            }

            /* Buttons - Simple and clean */
            .stButton > button {
                border-radius: 6px;
                font-weight: 500;
                border: 2px solid #e0e0e0;
                background: #ffffff;
                color: #1a1a1a;
                transition: all 0.2s ease;
            }

            .stButton > button:hover {
                border-color: #2196f3;
                background: #f5f5f5;
            }

            /* Input fields - High contrast */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                background-color: #ffffff !important;
                color: #1a1a1a !important;
                border: 2px solid #d0d0d0 !important;
                border-radius: 6px !important;
                padding: 0.75rem !important;
            }

            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {
                border-color: #2196f3 !important;
                outline: none !important;
            }

            /* Tabs - Clean separation */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
                background: transparent;
                border-bottom: 2px solid #e0e0e0;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 6px 6px 0 0;
                background: #f5f5f5;
                border: 2px solid #e0e0e0;
                border-bottom: none;
                padding: 0.5rem 1.5rem;
                font-weight: 500;
                color: #666666;
            }

            .stTabs [aria-selected="true"] {
                background: #ffffff;
                color: #1a1a1a !important;
                border-color: #e0e0e0;
                border-bottom: 2px solid #ffffff;
                margin-bottom: -2px;
            }

            /* Expanders - Simple boxes */
            .streamlit-expanderHeader {
                background: #f8f9fa;
                border-radius: 6px;
                border: 2px solid #e0e0e0;
                font-weight: 500;
                color: #1a1a1a;
            }

            .streamlit-expanderHeader:hover {
                background: #f0f0f0;
            }

            /* Status indicators - Clear and visible */
            .stSuccess {
                background: #e8f5e9;
                border-left: 4px solid #4caf50;
                border-radius: 6px;
                color: #1b5e20;
                padding: 1rem;
            }

            .stError {
                background: #ffebee;
                border-left: 4px solid #f44336;
                border-radius: 6px;
                color: #b71c1c;
                padding: 1rem;
            }

            .stWarning {
                background: #fff3e0;
                border-left: 4px solid #ff9800;
                border-radius: 6px;
                color: #e65100;
                padding: 1rem;
            }

            .stInfo {
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                border-radius: 6px;
                color: #0d47a1;
                padding: 1rem;
            }

            /* Dataframes */
            .stDataFrame {
                border-radius: 6px;
                overflow: hidden;
                border: 2px solid #e0e0e0;
            }

            .stDataFrame [data-testid="stDataFrameResizable"] {
                background-color: #ffffff !important;
            }

            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #1a1a1a !important;
                font-weight: 600;
                font-size: 1.5rem !important;
            }

            [data-testid="stMetricLabel"] {
                color: #666666 !important;
                font-weight: 500;
            }

            /* Dividers */
            hr {
                margin: 1.5rem 0;
                border: none;
                height: 2px;
                background: #e0e0e0;
            }

            /* Code blocks */
            .stCodeBlock {
                border-radius: 6px;
                border: 2px solid #e0e0e0;
                background: #f8f9fa;
            }

            code {
                background: #f0f0f0 !important;
                color: #1a1a1a !important;
                border-radius: 4px;
                padding: 0.2rem 0.4rem;
                font-weight: 500;
            }

            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }

            ::-webkit-scrollbar-track {
                background: #f5f5f5;
            }

            ::-webkit-scrollbar-thumb {
                background: #bdbdbd;
                border-radius: 5px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #9e9e9e;
            }

            /* Selectbox */
            .stSelectbox > div > div {
                background-color: #ffffff !important;
                border: 2px solid #d0d0d0 !important;
                border-radius: 6px !important;
                color: #1a1a1a !important;
            }

            /* Better text contrast */
            p, span, div {
                color: #1a1a1a !important;
            }

            /* Sidebar text */
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] div {
                color: #1a1a1a !important;
            }

            /* Headers in sidebar */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #1a1a1a !important;
            }

            /* Make captions more visible */
            .caption, [data-testid="stCaptionContainer"] {
                color: #666666 !important;
                font-size: 0.9rem;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_header():
        """Render application header."""
        st.markdown(
            '<div class="main-header">🗂️ MCP Filesystem Assistant</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sub-header">AI-Powered File Management with Model Context Protocol</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_connection_status(is_connected: bool, server_url: str):
        """
        Render server connection status.

        Args:
            is_connected: Whether server is connected
            server_url: Server URL to display
        """
        if is_connected:
            st.success("✅ MCP Server Connected")
            st.info(f"📡 **Server:** `{server_url}`")
        else:
            st.error("❌ MCP Server Disconnected")
            st.warning("**Start the server:**\n```bash\npython server/filesystem_mcp_server.py\n```")

    @staticmethod
    def render_workspace_info(workspace_path: Path, file_count: int):
        """
        Render workspace information.

        Args:
            workspace_path: Path to workspace directory
            file_count: Number of files in workspace
        """
        st.info(f"**📁 Location:**\n`{workspace_path}`")
        st.metric("📊 Files/Folders", file_count)

    @staticmethod
    def render_tools_list(tools: list[dict]):
        """
        Render available tools list.

        Args:
            tools: List of tool metadata
        """
        st.info(f"✨ **{len(tools)} tools loaded**")
        with st.expander("🔍 View All Tools", expanded=False):
            for i, tool in enumerate(tools, 1):
                st.markdown(f"**{i}. {tool['name']}**")
                st.caption(f"📝 {tool.get('description', 'No description')}")
                if i < len(tools):
                    st.markdown("---")

    @staticmethod
    def render_chat_message(role: str, content: str):
        """
        Render a chat message.

        Args:
            role: Message role (user/assistant)
            content: Message content
        """
        if role == "user":
            st.markdown(
                f'<div class="chat-user">👤 <b>You</b><br><br>{content}</div>',
                unsafe_allow_html=True,
            )
        elif role == "assistant":
            st.markdown(
                f'<div class="chat-assistant">🤖 <b>Assistant</b><br><br>{content}</div>',
                unsafe_allow_html=True,
            )

    @staticmethod
    def render_tool_calls(tool_calls: list[dict]):
        """
        Render tool calls in an expander.

        Args:
            tool_calls: List of tool calls made
        """
        if tool_calls:
            with st.expander(f"🔧 Tools Used ({len(tool_calls)})", expanded=True):
                for i, tool in enumerate(tool_calls, 1):
                    args_str = ", ".join([f"{k}={v}" for k, v in tool["arguments"].items()])
                    st.markdown(
                        f'<div class="tool-call">🛠️ {i}. {tool["name"]}({args_str})</div>',
                        unsafe_allow_html=True,
                    )

    @staticmethod
    def render_example_prompts():
        """Render example prompt buttons."""
        st.markdown("### 💡 Try these examples:")
        col1, col2, col3 = st.columns(3)

        examples = {
            "📋 List files": "List all files in the workspace",
            "📝 Read notes": "Read the contents of notes.txt",
            "📄 Create file": "Create a file called hello.txt with 'Hello from MCP!'",
        }

        clicked = None
        with col1:
            if st.button("📋 List files", use_container_width=True, key="ex1"):
                clicked = examples["📋 List files"]
        with col2:
            if st.button("📝 Read notes", use_container_width=True, key="ex2"):
                clicked = examples["📝 Read notes"]
        with col3:
            if st.button("📄 Create file", use_container_width=True, key="ex3"):
                clicked = examples["📄 Create file"]

        return clicked

    @staticmethod
    def list_workspace_files(workspace_path: Path) -> list[dict]:
        """
        Get list of files in workspace.

        Args:
            workspace_path: Path to workspace directory

        Returns:
            List of file metadata dictionaries
        """
        try:
            files = []
            for item in workspace_path.iterdir():
                stat = item.stat()
                files.append(
                    {
                        "name": item.name,
                        "type": "📂" if item.is_dir() else "📄",
                        "size": f"{stat.st_size:,} bytes" if stat.st_size < 1024 else f"{stat.st_size / 1024:.1f} KB",
                        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    }
                )
            return sorted(files, key=lambda x: (x["type"] != "📂", x["name"]))
        except Exception:
            return []

    @staticmethod
    def render_footer():
        """Render application footer."""
        st.divider()
        st.markdown(
            """
        <div style="text-align: center; color: #666666; padding: 1.5rem; font-size: 0.9rem;">
            <p style="margin: 0.5rem 0;">
                Built with ❤️ using <b style="color: #1a1a1a;">FastMCP</b>,
                <b style="color: #1a1a1a;">OpenAI</b>, and
                <b style="color: #1a1a1a;">Streamlit</b>
            </p>
            <p style="margin: 0.5rem 0; font-size: 0.85rem;">
                🔒 All operations are securely sandboxed to the workspace directory
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
