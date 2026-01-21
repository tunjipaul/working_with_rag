import os
from typing import Literal, TypedDict, Annotated
from dotenv import load_dotenv
import operator

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found! Please set it in your .env file.")

print("API key loaded")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, api_key=groq_api_key)

print("LLM initialized: Llama 3.3 70B via Groq")


@tool
def extract_keywords(text: str) -> str:
    """
    Extract key topics and keywords from text.

    Args:
        text: The text to analyze
    """
    keywords = []
    important_terms = [
        "python",
        "langgraph",
        "multi-agent",
        "system",
        "agent",
        "tool",
        "research",
        "data",
        "analysis",
        "programming",
        "machine learning",
        "AI",
        "artificial intelligence",
        "RAG",
        "retrieval",
    ]

    text_lower = text.lower()
    for term in important_terms:
        if term in text_lower:
            keywords.append(term)

    if keywords:
        return f"Keywords extracted: {', '.join(keywords)}"
    return "No significant keywords found"


@tool
def search_knowledge_base(keywords: str) -> str:
    """
    Search knowledge base for information about keywords.

    Args:
        keywords: Keywords to search for
    """
    knowledge_db = {
        "python": "Python is a high-level programming language created by Guido van Rossum in 1991. Known for readability and versatility in web development, data science, and AI.",
        "langgraph": "LangGraph is a library for building stateful, multi-actor applications with LLMs. It provides state management, graph-based workflows, and agent orchestration.",
        "multi-agent": "Multi-agent systems consist of multiple specialized autonomous agents that work together. Benefits include specialization, modularity, scalability, and parallel processing.",
        "tool": "Tools allow agents to interact with external systems and perform actions beyond text generation. Essential for true agent autonomy.",
        "programming": "Programming is the process of writing instructions for computers to execute. Involves problem-solving, algorithm design, and code implementation.",
        "machine learning": "Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. Uses algorithms to identify patterns in data.",
        "AI": "Artificial Intelligence (AI) is the simulation of human intelligence in machines. Includes learning, reasoning, problem-solving, perception, and language understanding.",
        "RAG": "Retrieval-Augmented Generation (RAG) combines information retrieval with text generation. Allows LLMs to access external knowledge bases for more accurate, up-to-date responses.",
        "retrieval": "Information retrieval is the process of finding relevant information from large datasets. Key component in search engines, recommendation systems, and RAG applications.",
    }

    keywords_lower = keywords.lower()
    results = []

    for topic, info in knowledge_db.items():
        if topic in keywords_lower:
            results.append(f"**{topic.upper()}**: {info}")

    if results:
        return "\n\n".join(results)

    return "No detailed information found for these keywords."


@tool
def format_as_summary(content: str, style: str = "detailed") -> str:
    """
    Format content as a well-structured summary.

    Args:
        content: Content to format
        style: Format style (detailed, bullet, concise)
    """
    sections = [s.strip() for s in content.split("\n\n") if s.strip()]

    if style == "bullet":
        formatted = "\n".join([f"• {section}" for section in sections])
    elif style == "concise":
        formatted = "\n".join(sections)
    else:
        formatted = "\n\n".join(sections)

    return f"Formatted Summary:\n{formatted}"


print("Collaborative agent tools created")


class ContentPipelineState(TypedDict):
    """State for content pipeline agents."""

    messages: Annotated[list, operator.add]
    task: str
    keywords: str
    research_results: str
    formatted_output: str


analyzer_prompt = SystemMessage(
    content="""You are an analysis specialist.
Use extract_keywords tool to identify key topics from the task.
Be thorough in your analysis."""
)

analyzer_llm = llm.bind_tools([extract_keywords])


