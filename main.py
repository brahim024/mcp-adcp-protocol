"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
import requests
from datetime import date

# Create an MCP server
mcp = FastMCP("Demo")

@mcp.tool("get_epg_shows", description="Fetch today's EPG shows for a given channel")
def get_epg_shows(channel: str, query_date: str = None) -> dict:
    """
    Fetch EPG schedule from the backend API.
    Args:
        channel (str): Channel name (e.g., "al_aoula")
        query_date (str): Date in YYYY-MM-DD format, defaults to today
    """
    if not query_date:
        query_date = str(date.today())

    url = "http://localhost:8000/api/v1/programs"
    params = {"channel": channel, "date": query_date}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool("get_solded_adbreaks", description="Fetch Solded adbreaks for a given channel and date")
def get_solded_adbreaks(available:str) -> dict:
    

    url = "http://localhost:8000/api/v1/adbreaks"
    params = {"available": available}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
# Add an addition tool
@mcp.tool("get_channels", description="Fetch channels list from the backend API")
def get_channels() -> dict:
    """Add two numbers"""
    url = "http://localhost:8000/api/v1/channels"
    # params = {"channel": channel, "date": query_date}

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    

@mcp.tool("get_api_data", description="Fetch JSON data from a public or internal API")
def get_api_data(
    url: str,
    method: str = "GET",
    headers: dict = None,
    params: dict = None,
    body: dict = None
) -> dict:
    """
    Get data from an API endpoint.
    Args:
        url (str): API endpoint URL.
        method (str): HTTP method (GET, POST, etc).
        headers (dict): Optional HTTP headers.
        params (dict): Optional query parameters.
        body (dict): Optional body for POST requests.
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body,
            timeout=10
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"text": response.text}
    except Exception as e:
        return {"error": str(e)}


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."