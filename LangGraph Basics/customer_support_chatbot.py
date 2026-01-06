"""
CUSTOMER SUPPORT CHATBOT - Exercise Solution (Gemini Edition)
=============================================================
A stateful chatbot that remembers conversation context
to provide better customer support.

Requirements:
- pip install langgraph langchain langchain-google-genai python-dotenv
"""

from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI  # <--- CHANGED THIS
from dotenv import load_dotenv
import os

# =============================================================================
# STEP 1: SETUP & CONFIGURATION
# =============================================================================

# Load API key
load_dotenv()
# Gemini requires GOOGLE_API_KEY in your .env file
google_api_key = os.getenv("GOOGLE_API_KEY") 

if not google_api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found! Please set it in your .env file.")

print("✅ API key loaded successfully!")

# Initialize LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # <--- CHANGED MODEL (Free tier compatible)
    temperature=0.7,           # Friendly but consistent
    google_api_key=google_api_key
)

print("✅ LLM initialized: gemini-2.5-flash")

# =============================================================================
# STEP 2: CREATE SYSTEM PROMPT
# =============================================================================

system_prompt = SystemMessage(content="""You are a helpful and empathetic customer support representative.

YOUR ROLE:
- Assist customers with their product issues
- Be patient, friendly, and professional
- Remember details from earlier in the conversation
- Ask clarifying questions when needed
- Provide step-by-step solutions

GUIDELINES:
- Always acknowledge the customer's issue with empathy
- Reference previous information they shared (product name, purchase date, issue description)
- Keep responses concise but helpful
- If you don't know something, be honest and offer to escalate

RESPONSE STYLE:
- Start with empathy: "I understand..." or "I'm sorry to hear..."
- Be conversational, not robotic
- Use bullet points for multi-step instructions
- End with a helpful question or next step

Remember: You're here to SOLVE PROBLEMS and make customers happy!
""")

print("✅ System prompt configured")

# =============================================================================
# STEP 3: CREATE ASSISTANT NODE
# =============================================================================

def customer_support_agent(state: MessagesState) -> dict:
    """
    The main agent node that processes customer messages
    and generates helpful responses with full conversation context.
    """
    # Combine system prompt with conversation history
    messages = [system_prompt] + state["messages"]
    
    # Get response from LLM
    response = llm.invoke(messages)
    
    # Return as state update
    return {"messages": [response]}

print("✅ Customer support agent node defined")

# =============================================================================
# STEP 4: BUILD THE GRAPH
# =============================================================================

# Create StateGraph with MessagesState
builder = StateGraph(MessagesState)

# Add the agent node
builder.add_node("agent", customer_support_agent)

# Define simple flow: START → agent → END
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

print("✅ Graph structure defined")

# =============================================================================
# STEP 5: ADD MEMORY (CHECKPOINTER)
# =============================================================================

# Create memory checkpointer
memory = MemorySaver()

# Compile the graph WITH memory
chatbot = builder.compile(checkpointer=memory)

print("✅ Chatbot compiled with memory")
print("\n" + "="*70)
print("🤖 CUSTOMER SUPPORT CHATBOT READY (Powered by Gemini)!")
print("="*70 + "\n")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def send_message(user_input: str, session_id: str = "default_customer"):
    """
    Send a message to the chatbot and display the conversation.
    
    Args:
        user_input: The customer's message
        session_id: Unique ID for this customer's conversation thread
    """
    print(f"👤 Customer: {user_input}")
    
    # Invoke the chatbot
    result = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": session_id}}
    )
    
    # Extract and display agent's response
    agent_response = result["messages"][-1].content
    print(f"🤖 Agent: {agent_response}\n")
    print("-" * 70 + "\n")
    
    return agent_response


