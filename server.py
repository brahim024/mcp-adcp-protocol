"""
ADCP-compliant FastMCP server
Implements AdCP v2.3.0 protocols for TV advertising automation

Run with: uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
import requests
from datetime import date, datetime
from typing import Optional, List, Dict

# Create an MCP server
mcp = FastMCP("ADCP TV Ad Server")

BASE_URL = "http://localhost:8000"

# ==============================================
# ADCP Media Buy Protocol
# ==============================================

@mcp.tool(
    "get_products",
    description="🎯 ADCP: Discover media inventory using natural language. Example: 'Find premium video spots during sports programs next week under 50,000 MAD'"
)
def get_products(
    query: str,
    channel: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    max_budget: Optional[float] = None
) -> dict:
    """
    ADCP Task: get_products
    Natural language product discovery across TV inventory.
    
    Args:
        query (str): Natural language description (e.g., "Find prime time slots for sports audience")
        channel (str): Filter by channel code (e.g., "al_aoula")
        date_from (str): Start date YYYY-MM-DD (defaults to today)
        date_to (str): End date YYYY-MM-DD (defaults to 7 days from start)
        max_budget (float): Maximum price per spot in MAD
    
    Returns:
        ADCP-compliant product catalog with availability and pricing
    """
    url = f"{BASE_URL}/api/v1/adcp/products"
    
    payload = {
        "query": query,
        "channel": channel,
        "date_from": date_from or str(date.today()),
        "date_to": date_to,
        "filters": {
            "max_budget": max_budget
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Product discovery error: {str(e)}"
        }


@mcp.tool(
    "create_media_buy",
    description="📺 ADCP: Create a new TV advertising campaign by purchasing ad spots"
)
def create_media_buy(
    name: str,
    advertiser: str,
    package_ids: List[str],
    start_date: str,
    end_date: str,
    budget: float,
    currency: str = "MAD",
    objectives: Optional[List[str]] = None
) -> dict:
    """
    ADCP Task: create_media_buy
    Launch a TV advertising campaign.
    
    Args:
        name (str): Campaign name (e.g., "Summer Sale 2025")
        advertiser (str): Advertiser/brand name
        package_ids (list): List of ad break IDs to purchase
        start_date (str): Campaign start YYYY-MM-DD
        end_date (str): Campaign end YYYY-MM-DD
        budget (float): Total campaign budget in MAD
        currency (str): Currency code (default: MAD)
        objectives (list): Marketing objectives (reach, awareness, conversions)
    
    Returns:
        ADCP MediaBuy object with campaign ID and confirmation
    """
    url = f"{BASE_URL}/api/v1/adcp/media-buy"
    
    payload = {
        "name": name,
        "advertiser": advertiser,
        "packages": [{"package_id": pid} for pid in package_ids],
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "currency": currency,
        "objectives": objectives or ["reach", "awareness"],
        "kpis": {}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Media buy creation error: {str(e)}"
        }


@mcp.tool(
    "get_media_buy_delivery",
    description="📊 ADCP: Get real-time campaign performance and delivery metrics"
)
def get_media_buy_delivery(media_buy_id: str) -> dict:
    """
    ADCP Task: get_media_buy_delivery
    Monitor campaign performance in real-time.
    
    Args:
        media_buy_id (str): Campaign identifier from create_media_buy
    
    Returns:
        Real-time delivery metrics including spots delivered, budget spent, completion rate
    """
    url = f"{BASE_URL}/api/v1/adcp/media-buy/{media_buy_id}/delivery"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Delivery data error: {str(e)}"
        }


# ==============================================
# ADCP Signals Activation Protocol
# ==============================================

@mcp.tool(
    "discover_signals",
    description="🎯 ADCP: Discover audience and contextual signals using natural language. Example: 'Find sports enthusiasts aged 25-45 in Casablanca'"
)
def discover_signals(
    query: str,
    signal_types: Optional[List[str]] = None,
    min_scale: Optional[int] = None
) -> dict:
    """
    ADCP Task: discover_signals
    Natural language signal discovery for audience targeting.
    
    Args:
        query (str): Natural language signal description
        signal_types (list): Types to search (audience, contextual, geographic, temporal)
        min_scale (int): Minimum audience size
    
    Returns:
        Matching signals with demographics and activation options
    """
    url = f"{BASE_URL}/api/v1/adcp/signals/discover"
    
    payload = {
        "query": query,
        "signal_types": signal_types or ["audience", "contextual"],
        "providers": None,
        "filters": {
            "min_scale": min_scale
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Signal discovery error: {str(e)}"
        }


@mcp.tool(
    "activate_signal",
    description="🚀 ADCP: Activate audience signals on decisioning platforms"
)
def activate_signal(
    signal_id: str,
    platform_ids: List[str],
    config: Optional[Dict] = None
) -> dict:
    """
    ADCP Task: activate_signal
    Push signals to advertising platforms.
    
    Args:
        signal_id (str): Signal ID from discover_signals
        platform_ids (list): Target platform IDs
        config (dict): Platform-specific configuration
    
    Returns:
        Activation status and sync confirmation
    """
    url = f"{BASE_URL}/api/v1/adcp/signals/activate"
    
    payload = {
        "signal_id": signal_id,
        "platforms": [{"platform_id": pid} for pid in platform_ids],
        "config": config or {}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Signal activation error: {str(e)}"
        }


# ==============================================
# ADCP Creative Protocol
# ==============================================

@mcp.tool(
    "sync_creatives",
    description="🎬 ADCP: Upload and assign creative assets (videos, images) to campaigns"
)
def sync_creatives(
    media_buy_id: str,
    creative_urls: List[str],
    assignments: Optional[Dict] = None
) -> dict:
    """
    ADCP Task: sync_creatives
    Upload creative assets and assign to ad spots.
    
    Args:
        media_buy_id (str): Target campaign ID
        creative_urls (list): URLs of video/image creative files
        assignments (dict): Map creatives to specific placements
    
    Returns:
        Upload status and creative IDs
    """
    url = f"{BASE_URL}/api/v1/adcp/creatives/sync"
    
    payload = {
        "media_buy_id": media_buy_id,
        "creatives": [{"url": url} for url in creative_urls],
        "assignments": assignments or {}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Creative sync error: {str(e)}"
        }


# ==============================================
# ADCP Property Discovery
# ==============================================

@mcp.tool(
    "get_properties",
    description="📡 ADCP: Get TV channel/property catalog (AdCP v2.3.0)"
)
def get_properties(
    publisher_domain: Optional[str] = None,
    tags: Optional[str] = None
) -> dict:
    """
    Get publisher-owned TV properties following ADCP v2.3.0 spec.
    
    Args:
        publisher_domain (str): Filter by publisher (e.g., "snrt.ma")
        tags (str): Comma-separated tags (premium, sports, news, ctv)
    
    Returns:
        TV channel/property definitions with metadata
    """
    url = f"{BASE_URL}/api/v1/adcp/properties"
    params = {}
    if publisher_domain:
        params["publisher_domain"] = publisher_domain
    if tags:
        params["tags"] = tags
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "protocol": "adcp",
            "version": "2.3.0",
            "status": "failed",
            "message": f"Property discovery error: {str(e)}"
        }


# ==============================================
# Legacy Tools (Backward Compatibility)
# ==============================================

@mcp.tool(
    "get_channels",
    description="[LEGACY] Get channels list - prefer get_properties for ADCP compliance"
)
def get_channels() -> dict:
    """Legacy: Fetch channels list"""
    url = f"{BASE_URL}/api/v1/channels"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(
    "get_epg_shows",
    description="[LEGACY] Fetch EPG schedule - prefer get_products for ADCP compliance"
)
def get_epg_shows(channel: str, query_date: Optional[str] = None) -> dict:
    """Legacy: Fetch EPG program schedule"""
    if not query_date:
        query_date = str(date.today())
    
    url = f"{BASE_URL}/api/v1/programs"
    params = {"channel": channel, "date": query_date}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(
    "get_adbreaks",
    description="[LEGACY] Fetch ad breaks - prefer get_products for ADCP compliance"
)
def get_adbreaks(available: Optional[bool] = None) -> dict:
    """Legacy: Fetch ad breaks with availability filter"""
    url = f"{BASE_URL}/api/v1/adbreaks"
    params = {}
    if available is not None:
        params["available"] = available
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(
    "get_inventory",
    description="[LEGACY] Get inventory with audience data"
)
def get_inventory(
    channel: str,
    query_date: str,
    region: Optional[str] = None
) -> dict:
    """Legacy: Get detailed inventory with pricing and audience"""
    url = f"{BASE_URL}/api/v1/inventory"
    params = {
        "channel": channel,
        "date": query_date
    }
    if region:
        params["region"] = region
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(
    "book_ad",
    description="[LEGACY] Book an ad spot - prefer create_media_buy for ADCP compliance"
)
def book_ad(inventory_id: str) -> dict:
    """Legacy: Mark a single ad break as sold"""
    url = f"{BASE_URL}/api/v1/book_ad"
    
    try:
        response = requests.post(url, json={"inventory_id": inventory_id}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ==============================================
# Generic API Tool
# ==============================================

@mcp.tool(
    "get_api_data",
    description="Generic HTTP API caller for non-ADCP endpoints"
)
def get_api_data(
    url: str,
    method: str = "GET",
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    body: Optional[Dict] = None
) -> dict:
    """
    Generic API endpoint caller.
    Use ADCP-specific tools when possible for better standardization.
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


