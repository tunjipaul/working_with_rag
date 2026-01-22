import os
import time
from typing import Literal
from dotenv import load_dotenv
import numpy as np

from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RateLimiter:
    """Rate limiter to handle API quota restrictions"""

    def __init__(self, calls_per_minute=5, buffer_seconds=2):
        self.calls_per_minute = calls_per_minute
        self.buffer_seconds = buffer_seconds
        self.call_times = []

    def wait_if_needed(self):
        """Wait if we're approaching rate limit"""
        current_time = time.time()

        self.call_times = [t for t in self.call_times if current_time - t < 60]

        if len(self.call_times) >= self.calls_per_minute:
            wait_time = 60 - (current_time - self.call_times[0]) + self.buffer_seconds
            if wait_time > 0:
                print(f"Rate limit approaching. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                self.call_times = []

        self.call_times.append(time.time())


rate_limiter = RateLimiter(calls_per_minute=4)

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found! Please set it in your .env file.")

print("API key loaded")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, api_key=groq_api_key)


print("LLM (Groq) initialized")

sample_documents = [
    Document(
        page_content="""
Python Functions: Complete Guide

Functions in Python are reusable blocks of code that perform specific tasks. 
They help organize code and make it more maintainable.

Basic Function Syntax:
def function_name(parameters):
    return result

Example:
def greet(name):
    return f"Hello, {name}!"

Parameters and Arguments:
- Parameters are variables in function definition
- Arguments are actual values passed when calling
- Default parameters: def greet(name="World")
- *args for variable positional arguments
- **kwargs for variable keyword arguments

Return Values:
Functions can return single values, multiple values (as tuple), or None.
Use 'return' statement to send data back to caller.

Best Practices:
1. Use descriptive function names
2. Keep functions focused on single task
3. Document with docstrings
4. Avoid side effects when possible
5. Test functions independently
""",
        metadata={"source": "python_functions.txt", "topic": "functions"},
    ),
    Document(
        page_content="""
Python Lists and List Comprehensions

Lists are ordered, mutable sequences in Python. They can contain mixed data types.

Creating Lists:
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

Common Operations:
- append(item): Add to end
- insert(index, item): Add at position
- remove(item): Remove first occurrence
- pop(index): Remove and return item
- sort(): Sort in place
- reverse(): Reverse in place

List Comprehensions:
Concise way to create lists based on existing iterables.

Syntax: [expression for item in iterable if condition]

Examples:
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
uppercase = [s.upper() for s in ["a", "b", "c"]]

Nested Comprehensions:
matrix = [[i*j for j in range(5)] for i in range(5)]

Performance:
List comprehensions are generally faster than equivalent for loops.
Use them for simple transformations, not complex logic.
""",
        metadata={"source": "python_lists.txt", "topic": "data_structures"},
    ),
    Document(
        page_content="""
Python Exception Handling

Exception handling allows programs to respond to errors gracefully.

Basic Try-Except:
try:
    risky_operation()
except ExceptionType:
    handle_error()

Multiple Exceptions:
try:
    operation()
except ValueError:
    handle_value_error()
except TypeError:
    handle_type_error()
except Exception as e:
    handle_generic_error(e)

Finally Block:
Always executes, regardless of exceptions.
try:
    operation()
except Exception:
    handle_error()
finally:
    cleanup()

Else Block:
Executes only if no exception occurred.
try:
    operation()
except Exception:
    handle_error()
else:
    success_case()

Raising Exceptions:
raise ValueError("Invalid input")
raise

Custom Exceptions:
class CustomError(Exception):
    pass

Best Practices:
1. Catch specific exceptions, not generic Exception
2. Don't use exceptions for flow control
3. Clean up resources in finally
4. Log exceptions appropriately
5. Don't swallow exceptions silently
""",
        metadata={"source": "python_exceptions.txt", "topic": "error_handling"},
    ),
    Document(
        page_content="""
Python Decorators Explained

Decorators are functions that modify the behavior of other functions.
They use the @decorator syntax and are powerful for cross-cutting concerns.

Basic Decorator:
def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

@my_decorator
def my_function():
    pass

Common Use Cases:
1. Logging: Track function calls
2. Timing: Measure execution time
3. Authentication: Check permissions
4. Caching: Store results
5. Validation: Check inputs

Timing Decorator Example:
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f}s")
        return result
    return wrapper

Decorator with Arguments:
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

Class-based Decorators:
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

Built-in Decorators:
- @property: Define getters/setters
- @staticmethod: Method without self
- @classmethod: Method with class reference
- @functools.wraps: Preserve function metadata
""",
        metadata={"source": "python_decorators.txt", "topic": "advanced"},
    ),
    Document(
        page_content="""
Python File I/O Operations

Reading and writing files is essential for data persistence.

Opening Files:
file = open('filename.txt', 'mode')

Modes:
- 'r': Read (default)
- 'w': Write (overwrites)
- 'a': Append
- 'r+': Read and write
- 'b': Binary mode

Best Practice - Context Manager:
with open('file.txt', 'r') as file:
    content = file.read()

Reading Methods:
- read(): Entire file as string
- readline(): Single line
- readlines(): List of lines
- Iteration: for line in file

Writing Methods:
with open('file.txt', 'w') as file:
    file.write('Hello World\\n')
    file.writelines(['Line 1\\n', 'Line 2\\n'])

Binary Files:
with open('image.png', 'rb') as file:
    data = file.read()

Working with JSON:
import json

data = {'name': 'John', 'age': 30}
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

with open('data.json', 'r') as f:
    data = json.load(f)

Working with CSV:
import csv

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age'])
    writer.writerow(['John', 30])

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

Error Handling:
try:
    with open('file.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")

Path Operations:
from pathlib import Path

path = Path('folder/file.txt')
if path.exists():
    content = path.read_text()
    path.write_text('New content')
""",
        metadata={"source": "python_file_io.txt", "topic": "io"},
    ),
]

