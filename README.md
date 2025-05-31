# MCP for Python

The Model Context Protocol (MCP) is a powerful framework that enables developers to build AI applications with large language models (LLMs) by providing a standardized way to connect models with external data sources and tools. This crash course will guide you through the fundamentals of MCP, from understanding its core concepts to implementing servers and clients that leverage prompts, resources, and tools.

## Table of Contents

1. [Understanding MCP](./1-understanding-mcp/README.md)
2. [Simple Server Setup with Python's SDK](./2-simple-server-setup/README.md)
3. [Azure OpenAI Integration](./3-azure-openai-integration/README.md)

## Setting Up Your Development Environment

Let's start by setting up our environment. The MCP Python SDK provides everything we need to build both servers and clients.

```bash
# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

The MCP CLI tools provide helpful utilities for development and testing:

```bash
# Test a server with the MCP Inspector
mcp dev server.py

# Install a server in Claude Desktop
mcp install server.py

# Run a server directly
mcp run server.py
```

## Resources and Next Steps

Key resources for deepening your MCP knowledge:

- [Model Context Protocol documentation](https://modelcontextprotocol.io)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io)
- [Python SDK GitHub repository](https://github.com/modelcontextprotocol/python-sdk)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)
- [MCP Core Architecture](https://modelcontextprotocol.io/docs/concepts/architecture)