def start_conversation(session_id: str = "default_customer"):
    """
    Start an interactive customer support conversation.
    Type 'exit' or 'quit' to end the session.
    """
    print("\n" + "="*70)
    print("🎧 CUSTOMER SUPPORT SESSION STARTED")
    print("="*70)
    print(f"Session ID: {session_id}")
    print("Type your message and press Enter.")
    print("Type 'exit' or 'quit' to end the session.\n")
    print("="*70 + "\n")
    
    while True:
        user_input = input("👤 You: ").strip()
        
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print("\n🤖 Agent: Thank you for contacting support! Have a great day!")
            print("\n👋 Session ended.\n")
            break
        
        if not user_input:
            continue
        
        # Get response
        result = chatbot.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": session_id}}
        )
        
        # Display response
        agent_message = result["messages"][-1]
        print(f"\n🤖 Agent: {agent_message.content}\n")
        print("-" * 70 + "\n")


# =============================================================================
# TEST SCENARIOS
# =============================================================================

def test_scenario_1():
    """
    Test Scenario 1: Laptop Won't Turn On
    Tests if agent remembers product type and issue across messages.
    """
    print("\n" + "="*70)
    print("📋 TEST SCENARIO 1: Laptop Won't Turn On")
    print("="*70 + "\n")
    
    session = "test_laptop_issue"
    
    # Message 1: Customer states the problem
    send_message("I bought a laptop last week", session)
    
    # Message 2: Describes the issue
    send_message("It won't turn on", session)
    
    # Message 3: Asks for clarification
    send_message("I tried holding the power button but nothing happens", session)
    
    # Message 4: Agent should remember it's a laptop
    send_message("What else can I try?", session)


def test_scenario_2():
    """
    Test Scenario 2: Phone Screen Broken
    Tests multi-turn conversation with warranty question.
    """
    print("\n" + "="*70)
    print("📋 TEST SCENARIO 2: Phone Screen Broken")
    print("="*70 + "\n")
    
    session = "test_phone_screen"
    
    send_message("My phone screen cracked", session)
    send_message("I bought it 3 months ago", session)
    send_message("Is it covered under warranty?", session)
    send_message("How do I file a claim?", session)


def test_scenario_3():
    """
    Test Scenario 3: Multiple Issues with Same Product
    Tests if agent can track multiple issues for one product.
    """
    print("\n" + "="*70)
    print("📋 TEST SCENARIO 3: Multiple Product Issues")
    print("="*70 + "\n")
    
    session = "test_multiple_issues"
    
    send_message("I have a problem with my wireless headphones", session)
    send_message("The left earbud doesn't work", session)
    send_message("Also, the battery drains really fast", session)
    send_message("Which issue should we fix first?", session)


def test_memory_across_sessions():
    """
    Test that different customers have separate conversation memories.
    """
    print("\n" + "="*70)
    print("📋 TEST: Memory Separation Between Customers")
    print("="*70 + "\n")
    
    # Customer A
    print("👤 CUSTOMER A:")
    send_message("I have a laptop problem", "customer_a")
    
    # Customer B (different session)
    print("\n👤 CUSTOMER B:")
    send_message("My phone won't charge", "customer_b")
    
    # Back to Customer A - should remember laptop
    print("\n👤 CUSTOMER A (returning):")
    send_message("What should I try next?", "customer_a")
    
    # Back to Customer B - should remember phone
    print("\n👤 CUSTOMER B (returning):")
    send_message("I tried a different cable", "customer_b")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        🎧 CUSTOMER SUPPORT CHATBOT - EXERCISE SOLUTION 🎧         ║
║                    (Gemini 2.5 Flash Edition)                      ║
║                                                                    ║
║  This chatbot demonstrates:                                        ║
║  ✅ Stateful conversation (remembers context)                     ║
║  ✅ MessagesState for conversation history                        ║
║  ✅ MemorySaver checkpointer for persistent memory               ║
║  ✅ Empathetic customer support behavior                          ║
║  ✅ Multi-turn conversations with context awareness               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run automated tests
    print("\n🧪 Running automated test scenarios...\n")
    
    test_scenario_1()
    test_scenario_2()
    test_scenario_3()
    test_memory_across_sessions()
    
    # Interactive mode
    print("\n" + "="*70)
    print("Would you like to try the INTERACTIVE mode?")
    print("="*70)
    
    response = input("\nStart interactive session? (yes/no): ").strip().lower()
    
    if response in ["yes", "y"]:
        start_conversation("interactive_session")
    else:
        print("\n✅ All tests complete! You can call start_conversation() anytime.")