print(f"Created {len(sample_documents)} sample documents")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

doc_splits = text_splitter.split_documents(sample_documents)
print(f"Created {len(doc_splits)} chunks")

chroma_path = "./chroma_db_python_docs"

vectorstore = Chroma(
    collection_name="python_docs",
    persist_directory=chroma_path,
    embedding_function=embeddings,
)

print("Adding documents to vector store...")
batch_size = 3

for i in range(0, len(doc_splits), batch_size):
    batch = doc_splits[i : i + batch_size]
    rate_limiter.wait_if_needed()
    vectorstore.add_documents(documents=batch)
    print(f"   Added batch {i//batch_size + 1}/{(len(doc_splits)-1)//batch_size + 1}")

print(f"Vector store created with {len(doc_splits)} chunks")

retrieval_cache = []


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def check_semantic_cache(query, threshold=0.92):
    """Check if a semantically similar query exists in cache"""
    if not retrieval_cache:
        return None

    query_embedding = embeddings.embed_query(query)

    for cached_embedding, cached_result, cached_query in retrieval_cache:
        similarity = cosine_similarity(query_embedding, cached_embedding)
        if similarity >= threshold:
            print(f"[Cache hit! Similarity: {similarity:.2f} with '{cached_query}']")
            return cached_result

    return None


