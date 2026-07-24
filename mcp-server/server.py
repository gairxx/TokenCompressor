from mcp.server.fastmcp import FastMCP
import requests
import json

# Initialize the MCP Server
mcp = FastMCP("PromptCompressor_Networked")

# This MCP server now proxies the compression to the central site API.
# The text is NEVER saved by the site, but the total tokens saved 
# across all models and users is tallied globally.
SITE_API_URL = "http://127.0.0.1:5000/compress"

@mcp.tool()
def compress_prompt(text: str) -> str:
    """
    Compresses a large block of text or prompt into a token-optimized format 
    without losing the core semantic meaning. It uses a central API that 
    tracks global token savings without saving your text.
    
    Args:
        text: The original verbose text that needs token compression.
    """
    try:
        response = requests.post(SITE_API_URL, json={"text": text})
        response.raise_for_status()
        data = response.json()
        
        # We return the compressed text back to the LLM agent calling this tool
        return data.get("compressed_text", text)
        
    except requests.RequestException as e:
        return f"Error compressing prompt via Site API: {e}"

if __name__ == "__main__":
    # Start the standard stdio server for MCP
    mcp.run()
