# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
import requests
from typing import List, Dict, Any, Optional

mcp = FastMCP("MapNavigator")

YOUR_MAP_API_KEY = "..."
@mcp.tool()
def geocode(address: str, city: str = "") -> dict:
    """Convert address to geographic coordinates using Amap API."""
    api_key = YOUR_MAP_API_KEY
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": address,
        "city": city,
        "output": "json",
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        
        data = response.json()
        print(f"Geocode API status: {data.get('status')}") 
        return data
    except Exception as e:
        print(f"Error calling geocode API: {e}")
        return {"status": "0", "info": str(e)}
@mcp.tool()
def get_weather(city: str) -> dict:
    """Get weather information for a city using Amap API."""
    api_key = YOUR_MAP_API_KEY
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "city": city,
        "key": api_key,
        "output": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        
        data = response.json()
        print(f"Weather API status: {data.get('status')}")
        return data
    except Exception as e:
        print(f"Error calling weather API: {e}")
        return {"status": "0", "info": str(e)}

@mcp.tool()
def plan_driving_route(origin: str, destination: str, waypoints: str = "", strategy: str = "0", 
                      extensions: str = "base", avoid_road: str = "") -> dict:
    """Plan a driving route between two points
    
    Parameters:
        origin: Starting coordinates, format "longitude,latitude", e.g. "116.481028,39.989643"
        destination: Ending coordinates, format "longitude,latitude", e.g. "116.434446,39.90816"
        waypoints: Optional waypoints, format "longitude1,latitude1;longitude2,latitude2"
        strategy: Route planning strategy, default is "0" (speed priority)
        extensions: Return basic information ("base") or all information ("all")
        avoid_road: Specify roads to avoid
        
    Returns:
        Route planning information, including distance, time, and detailed route segments
    """
    api_key = YOUR_MAP_API_KEY
    url = "https://restapi.amap.com/v3/direction/driving"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
        "output": "json",
        "strategy": strategy,
        "extensions": extensions
    }
    
    if waypoints:
        params["waypoints"] = waypoints
        
    if avoid_road:
        params["avoidroad"] = avoid_road
    
    try:
        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        data = response.json()
        print(f"Driving route planning API status: {data.get('status')}")
        return data
    except Exception as e:
        print(f"Error calling driving route planning API: {e}")
        return {"status": "0", "info": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")