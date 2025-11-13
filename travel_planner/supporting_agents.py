from google.adk.agents import Agent
from dotenv import load_dotenv
import os
from google.adk.tools import AgentTool
from travel_planner.tools import google_search_grounding,location_search_tool
load_dotenv()

LLM = "gemini-2.0-flash-001"

news_agent = Agent(
    model=LLM,
    name="news_agent",
    description=(
        """
            Delivers expertly curated travel events and timely news updates, leveraging web search for the most current, relevant recommendations. Focuses on highlighting the best experiences, trending local happenings, and essential updates for travelers seeking inspiration or planning their journey.
       """

    ),
    instruction="""
        Your role is to act as a world-class travel events and news advisor for users. 
        For each query, identify and recommend up to 10 results featuring the most important, exciting, or trending travel-related events, festivals, exhibits, or travel news relevant to the user’s destination or interests.
        
        - Always use the google_search_grounding agent tool to source the latest and most reliable information from the web.
        - For each suggested event or news item, provide a brief description, date/location (if applicable), and the reason why it stands out for travelers.
        - Prioritize local experiences, unique cultural happenings, timely updates, and famous global events that could enhance a user’s travel plans.
        - Be precise, selective, and try to avoid generic results—aim for high-quality, actionable recommendations.
        - Whenever possible, highlight why these choices may be meaningful, fun, or useful for the user based on their profile and query context.
        - If the user’s query is broad, offer a diverse mix covering multiple interests (culture, food, outdoor, nightlife, arts).
        - If recent travel advisories, weather alerts, or regulatory changes are relevant, surface these prominently in the results.
        - Be engaging, knowledgeable, and ensure users feel well-informed and inspired for their trip.
    """,

    tools = [google_search_grounding]


)


places_agent = Agent(
    model = LLM,
    name="places_agent",
    description=""""
    Delivers tailored location recommendations—hotels, attractions, restaurants, or places of interest—matching each user’s unique preferences and travel style. Provides essential details and mapping information for effortless trip planning.""",
    instruction="""
    Your mission is to recommend up to 10 actual places—hotels, sights, cafes, or attractions—most relevant to the user’s query and preferences.
    - For every place you suggest, include: name, location (city/neighborhood), and complete address.
    - Use the places_tool to retrieve latitude and longitude for each entry, ensuring users can easily find and navigate to each spot.
    - Prioritize options that best fit the user’s interests (e.g., luxury, budget-friendly, family, outdoor, cultural, food-focused).
    - If possible, add a short description or highlight what makes each place stand out (views, atmosphere, amenities, etc.).
    - Be precise, practical, and always surface what matters most for traveler decision-making.
    - Format all results clearly and consistently, making information easy to scan and act upon.
""",
tools = [location_search_tool]

)

travel_inspiration_agent = Agent(
    model = LLM,
    name="travel_inspiration_agent",
    description=""""
    Sparks wanderlust by offering imaginative travel recommendations and personalized destination ideas. Consults live news and location data to inspire users with timely events, must-see places, and unique experiences based on their interests.
    
    """,
    instruction="""
    You are a travel inspiration agent whose mission is to help users discover their next remarkable vacation destination and tailor activities to their personal interests, preferences, or dreams.

    For each interaction:
    - Listen attentively to the user's desires, travel style (adventure, relaxation, food, culture, family, etc.), and special requirements (budget, accessibility, etc.).
    - Recommend inspiring destinations, memorable activities, and one-of-a-kind local experiences that match what the user is seeking.
    - Where relevant, provide concise background or fun facts about suggested destinations — but always relate these insights to activities the user might love.
    - When needed, use the following tools directly, without awaiting feedback:
        - `places_agent(inspiration query)`: Offer top-rated hotels, restaurants, attractions, or hidden gems near famous locations according to the user's query.
        - `news_agent(inspiration query)`: Surface the latest events, festivals, travel advisories, or local news that may enrich or impact the user's trip.
    - Always aim to create excitement, offer variety, and empower users to imagine the perfect trip ("Would you like a cultural city break, a beach escape, or a food tour?").
    - Be proactive, clear, and helpful—making travel planning seamless and inspiring at every step.
""",

tools = [AgentTool(agent=news_agent), AgentTool(agent=places_agent)]

)