"""
MULTI-TOOL AGENT - Exercise Solution
=====================================
An agent with three custom tools:
1. Weather tool (simulated data)
2. Dictionary tool (word definitions)
3. Web search tool (DuckDuckGo)

Installation:
pip install langgraph langchain langchain-google-genai python-dotenv duckduckgo-search
"""

from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Literal
import os

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
    model="gemini-1.5-flash", temperature=0, google_api_key=google_api_key
)

print("LLM initialized: Gemini 1.5 Flash")


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city.
    Use this tool when the user asks about weather conditions, temperature, or forecasts.

    Args:
        city: The name of the city to check weather for (e.g., "Lagos", "London", "New York")

    Returns:
        Current weather information including temperature, conditions, and humidity

    Examples:
        - "What's the weather in Lagos?" → Use this tool with city="Lagos"
        - "Is it raining in Paris?" → Use this tool with city="Paris"
    """
    weather_data = {
        "lagos": {
            "temp": "32°C",
            "condition": "Partly cloudy",
            "humidity": "75%",
            "wind": "15 km/h",
        },
        "london": {
            "temp": "12°C",
            "condition": "Rainy",
            "humidity": "85%",
            "wind": "20 km/h",
        },
        "new york": {
            "temp": "18°C",
            "condition": "Sunny",
            "humidity": "60%",
            "wind": "10 km/h",
        },
        "tokyo": {
            "temp": "22°C",
            "condition": "Clear",
            "humidity": "55%",
            "wind": "8 km/h",
        },
        "paris": {
            "temp": "15°C",
            "condition": "Cloudy",
            "humidity": "70%",
            "wind": "12 km/h",
        },
        "dubai": {
            "temp": "38°C",
            "condition": "Hot and sunny",
            "humidity": "45%",
            "wind": "5 km/h",
        },
    }

    city_lower = city.lower().strip()

    if city_lower in weather_data:
        data = weather_data[city_lower]
        return f"""Weather in {city.title()}:
 Temperature: {data['temp']}
 Conditions: {data['condition']}
 Humidity: {data['humidity']}
 Wind Speed: {data['wind']}"""
    else:
        return f"""Weather in {city.title()}:
 Temperature: 25°C
 Conditions: Partly cloudy
 Humidity: 65%
 Wind Speed: 12 km/h
