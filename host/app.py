"""
Streamlit Host Application
Main entry point for the MCP Filesystem Assistant
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from host.mcp_connector import MCPConnector
from host.ui_components import UIComponents
from server.config import (
    MCP_SERVER_HOST,
    MCP_SERVER_PORT,
    OPENAI_API_KEY,
    WORKSPACE_DIR,
)


# Helper function to run async code
def run_async(coro):
    """Run async coroutine in event loop"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# Page configuration
st.set_page_config(
    page_title="MCP Filesystem Assistant",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize UI components
ui = UIComponents()

# Apply custom CSS
ui.render_custom_css()

# MCP Server URL
MCP_SERVER_URL = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}"

# Initialize session state
if "mcp_connector" not in st.session_state:
    if OPENAI_API_KEY:
        st.session_state.mcp_connector = MCPConnector(MCP_SERVER_URL, OPENAI_API_KEY)
    else:
        st.session_state.mcp_connector = None

if "server_connected" not in st.session_state:
    st.session_state.server_connected = False

if "tools_fetched" not in st.session_state:
    st.session_state.tools_fetched = False


# ==================== HEADER ====================
ui.render_header()


# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("⚙️ Server Status")

    # Check connection button
    if st.button("🔄 Check Connection", use_container_width=True) and st.session_state.mcp_connector:
        st.session_state.server_connected = st.session_state.mcp_connector.check_connection()
        if st.session_state.server_connected and not st.session_state.tools_fetched:
            with st.spinner("Fetching tools..."):
                tools = run_async(st.session_state.mcp_connector.fetch_tools())
                st.session_state.tools_fetched = tools is not None

    # Auto-check on first load
    if not st.session_state.server_connected and st.session_state.mcp_connector:
        with st.spinner("Checking server connection..."):
            print("Checking connection to MCP server...")
            st.session_state.server_connected = st.session_state.mcp_connector.check_connection()
            print(f"Connection check result: {st.session_state.server_connected}")

        if st.session_state.server_connected and not st.session_state.tools_fetched:
            with st.spinner("Connecting to MCP server..."):
                try:
                    print("Fetching tools from MCP server...")
                    tools = run_async(st.session_state.mcp_connector.fetch_tools())
                    st.session_state.tools_fetched = tools is not None
                    print(f"Tools fetched: {st.session_state.tools_fetched}")
                    if tools:
                        print(f"Number of tools: {len(tools)}")
                except Exception as e:
                    print(f"Error fetching tools: {e}")
                    import traceback

                    traceback.print_exc()
                    st.error(f"Error fetching tools: {e}")
                    st.session_state.server_connected = False

    # Display connection status
    ui.render_connection_status(st.session_state.server_connected, MCP_SERVER_URL)

    st.divider()

    # Workspace info
    st.header("📁 Workspace")
    files = ui.list_workspace_files(WORKSPACE_DIR)
    ui.render_workspace_info(WORKSPACE_DIR, len(files))

    if st.button("🔄 Refresh Files", use_container_width=True):
        st.rerun()

    st.divider()

    # Available tools
    if st.session_state.mcp_connector and st.session_state.mcp_connector.available_tools:
        st.header("🛠️ Available Tools")
        ui.render_tools_list(st.session_state.mcp_connector.available_tools)

    st.divider()

    # Clear conversation
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        if st.session_state.mcp_connector:
            st.session_state.mcp_connector.clear_history()
        st.rerun()


# ==================== MAIN CONTENT ====================

# Create tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📂 File Browser", "🎯 Quick Actions"])