@tool
def retrieve_python_docs(query: str) -> str:
    """
    Search Python programming documentation for relevant information.

    Use this tool when you need information about:
    - Python syntax and features
    - How to use specific Python functions or methods
    - Code examples and best practices
    - Python programming concepts

    Do NOT use this for:
    - General greetings or casual conversation
    - Simple math calculations
    - Questions about other programming languages
    - General knowledge not related to Python

    Args:
        query: The search query about Python programming

    Returns:
        Relevant documentation excerpts that can help answer the question
    """
    cached_result = check_semantic_cache(query)
    if cached_result:
        return cached_result

    retriever = vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": 3, "fetch_k": 6}
    )

    results = retriever.invoke(query)

    if not results:
        return "No relevant Python documentation found."

    formatted = "\n\n---\n\n".join(
        f"Document {i+1} (Topic: {doc.metadata.get('topic', 'unknown')}):\n{doc.page_content}"
        for i, doc in enumerate(results)
    )

    query_embedding = embeddings.embed_query(query)
    retrieval_cache.append((query_embedding, formatted, query))

    print(f"[Cached new query: '{query}']")

    return formatted


print("Retrieval tool created with semantic caching")

system_prompt = SystemMessage(
    content="""You are a helpful Python programming assistant with access to Python documentation.

RETRIEVAL DECISION RULES:

DO NOT retrieve for:
- Greetings: "Hello", "Hi", "How are you"
- Questions about your capabilities: "What can you help with?"
- Simple math: "What is 2+2?"
- General conversation: "Thank you", "Goodbye"
- Questions about other programming languages (unless comparing to Python)

DO retrieve for:
- Questions about Python syntax or features
- How to use Python functions, methods, or libraries
- Python code examples
- Python best practices
- Python programming concepts
- Error explanations in Python

When you retrieve documents, cite them clearly. If documents don't contain the answer, say so.
Keep responses concise but informative.
"""
)

tools = [retrieve_python_docs]
llm_with_tools = llm.bind_tools(tools)


def assistant(state: MessagesState) -> dict:
    """Assistant node with rate limiting"""
    messages = [system_prompt] + state["messages"]

    rate_limiter.wait_if_needed()

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    """Decide whether to call tools or finish"""
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

print("Agentic RAG system compiled")


def query_agent(user_input: str, thread_id: str = "default_session"):
    """Query the agent with rate limiting"""
    print(f"\n{'='*70}")
    print(f"User: {user_input}")
    print(f"{'='*70}\n")

    rate_limiter.wait_if_needed()

    result = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}},
    )

    used_retrieval = False
    final_answer = None

    for message in result["messages"]:
        if isinstance(message, AIMessage):
            if message.tool_calls:
                used_retrieval = True
                print(f"Agent: [Calling retrieval tool...]")
            if message.content and not message.tool_calls:
                final_answer = message.content

    if final_answer:
        print(f"Agent: {final_answer}")

    print(f"\nDecision: {'USED RETRIEVAL' if used_retrieval else 'ANSWERED DIRECTLY'}")
    print(f"{'='*70}\n")

    return final_answer


print("\n" + "=" * 70)
print("TESTING AGENTIC RAG SYSTEM")
print("=" * 70)

test_queries = [
    ("Hello! What can you help me with?", False),
    ("Thank you for your help!", False),
    ("What is 5 + 5?", False),
    ("Tell me about JavaScript", False),
    ("How are you today?", False),
    ("How do I create a function in Python?", True),
    ("What are list comprehensions?", True),
    ("Explain exception handling in Python", True),
    ("How do I read a file in Python?", True),
    ("What are Python decorators?", True),
]

results = []

print("\nRunning Test Cases...\n")

for i, (query, should_retrieve) in enumerate(test_queries, 1):
    print(f"\n{'='*70}")
    print(f"TEST {i}/10: {query}")
    print(f"Expected: {'RETRIEVE' if should_retrieve else 'DIRECT'}")
    print(f"{'='*70}")

    query_agent(query, thread_id=f"test_{i}")

    time.sleep(2)

print("\n" + "=" * 70)
print("ALL TESTS COMPLETED")
print("=" * 70)

print("\n" + "=" * 70)
print("INTERACTIVE MODE")
print("=" * 70)
print("You can now ask questions! Type 'quit' to exit.\n")

session_id = "interactive_session"

while True:
    try:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        query_agent(user_input, thread_id=session_id)

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}")
        print("Continuing...")