# ==============================================
# ADCP Resources
# ==============================================

@mcp.resource("adcp://protocol")
def get_protocol_info() -> str:
    """Get ADCP protocol information"""
    return """Ad Context Protocol (ADCP) v2.3.0
    
Task-first architecture for advertising automation:
- Media Buy Protocol: get_products, create_media_buy, get_media_buy_delivery
- Signals Activation: discover_signals, activate_signal
- Creative Protocol: sync_creatives
- Property Discovery: get_properties

Natural language queries supported across all discovery tasks."""


@mcp.resource("adcp://examples")
def get_usage_examples() -> str:
    """Get ADCP usage examples"""
    return """ADCP Usage Examples:

1. Product Discovery:
   get_products(query="Find prime time video spots during news programs next week under 30,000 MAD")

2. Campaign Creation:
   create_media_buy(
       name="Spring Sale 2025",
       advertiser="Marjane",
       package_ids=["ab_001", "ab_002"],
       start_date="2025-03-01",
       end_date="2025-03-31",
       budget=500000
   )

3. Audience Signals:
   discover_signals(query="Find sports enthusiasts interested in football, aged 18-35 in Morocco")

4. Creative Upload:
   sync_creatives(
       media_buy_id="mb_20250306",
       creative_urls=["https://cdn.example.com/ad1.mp4"]
   )
"""


# ==============================================
# ADCP Prompts
# ==============================================

@mcp.prompt()
def campaign_planner(
    objective: str,
    target_audience: str,
    budget: float,
    duration_days: int
) -> str:
    """Generate ADCP-ready campaign planning prompt"""
    return f"""Plan a TV advertising campaign using ADCP protocols:

    """

@mcp.prompt()
def inventory_analyzer(channel: str, date_from: str, date_to: str) -> str:
    """Generate inventory analysis prompt"""
    return f"""Analyze TV advertising inventory using ADCP:

📺 Channel: {channel}
📅 Date Range: {date_from} to {date_to}

Use get_products to:
1. Discover all available spots in this timeframe
2. Group by program category (news, sports, entertainment)
3. Analyze pricing patterns (prime time vs. off-peak)
4. Identify premium inventory opportunities
5. Calculate total available impressions

Provide:
- Inventory summary with availability rates
- Pricing recommendations
- Best time slots for different advertiser objectives
- Audience reach estimates"""