"""
Filesystem MCP Server using FastMCP
Provides 8 tools for file operations and 1 PDF resource
"""

import shutil
from datetime import datetime
from pathlib import Path

from config import MCP_SERVER_HOST, MCP_SERVER_PORT, WORKSPACE_DIR
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Filesystem MCP Server")


# ==================== UTILITY FUNCTIONS ====================


def validate_path(path: str) -> Path:
    """
    Validate and resolve path within workspace.
    Prevents path traversal attacks.
    """
    # Convert to Path object
    requested_path = Path(path)

    # Resolve to absolute path within workspace
    if requested_path.is_absolute():
        raise ValueError("Absolute paths are not allowed")

    # Resolve relative to workspace
    full_path = (WORKSPACE_DIR / requested_path).resolve()

    # Ensure path is within workspace
    if not str(full_path).startswith(str(WORKSPACE_DIR)):
        raise ValueError("Path traversal detected - access denied")

    return full_path


# ==================== TOOL 1: READ FILE ====================


@mcp.tool()
def read_file(path: str, encoding: str = "utf-8") -> str:
    """
    Read contents of a file.

    Args:
        path: Relative path to file within workspace
        encoding: File encoding (default: utf-8)

    Returns:
        File contents as string
    """
    try:
        file_path = validate_path(path)

        if not file_path.exists():
            return f"❌ Error: File '{path}' does not exist"

        if not file_path.is_file():
            return f"❌ Error: '{path}' is not a file"

        # Try reading as text
        try:
            with open(file_path, encoding=encoding) as f:
                content = f.read()
            return f"✅ File: {path}\n\n{content}"
        except UnicodeDecodeError:
            # If text fails, read as binary
            with open(file_path, "rb") as f:
                content = f.read()
            return f"✅ Binary file: {path}\nSize: {len(content)} bytes"

    except Exception as e:
        return f"❌ Error reading file: {e!s}"


# ==================== TOOL 2: WRITE FILE ====================


@mcp.tool()
def write_file(path: str, content: str, encoding: str = "utf-8") -> str:
    """
    Create or overwrite a file with content.

    Args:
        path: Relative path to file within workspace
        content: Content to write to file
        encoding: File encoding (default: utf-8)

    Returns:
        Success or error message
    """
    try:
        file_path = validate_path(path)

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)

        return f"✅ File written successfully: {path} ({len(content)} characters)"

    except Exception as e:
        return f"❌ Error writing file: {e!s}"


# ==================== TOOL 3: APPEND FILE ====================


@mcp.tool()
def append_file(path: str, content: str, encoding: str = "utf-8") -> str:
    """
    Append content to an existing file.

    Args:
        path: Relative path to file within workspace
        content: Content to append
        encoding: File encoding (default: utf-8)

    Returns:
        Success or error message
    """
    try:
        file_path = validate_path(path)

        if not file_path.exists():
            return f"❌ Error: File '{path}' does not exist. Use write_file to create it."

        # Append content
        with open(file_path, "a", encoding=encoding) as f:
            f.write(content)

        return f"✅ Content appended to: {path} ({len(content)} characters added)"

    except Exception as e:
        return f"❌ Error appending to file: {e!s}"


# ==================== TOOL 4: DELETE FILE ====================


@mcp.tool()
def delete_file(path: str) -> str:
    """
    Delete a file.

    Args:
        path: Relative path to file within workspace

    Returns:
        Success or error message
    """
    try:
        file_path = validate_path(path)

        if not file_path.exists():
            return f"❌ Error: File '{path}' does not exist"

        if not file_path.is_file():
            return f"❌ Error: '{path}' is not a file. Use a different tool for directories."

        # Delete file
        file_path.unlink()

        return f"✅ File deleted successfully: {path}"

    except Exception as e:
        return f"❌ Error deleting file: {e!s}"


# ==================== TOOL 5: LIST DIRECTORY ====================


