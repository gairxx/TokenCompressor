# PromptCompressor MCP Server

This is a Model Context Protocol (MCP) server that provides AI agents with the ability to instantly compress long prompts, logs, and files to save context window tokens. 

It works safely via lexical abbreviation and stopword culling that preserves Byte-Pair Encoding (BPE) boundaries.

## 1. Installation

You will need Python installed on your machine.

First, install the official `mcp` SDK:
```bash
pip install mcp
```

## 2. Testing the Server
You can run the server directly to verify it works (it will wait for stdio communication):
```bash
python server.py
```

## 3. How to connect this to your AI Agents

Because this is a standard MCP server, any MCP-compatible agent can use it instantly.

### Adding to Claude Desktop
Open your Claude Desktop config file (usually located at `%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "prompt-compressor": {
      "command": "python",
      "args": [
        "C:\\Absolute\\Path\\To\\TokenCompressor\\mcp-server\\server.py"
      ]
    }
  }
}
```
*(Make sure to change the path to where you saved `server.py`)*

### Adding to Cursor IDE
1. Open Cursor Settings > Features > MCP
2. Add a new MCP server.
3. Type: `stdio`
4. Command: `python C:\Absolute\Path\To\TokenCompressor\mcp-server\server.py`

## 4. How Agents Will Use It
Once configured, the AI agent will automatically have access to the `compress_prompt` tool.
You can tell your agent:
> "Read this 10,000 line log file, compress it using the prompt compressor to save tokens, and give me a summary."

The agent will seamlessly send the text through this local Python process, saving you up to 30% of your token quota.
