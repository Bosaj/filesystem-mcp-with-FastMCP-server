import asyncio
import contextlib
import json

import httpx
from fastmcp import Client
from openai import OpenAI


class MCPConnector:
    """
    MCP Client implementation for connecting to MCP servers via SSE.
    Handles tool discovery, execution, and LLM integration.
    """

    def __init__(self, server_url: str, openai_api_key: str):
        self.server_url = server_url.rstrip("/")
        self.sse_url = f"{self.server_url}/sse"
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.client: Client | None = None
        self.available_tools = []
        self.conversation_history = []
        self._connected = False

    async def connect(self) -> bool:
        try:
            print(f"Attempting to connect to: {self.sse_url}")
            self.client = Client(self.sse_url)
            await asyncio.wait_for(self.client.__aenter__(), timeout=10.0)
            print("Successfully connected to MCP server!")
            self._connected = True
            return True
        except asyncio.TimeoutError:
            print("Connection timeout after 10 seconds")
            self._connected = False
            return False
        except Exception as e:
            print(f"Error connecting to MCP server: {e}")
            import traceback

            traceback.print_exc()
            self._connected = False
            return False

    def check_connection(self) -> bool:
        try:
            print(f"Testing connection to: {self.sse_url}")
            with httpx.Client(timeout=5.0) as client, client.stream("GET", self.sse_url) as response:
                print(f"Response status: {response.status_code}")
                return response.status_code == 200
        except Exception as e:
            print(f"Connection error: {e}")
            import traceback

            traceback.print_exc()
            return False

    async def fetch_tools(self) -> list[dict] | None:
        try:
            if not self._connected or not self.client:
                print("Connecting to MCP server...")
                await self.connect()
            if not self.client:
                return None

            print("Listing tools from MCP server...")
            tools_response = await asyncio.wait_for(self.client.list_tools(), timeout=10.0)
            self.available_tools = []
            for tool in tools_response:
                input_schema = getattr(tool, "inputSchema", getattr(tool, "input_schema", {}))
                tool_dict = {
                    "name": tool.name,
                    "description": getattr(tool, "description", "") or "",
                    "parameters": {
                        "type": "object",
                        "properties": input_schema.get("properties", {}) if isinstance(input_schema, dict) else {},
                        "required": input_schema.get("required", []) if isinstance(input_schema, dict) else [],
                    },
                }
                self.available_tools.append(tool_dict)
                print(f"  - {tool.name}")
            return self.available_tools
        except Exception as e:
            print(f"Error fetching tools: {e}")
            import traceback

            traceback.print_exc()
            return None

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Execute a tool on the MCP server asynchronously using a fresh connection.
        Returns:
            Tool execution result as dict.
        """
        try:
            print(f"[DEBUG] Starting execute_tool for {tool_name}")
            print(f"[DEBUG] Calling tool '{tool_name}' with arguments: {arguments}")

            # Create a fresh client for this tool call to avoid SSE re-entrancy issues
            temp_client = None
            try:
                print("[DEBUG] Creating temporary client for tool execution...")
                temp_client = Client(self.sse_url)
                await asyncio.wait_for(temp_client.__aenter__(), timeout=5.0)

                print("[DEBUG] About to call tool with temporary client...")
                result = await asyncio.wait_for(temp_client.call_tool(tool_name, arguments), timeout=30.0)
                print(f"[DEBUG] Tool call completed: {result}")

                if hasattr(result, "content") and result.content:
                    print(
                        f"[DEBUG] Has content attribute: {result.content[0].text[:100] if len(str(result.content[0].text)) > 100 else result.content[0].text}"
                    )
                    return {"result": result.content[0].text}
                else:
                    print(f"[DEBUG] No content attribute, returning string: {str(result)[:100]}")
                    return {"result": str(result)}

            except asyncio.TimeoutError:
                print(f"[ERROR] Tool execution timed out after 30 seconds: {tool_name}")
                return {"error": "Tool execution timed out after 30 seconds"}
            finally:
                # Clean up temporary client
                if temp_client:
                    with contextlib.suppress(BaseException):
                        await temp_client.__aexit__(None, None, None)

        except Exception as e:
            print(f"[ERROR] Tool execution error: {e}")
            import traceback

            traceback.print_exc()
            return {"error": str(e)}

    def convert_tools_to_openai_format(self) -> list[dict]:
        openai_tools = []
        for tool in self.available_tools:
            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": {
                            "type": "object",
                            "properties": tool.get("parameters", {}).get("properties", {}),
                            "required": tool.get("parameters", {}).get("required", []),
                        },
                    },
                }
            )
        return openai_tools

    async def chat_async(self, user_message: str, model: str = "gpt-4-turbo-preview") -> tuple[str, list[dict]]:
        self.conversation_history.append({"role": "user", "content": user_message})

        if not self.available_tools:
            print("Fetching tools before chat...")
            await self.fetch_tools()

        openai_tools = self.convert_tools_to_openai_format()

        try:
            # Use asyncio.to_thread to call synchronous create() safely
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=model,
                messages=self.conversation_history,
                tools=openai_tools,
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message
            tool_calls_made = []

            if getattr(assistant_message, "tool_calls", None):
                print(f"AI wants to call {len(assistant_message.tool_calls)} tools")
                self.conversation_history.append(
                    {
                        "role": "assistant",
                        "content": getattr(assistant_message, "content", ""),
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments,
                                },
                            }
                            for tc in assistant_message.tool_calls
                        ],
                    }
                )

                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    print(f"Executing tool: {tool_name} with args: {tool_args}")
                    tool_calls_made.append({"name": tool_name, "arguments": tool_args})
                    result = await self.execute_tool(tool_name, tool_args)
                    self.conversation_history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        }
                    )

                # Get final AI response with tool results
                final_response = await asyncio.to_thread(
                    self.openai_client.chat.completions.create,
                    model=model,
                    messages=self.conversation_history,
                )
                final_message = final_response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": final_message})
                return final_message, tool_calls_made
            else:
                self.conversation_history.append({"role": "assistant", "content": assistant_message.content})
                return assistant_message.content, []

        except Exception as e:
            error_msg = f"Error communicating with AI: {e}"
            print(error_msg)
            return error_msg, []

    def chat(self, user_message: str, model: str = "gpt-4-turbo-preview") -> tuple[str, list[dict]]:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.chat_async(user_message, model))

    def clear_history(self):
        self.conversation_history = []

    def get_tool_count(self) -> int:
        return len(self.available_tools)

    def get_tool_names(self) -> list[str]:
        return [tool["name"] for tool in self.available_tools]

    async def disconnect(self):
        if self.client:
            await self.client.__aexit__(None, None, None)
        self._connected = False
        self.client = None