"""


print("Weather tool created")


@tool
def define_word(word: str) -> str:
    """
    Look up the definition of a word.
    Use this tool when the user asks for the meaning, definition, or explanation of a word.

    Args:
        word: The word to define (e.g., "ephemeral", "serendipity", "ubiquitous")

    Returns:
        The definition of the word with part of speech and example usage

    Examples:
        - "What does ephemeral mean?" → Use this tool with word="ephemeral"
        - "Define serendipity" → Use this tool with word="serendipity"
    """
    dictionary = {
        "ephemeral": {
            "part_of_speech": "adjective",
            "definition": "Lasting for a very short time; fleeting or transitory",
            "example": "The ephemeral beauty of cherry blossoms lasts only a week.",
            "synonyms": "temporary, transient, fleeting",
        },
        "serendipity": {
            "part_of_speech": "noun",
            "definition": "The occurrence of events by chance in a happy or beneficial way",
            "example": "Finding that book was pure serendipity.",
            "synonyms": "luck, fortune, chance",
        },
        "ubiquitous": {
            "part_of_speech": "adjective",
            "definition": "Present, appearing, or found everywhere",
            "example": "Smartphones have become ubiquitous in modern society.",
            "synonyms": "omnipresent, pervasive, universal",
        },
        "pragmatic": {
            "part_of_speech": "adjective",
            "definition": "Dealing with things sensibly and realistically; practical",
            "example": "She took a pragmatic approach to solving the problem.",
            "synonyms": "practical, realistic, sensible",
        },
        "eloquent": {
            "part_of_speech": "adjective",
            "definition": "Fluent or persuasive in speaking or writing",
            "example": "The speaker gave an eloquent speech that moved the audience.",
            "synonyms": "articulate, expressive, fluent",
        },
        "resilient": {
            "part_of_speech": "adjective",
            "definition": "Able to withstand or recover quickly from difficult conditions",
            "example": "The resilient community rebuilt after the disaster.",
            "synonyms": "strong, tough, hardy",
        },
        "ambiguous": {
            "part_of_speech": "adjective",
            "definition": "Open to more than one interpretation; not having one obvious meaning",
            "example": "The politician's ambiguous statement confused voters.",
            "synonyms": "unclear, vague, equivocal",
        },
    }

    word_lower = word.lower().strip()

    if word_lower in dictionary:
        entry = dictionary[word_lower]
        return f""" Definition of "{word.title()}":

     Part of Speech: {entry['part_of_speech']}

     Definition: {entry['definition']}

     Example: {entry['example']}

     Synonyms: {entry['synonyms']}"""
    else:
        return f""" Word: "{word}"

     Definition not found in dictionary.

     Tip: Try searching the web for the definition, or check if the spelling is correct."""


print("Dictionary tool created")


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


def query_agent(user_input: str, thread_id: str = "default"):
    """Query the agent and display results."""
    print(f"\n{'='*70}")
    print(f"User: {user_input}")
    print(f"{'='*70}\n")

    result = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}},
    )

    used_tool = None

    for message in result["messages"]:
        if isinstance(message, AIMessage):
            if message.tool_calls:
                tool_name = message.tool_calls[0]["name"]
                used_tool = tool_name
                print(f"Agent: [Calling {tool_name} tool...]")
            elif message.content and not message.tool_calls:
                print(f"Agent: {message.content}")

    if used_tool:
        print(f"\nTool Used: {used_tool}")
    else:
        print(f"\nDecision: Answered directly (no tool needed)")

    print(f"{'='*70}\n")


def run_tests():
    """Run comprehensive tests of all tools."""

    print(
        """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        MULTI-TOOL AGENT - COMPREHENSIVE TESTING             ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """
    )

    print("\nTEST 1: WEATHER QUERIES")
    query_agent("What's the weather in Lagos?", "test1")
    query_agent("Is it raining in London?", "test1")

    print("\nTEST 2: DICTIONARY QUERIES")
    query_agent("Define the word 'ephemeral'", "test2")
    query_agent("What does serendipity mean?", "test2")

    print("\nTEST 3: WEB SEARCH QUERIES")
    query_agent("Search for latest AI news", "test3")
    query_agent("Find information about LangGraph", "test3")

    print("\nTEST 4: DIRECT ANSWERS (No Tool)")
    query_agent("What's the capital of France?", "test4")
    query_agent("Hello! How are you?", "test4")

    print("\nTEST 5: MEMORY TEST")
    query_agent("What's the weather in Tokyo?", "memory_test")
    query_agent("Now check Paris", "memory_test")
    query_agent("Which city was warmer?", "memory_test")

    print("\nTEST 6: CORRECT TOOL SELECTION")
    query_agent("What does ubiquitous mean and what's the weather in Dubai?", "test6")


if __name__ == "__main__":
    run_tests()

    print("\n" + "=" * 70)
    print("Would you like to try INTERACTIVE mode?")
    print("=" * 70)

    response = input("\nStart interactive chat? (yes/no): ").strip().lower()

    if response in ["yes", "y"]:
        print("\n🎮 Interactive Mode Started!")
        print("Commands:")
        print("  - Type your query and press Enter")
        print("  - Type 'exit' or 'quit' to stop\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\n Goodbye!\n")
                break

            if not user_input:
                continue

            result = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": "interactive"}},
            )

            agent_response = result["messages"][-1].content
            print(f"\nAgent: {agent_response}\n")
            print("-" * 70 + "\n")
    else:
        print("\n All tests complete!")


"""
QUICK START:
============

1. Install dependencies:
   pip install langgraph langchain langchain-google-genai python-dotenv duckduckgo-search

2. Get Google AI API key:
   https://aistudio.google.com/app/apikey

3. Create .env file:
   GOOGLE_API_KEY=your_key_here

4. Run the script:
   python multi_tool_agent.py


EXAMPLE QUERIES:
================

Weather:
- "What's the weather in Lagos?"
- "Is it raining in London?"
- "How hot is it in Dubai?"

Dictionary:
- "Define ephemeral"
- "What does serendipity mean?"
- "Explain the word pragmatic"

Web Search:
- "Search for latest AI news"
- "Find Python tutorials for beginners"
- "Look up who won the Nobel Prize 2024"

No Tool Needed:
- "Hello!"
- "What's 2+2?"
- "What's the capital of France?"


KEY FEATURES:
=============

Three Specialized Tools
   - Simulated weather data for major cities
   - Built-in dictionary with common words
   - Real-time web search via DuckDuckGo

 Intelligent Tool Selection
   - Agent chooses the right tool automatically
   - Can answer without tools when appropriate
   - Handles edge cases gracefully

 Conversation Memory
   - Remembers context within session
   - Can reference previous tool results
   - Multi-turn conversations work naturally

 Error Handling
   - Graceful fallbacks for unknown cities/words
   - Clear error messages for tool failures
   - Helps user rephrase failed queries


EXERCISE REQUIREMENTS CHECKLIST:
=================================

Weather tool (simulated)
Dictionary tool (with database)
Web search tool (DuckDuckGo integration)
@tool decorator for all tools
Tools bound to LLM
Conditional routing implemented
Handles cases where no tool is needed
Memory across conversations
Comprehensive testing


NEXT STEPS:
===========

1. Add more cities to weather database
2. Expand dictionary with more words
3. Add more tools (calculator, translator, etc.)
4. Improve error handling
5. Add logging for debugging
6. Create web UI with Gradio/Streamlit
"""