def analyzer_agent(state: ContentPipelineState) -> dict:
    """Analyzer agent with keyword extraction tool."""
    task = state["task"]
    messages = [
        analyzer_prompt,
        HumanMessage(content=f"Analyze this task and extract keywords: {task}"),
    ]

    response = analyzer_llm.invoke(messages)

    keywords_result = ""
    if response.tool_calls:
        print("\nAnalyzer: Using extract_keywords tool...")
        tool_call = response.tool_calls[0]
        keywords_result = extract_keywords.invoke(tool_call["args"])
        print(f"   {keywords_result}\n")
    else:
        keywords_result = response.content
        print(f"\nAnalyzer: {keywords_result[:100]}...\n")

    return {
        "messages": [AIMessage(content=f"Analyzer findings: {keywords_result}")],
        "keywords": keywords_result,
    }


researcher_prompt = SystemMessage(
    content="""You are a research specialist.
Use search_knowledge_base tool to find comprehensive information about the keywords provided.
The tool will search for ALL keywords and return detailed results."""
)

researcher_llm = llm.bind_tools([search_knowledge_base])


def researcher_agent(state: ContentPipelineState) -> dict:
    """Researcher agent with knowledge base tool."""
    keywords = state["keywords"]

    print("Researcher: Using search_knowledge_base tool...")
    research_result = search_knowledge_base.invoke({"keywords": keywords})
    print(f"   Found results in knowledge base\n")

    return {
        "messages": [AIMessage(content=f"Research results: {research_result}")],
        "research_results": research_result,
    }


formatter_prompt = SystemMessage(
    content="""You are a formatting specialist.
Use format_as_summary tool to create well-formatted output.
Make the summary clear and well-structured."""
)

formatter_llm = llm.bind_tools([format_as_summary])


def formatter_agent(state: ContentPipelineState) -> dict:
    """Formatter agent with summary formatting tool."""
    research = state["research_results"]

    print("Formatter: Using format_as_summary tool...")
    formatted_result = format_as_summary.invoke(
        {"content": research, "style": "detailed"}
    )
    print(f"   Formatted output created\n")

    return {
        "messages": [AIMessage(content=f"Final output: {formatted_result}")],
        "formatted_output": formatted_result,
    }


print("Collaborative agents created (with tools!)")

content_pipeline_builder = StateGraph(ContentPipelineState)

content_pipeline_builder.add_node("analyzer", analyzer_agent)
content_pipeline_builder.add_node("researcher", researcher_agent)
content_pipeline_builder.add_node("formatter", formatter_agent)

content_pipeline_builder.add_edge(START, "analyzer")
content_pipeline_builder.add_edge("analyzer", "researcher")
content_pipeline_builder.add_edge("researcher", "formatter")
content_pipeline_builder.add_edge("formatter", END)

content_pipeline = content_pipeline_builder.compile()

print("Content pipeline multi-agent system created!")

console = Console()


def run_content_pipeline(task: str):
    """Run the content pipeline on a task."""
    print("\n" + "=" * 80)
    print(f"Task: {task}")
    print("=" * 80)

    result = content_pipeline.invoke(
        {
            "task": task,
            "messages": [],
            "keywords": "",
            "research_results": "",
            "formatted_output": "",
        }
    )

    print("\n" + "=" * 80)
    print("FINAL FORMATTED OUTPUT:")
    print("=" * 80)
    console.print(Markdown(result["formatted_output"]))
    print("=" * 80)
    print("\nAGENT ACTIVITY:")
    print("- Analyzer: Used extract_keywords tool")
    print("- Researcher: Used search_knowledge_base tool")
    print("- Formatter: Used format_as_summary tool")
    print("=" * 80 + "\n")

    return result


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("COLLABORATIVE MULTI-AGENT CONTENT PIPELINE")
    print("=" * 80)
    print("\nThis system demonstrates the Collaborative (Handoff) pattern where:")
    print("- Each agent has specialized tools")
    print("- Agents pass work sequentially in a pipeline")
    print("- Each agent adds value before handing off\n")

    run_content_pipeline("Explain Python and multi-agent systems")

    run_content_pipeline("What is RAG and machine learning?")

    run_content_pipeline("Tell me about AI and programming")