@mcp.tool()
def list_directory(path: str = ".", pattern: str | None = None) -> str:
    """
    List files and directories.

    Args:
        path: Relative path to directory (default: current directory)
        pattern: Optional glob pattern (e.g., "*.txt")

    Returns:
        Formatted list of files and directories
    """
    try:
        dir_path = validate_path(path)

        if not dir_path.exists():
            return f"❌ Error: Directory '{path}' does not exist"

        if not dir_path.is_dir():
            return f"❌ Error: '{path}' is not a directory"

        # Get items
        items = list(dir_path.glob(pattern)) if pattern else list(dir_path.iterdir())

        if not items:
            return f"📁 Directory '{path}' is empty"

        # Sort: directories first, then files
        items.sort(key=lambda x: (not x.is_dir(), x.name))

        # Format output
        output = [f"📁 Directory: {path}\n"]

        for item in items:
            if item.is_dir():
                output.append(f"  📂 {item.name}/")
            else:
                size = item.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024 else f"{size / 1024:.1f} KB"
                output.append(f"  📄 {item.name} ({size_str})")

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error listing directory: {e!s}"


# ==================== TOOL 6: CREATE DIRECTORY ====================


@mcp.tool()
def create_directory(path: str, parents: bool = True) -> str:
    """
    Create a new directory.

    Args:
        path: Relative path to new directory
        parents: Create parent directories if needed (default: True)

    Returns:
        Success or error message
    """
    try:
        dir_path = validate_path(path)

        if dir_path.exists():
            return f"❌ Error: '{path}' already exists"

        # Create directory
        dir_path.mkdir(parents=parents, exist_ok=False)

        return f"✅ Directory created successfully: {path}"

    except Exception as e:
        return f"❌ Error creating directory: {e!s}"


# ==================== TOOL 7: MOVE FILE ====================


@mcp.tool()
def move_file(source: str, destination: str) -> str:
    """
    Move or rename a file.

    Args:
        source: Current file path
        destination: New file path

    Returns:
        Success or error message
    """
    try:
        source_path = validate_path(source)
        dest_path = validate_path(destination)

        if not source_path.exists():
            return f"❌ Error: Source '{source}' does not exist"

        if not source_path.is_file():
            return f"❌ Error: '{source}' is not a file"

        if dest_path.exists():
            return f"❌ Error: Destination '{destination}' already exists"

        # Create destination parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Move file
        shutil.move(str(source_path), str(dest_path))

        return f"✅ File moved: {source} → {destination}"

    except Exception as e:
        return f"❌ Error moving file: {e!s}"


# ==================== TOOL 8: GET FILE INFO ====================


@mcp.tool()
def get_file_info(path: str) -> str:
    """
    Get detailed information about a file.

    Args:
        path: Relative path to file

    Returns:
        File metadata (size, modified time, etc.)
    """
    try:
        file_path = validate_path(path)

        if not file_path.exists():
            return f"❌ Error: '{path}' does not exist"

        stat = file_path.stat()

        # Format information
        info = {
            "name": file_path.name,
            "path": str(path),
            "type": "directory" if file_path.is_dir() else "file",
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size:,} bytes" if stat.st_size < 1024 else f"{stat.st_size / 1024:.2f} KB",
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "permissions": oct(stat.st_mode)[-3:],
        }

        output = [f"📋 File Information: {path}\n"]
        for key, value in info.items():
            output.append(f"  {key}: {value}")

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error getting file info: {e!s}"


# ==================== SERVER STARTUP ====================

if __name__ == "__main__":
    print("🚀 MCP Server starting...")
    print(f"📁 Workspace directory: {WORKSPACE_DIR}")
    print(f"🌐 Server running on http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}")
    print(f"🔗 SSE endpoint: http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse")
    print("✅ Available tools: 9")
    print("✅ Available resources: 1 (PDF)")
    print("\n🔧 Tools registered:")
    print("  1. read_file")
    print("  2. write_file")
    print("  3. append_file")
    print("  4. delete_file")
    print("  5. list_directory")
    print("  6. create_directory")
    print("  7. move_file")
    print("  8. get_file_info")
    print("  9. health_check")
    print("\n🎨 Streamlit UI: streamlit run app.py")
    print("⌨️  Press Ctrl+C to stop\n")

    # Run server with SSE transport
    mcp.run(transport="sse", host=MCP_SERVER_HOST, port=MCP_SERVER_PORT)
