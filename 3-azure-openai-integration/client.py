import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional
import os

# import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AzureOpenAI

# nest_asyncio.apply()

load_dotenv("../.env")


class MCPOpenAIClient:
    def __init__(self, deployment: str = "gpt-4o"):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AzureOpenAI(
            api_version="2024-12-01-preview",
            azure_endpoint="https://bacsysai.openai.azure.com/",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.deployment = deployment
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self, server_script_path: str = "server.py"):
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        tools_result = await self.session.list_tools()
        print("\nConnected to server with tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
       
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str) -> str:
       
        tools = await self.get_mcp_tools()
        response = self.openai_client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": query}],
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        messages = [
            {"role": "user", "content": query},
            assistant_message,
        ]

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                result = await self.session.call_tool(
                    tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments),
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.content[0].text,
                    }
                )

            final_response = self.openai_client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                tools=tools,
                tool_choice="none",
            )

            return final_response.choices[0].message.content

        return assistant_message.content

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPOpenAIClient()
    await client.connect_to_server("server.py")

    query = "I am planning for a Vacation, i need to know if our company has a policy regarding that ?"
    print(f"\nQuery: {query}")

    response = await client.process_query(query)
    print(f"\nResponse: {response}")

    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
