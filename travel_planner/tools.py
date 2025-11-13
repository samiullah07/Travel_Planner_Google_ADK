from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search
from dotenv import load_dotenv
import os

from google.adk.tools import AgentTool
load_dotenv()

LLM = "gemini-2.0-flash-001"


_search_agent  = Agent(
    model = LLM,
    name="google_search_grounding",
    description="Provides instant, Google-powered answers with actionable insights for travelers. Delivers grounded, concise, and practical recommendations so users quickly know what to do—no searching required.",
    instruction="""
    Use the google_search grounding tool to instantly answer user queries with clear, up-to-date information.
    - Your responses should be brief, direct, and focused on the most useful action for a tourist or traveler.
    - Give exactly what the user needs in as few words as possible—avoid lengthy explanations or extra details.
    - Never prompt users to research or verify information themselves; you are their expert resource.
    
    IMPORTANT:
    - Always format your answers as simple bullet points.
    - Put what matters most to the traveler first (e.g., opening times, ticket links, weather alerts, must-see tips).
    - If the query is about logistics (how to get somewhere, opening hours, visa requirements), give an immediate, actionable step.
    - Be practical: highlight the best route, ticket site, current entry rules, or what to do next.
    - Make sure each bullet is easily understood and something the user can act on right now.
""",
tools=[google_search]



)
google_search_grounding = AgentTool(agent=_search_agent)

##Places Agent to be implemented

from google.adk.tools import FunctionTool
from geopy.geocoders import Nominatim
import requests

def find_nearby_places_open(query: str, location: str, radius: int = 3000, limit: int = 5) -> str:
    """
    Finds nearby places for any text query using ONLY free OpenStreetMap APIs (no API key needed).
    
    Args:
        query (str): What you’re looking for (e.g., "restaurant", "hospital", "gym", "bar").
        location (str): The city or area to search in.
        radius (int): Search radius in meters (default: 3000).
        limit (int): Number of results to show (default: 5).
    
    Returns:
        str: List of matching place names and addresses.
    """

    try:
        # Step 1: Geocode the location to get coordinates
        geolocator = Nominatim(user_agent="open_place_finder")
        loc = geolocator.geocode(location)
        if not loc:
            return f"Could not find location '{location}'."

        lat, lon = loc.latitude, loc.longitude

        # Step 2: Query Overpass API for matching places
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["name"~"{query}", i](around:{radius},{lat},{lon});
          node["amenity"~"{query}", i](around:{radius},{lat},{lon});
          node["shop"~"{query}", i](around:{radius},{lat},{lon});
        );
        out body {limit};
        """

        response = requests.get(overpass_url, params={"data": overpass_query})
        if response.status_code != 200:
            return f"Overpass API error: {response.status_code}"

        data = response.json()
        elements = data.get("elements", [])
        if not elements:
            return f"No results found for '{query}' near {location}."

        # Step 3: Format results
        output = [f"Top results for '{query}' near {location}:"]
        for el in elements[:limit]:
            name = el.get("tags", {}).get("name", "Unnamed place")
            street = el.get("tags", {}).get("addr:street", "")
            city = el.get("tags", {}).get("addr:city", "")
            full_addr = ", ".join(filter(None, [street, city]))
            output.append(f"- {name} | {full_addr if full_addr else 'Address not available'}")

        return "\n".join(output)

    except Exception as e:
        return f"Error searching for '{query}' near '{location}': {str(e)}"


location_search_tool = FunctionTool(func=find_nearby_places_open)