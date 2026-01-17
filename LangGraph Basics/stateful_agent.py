from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Literal
import os
import time
import requests

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError(
        """
    GOOGLE_API_KEY not found!
    
    Get your FREE API key from:
    https://aistudio.google.com/app/apikey
    
    Then create a .env file with:
    GOOGLE_API_KEY=your_key_here
    """
    )

print("API key loaded")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", temperature=0, google_api_key=google_api_key
)

print("LLM initialized: Gemini 2.5 Flash Lite")

weather_cache = {}
WEATHER_CACHE_DURATION = 3600


@tool
def get_weather(city: str) -> str:
    """
    Get real-time weather for a city using Open-Meteo API (free, no API key).
    Uses 1-hour caching to reduce API calls.

    Args:
        city: City name (e.g., "Lagos", "London", "New York")

    Returns:
        Current weather with temperature, wind speed, and conditions
    """
    cache_key = city.lower().strip()
    current_time = time.time()

    if cache_key in weather_cache:
        cached_data, cached_time = weather_cache[cache_key]
        if current_time - cached_time < WEATHER_CACHE_DURATION:
            return cached_data

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url, timeout=5)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"City '{city}' not found. Please check the spelling."

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url, timeout=5)
        weather_data = weather_response.json()

        current = weather_data["current_weather"]
        temp = current["temperature"]
        windspeed = current["windspeed"]

        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Drizzle",
            55: "Heavy drizzle",
            61: "Light rain",
            63: "Rain",
            65: "Heavy rain",
            71: "Light snow",
            73: "Snow",
            75: "Heavy snow",
            95: "Thunderstorm",
        }
        condition = weather_codes.get(current["weathercode"], "Unknown")

        result = f"""Weather in {city.title()}:
 Temperature: {temp}°C
 Conditions: {condition}
 Wind Speed: {windspeed} km/h"""

        weather_cache[cache_key] = (result, current_time)
        return result

    except requests.exceptions.Timeout:
        return f"Weather service timeout. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather: Network issue"
    except Exception as e:
        return f"Error: {str(e)}"


print("Weather tool created (Open-Meteo API with caching)")

dictionary_cache = {}


@tool
def define_word(word: str) -> str:
    """
    Look up word definition using WordNet (offline, comprehensive).
    Uses permanent caching since definitions don't change.

    Args:
        word: The word to define (e.g., "ephemeral", "serendipity")

    Returns:
        Definition with examples and synonyms
    """
    cache_key = word.lower().strip()

    if cache_key in dictionary_cache:
        return dictionary_cache[cache_key]

    try:
        from nltk.corpus import wordnet

        synsets = wordnet.synsets(cache_key)

        if not synsets:
            result = f"No definition found for '{word}'. Try checking the spelling or use web search."
            dictionary_cache[cache_key] = result
            return result

        result = f"Definition of '{word}':\n\n"

        for i, synset in enumerate(synsets[:2], 1):
            pos = synset.pos()
            pos_map = {"n": "noun", "v": "verb", "a": "adjective", "r": "adverb"}
            pos_name = pos_map.get(pos, pos)

            result += f"{i}. [{pos_name}] {synset.definition()}\n"

            if synset.examples():
                result += f"   Example: {synset.examples()[0]}\n"

        synonyms = set()
        for syn in synsets[:3]:
            for lemma in syn.lemmas():
                if lemma.name().lower() != cache_key:
                    synonyms.add(lemma.name().replace("_", " "))

        if synonyms:
            result += f"\nSynonyms: {', '.join(list(synonyms)[:5])}"

        dictionary_cache[cache_key] = result
        return result

    except ImportError:
        return """WordNet not installed!

To enable dictionary:
1. pip install nltk
2. python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

Then restart the agent."""
    except Exception as e:
        return f"Error looking up word: {str(e)}"


print("Dictionary tool created (WordNet with caching)")


@tool
def web_search(query: str) -> str:
    """
    Search the web for information using DuckDuckGo.
    Use this tool when you need current information, news, or facts not in your knowledge.

    Args:
        query: The search query (e.g., "latest AI news", "Python tutorials", "who won the 2024 Olympics")

    Returns:
        Top search results from DuckDuckGo with titles, snippets, and links

    Examples:
        - "Search for latest AI news" → Use this tool with query="latest AI news"
        - "Find Python tutorials" → Use this tool with query="Python tutorials"

    Note: This searches the actual web in real-time for current information.
    """
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return f" No results found for: {query}"

        formatted_results = [f" Web Search Results for: '{query}'\n"]

        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            snippet = result.get("body", "No description")
            link = result.get("href", "No link")

            formatted_results.append(
                f"""
{i}.  {title}
   {snippet[:200]}{'...' if len(snippet) > 200 else ''}
    {link}
"""
            )

        return "\n".join(formatted_results)

    except ImportError:
        return """DuckDuckGo search not available!

To enable web search:
pip install duckduckgo-search

Then restart the agent."""

    except Exception as e:
        return f"Search error: {str(e)}\n\nPlease try rephrasing your query."


print("Web search tool created")

system_prompt = SystemMessage(
    content="""You are a helpful assistant with access to three tools:

1. **get_weather**: Use when users ask about weather, temperature, or forecasts
2. **define_word**: Use when users ask for word definitions or meanings
3. **web_search**: Use when users need current information, news, or web searches

DECISION RULES:
- Weather questions → get_weather tool
- Word definitions → define_word tool
- Current info/news/research → web_search tool
- General knowledge/greetings → Answer directly (no tool needed)

Be smart about tool selection. Only use tools when necessary."""
)

tools = [get_weather, define_word, web_search]

llm_with_tools = llm.bind_tools(tools)

print(f"LLM bound to {len(tools)} tools")


def assistant(state: MessagesState) -> dict:
    """Assistant node that decides whether to use tools or answer directly."""
    messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    """Decide whether to use tools or finish."""
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"
    return "__end__"


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant", should_continue, {"tools": "tools", "__end__": END}
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
agent = builder.compile(checkpointer=memory)

print("Multi-tool agent compiled with memory")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  Interactive Mode Started!")
    print("=" * 70)
    print("\nCommands:")
    print("  - Type your query and press Enter")
    print("  - Type 'exit' or 'quit' to stop\n")

    last_request_time = 0
    min_delay = 12

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\n Goodbye!\n")
            break

        if not user_input:
            continue

        time_since_last = time.time() - last_request_time
        if time_since_last < min_delay and last_request_time > 0:
            wait_time = min_delay - time_since_last
            print(f"\n⏳ Rate limit: waiting {wait_time:.1f}s before next request...\n")
            time.sleep(wait_time)

        last_request_time = time.time()

        try:
            result = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": "interactive"}},
            )

            last_message = result["messages"][-1]

            if hasattr(last_message, "content") and last_message.content:
                agent_response = last_message.content
                print(f"\nAgent: {agent_response}\n")
            elif hasattr(last_message, "tool_calls") and last_message.tool_calls:
                print(f"\nAgent: [Using tools to answer...]\n")
            else:
                print(f"\nAgent: [No response generated]\n")
                print(f"Debug - Message type: {type(last_message)}\n")

            print("-" * 70 + "\n")

        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print(f"\n Quota exceeded! You've used up your daily quota.")
                print(
                    f"Your quota will reset tomorrow. Check usage at: https://ai.dev/rate-limit\n"
                )
                break
            else:
                print(f"\nError: {str(e)}\n")
                print("-" * 70 + "\n")