# ==================== TAB 1: CHAT ASSISTANT ====================
with tab1:
    st.subheader("Chat with AI Assistant")

    if not st.session_state.server_connected:
        st.warning("⚠️ Please start the MCP server first!")
        st.code("python server/filesystem_mcp_server.py", language="bash")
    elif not OPENAI_API_KEY:
        st.error("❌ OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
    else:
        connector = st.session_state.mcp_connector

        # Display conversation history
        for msg in connector.conversation_history:
            if msg["role"] == "user":
                ui.render_chat_message("user", msg["content"])
            elif msg["role"] == "assistant" and msg.get("content"):
                ui.render_chat_message("assistant", msg["content"])

        # Input area
        st.divider()

        col1, col2 = st.columns([5, 1])

        with col1:
            user_input = st.text_input(
                "Message",
                placeholder="Ask me to read, create, or manage files...",
                label_visibility="collapsed",
                key="user_input",
            )

        with col2:
            send_button = st.button("Send 📤", use_container_width=True)

        # Example prompts
        example_clicked = ui.render_example_prompts()
        if example_clicked:
            user_input = example_clicked
            send_button = True

        # Process message
        if send_button and user_input:
            with st.spinner("🤔 Thinking..."):
                try:
                    response, tool_calls = connector.chat(user_input)

                    # Show tool calls if any
                    if tool_calls:
                        ui.render_tool_calls(tool_calls)

                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ==================== TAB 2: FILE BROWSER ====================
with tab2:
    st.subheader("Workspace File Browser")

    files = ui.list_workspace_files(WORKSPACE_DIR)

    if not files:
        st.info("📭 Workspace is empty")
    else:
        # Display files as a table
        df = pd.DataFrame(files)
        st.dataframe(
            df,
            column_config={
                "type": st.column_config.TextColumn("Type", width="small"),
                "name": st.column_config.TextColumn("Name", width="medium"),
                "size": st.column_config.TextColumn("Size", width="small"),
                "modified": st.column_config.TextColumn("Modified", width="medium"),
            },
            hide_index=True,
            use_container_width=True,
        )

        # File actions
        st.divider()
        file_list = [f["name"] for f in files if f["type"] == "📄"]

        if file_list:
            selected_file = st.selectbox("Select a file to view:", file_list)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("👁️ View Content", use_container_width=True) and selected_file:
                    file_path = WORKSPACE_DIR / selected_file
                    try:
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()
                        st.code(content, language=None)
                    except Exception as e:
                        st.error(f"Error reading file: {e}")

            with col2:
                if st.button("ℹ️ File Info", use_container_width=True) and selected_file:
                    file_path = WORKSPACE_DIR / selected_file
                    stat = file_path.stat()
                    st.json(
                        {
                            "Name": file_path.name,
                            "Size": f"{stat.st_size:,} bytes",
                            "Created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                            "Modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )


# ==================== TAB 3: QUICK ACTIONS ====================
with tab3:
    st.subheader("Quick File Operations")

    if not st.session_state.server_connected:
        st.warning("⚠️ Please start the MCP server first!")
    else:
        connector = st.session_state.mcp_connector

        # Create File
        with st.expander("📝 Create New File", expanded=True):
            new_filename = st.text_input("Filename:", placeholder="example.txt")
            new_content = st.text_area("Content:", placeholder="Enter file content here...")

            if st.button("Create File", key="create_file"):
                if new_filename and new_content:
                    with st.spinner("Creating file..."):
                        result = run_async(
                            connector.execute_tool(
                                "write_file",
                                {"path": new_filename, "content": new_content},
                            )
                        )
                        if "error" not in str(result):
                            st.success(f"✅ File created: {new_filename}")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result}")
                else:
                    st.warning("Please enter both filename and content")

        # Create Directory
        with st.expander("📁 Create New Directory"):
            new_dirname = st.text_input("Directory name:", placeholder="my_folder")

            if st.button("Create Directory", key="create_dir"):
                if new_dirname:
                    with st.spinner("Creating directory..."):
                        result = run_async(
                            connector.execute_tool(
                                "create_directory",
                                {"path": new_dirname, "parents": True},
                            )
                        )
                        if "error" not in str(result):
                            st.success(f"✅ Directory created: {new_dirname}")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result}")
                else:
                    st.warning("Please enter a directory name")

        # Delete File
        with st.expander("🗑️ Delete File"):
            files = ui.list_workspace_files(WORKSPACE_DIR)
            file_list = [f["name"] for f in files if f["type"] == "📄"]

            if file_list:
                file_to_delete = st.selectbox("Select file:", file_list, key="delete_select")

                if (
                    st.button("Delete File", key="delete_file", type="secondary")
                    and file_to_delete
                    and st.checkbox("I confirm deletion", key="confirm_delete")
                ):
                    with st.spinner("Deleting file..."):
                        result = run_async(connector.execute_tool("delete_file", {"path": file_to_delete}))
                        if "error" not in str(result):
                            st.success(f"✅ File deleted: {file_to_delete}")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result}")
            else:
                st.info("No files available to delete")


# ==================== FOOTER ====================
ui.render_footer()
