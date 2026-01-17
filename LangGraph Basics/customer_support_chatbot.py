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
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY") 

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found! Please set it in your .env file.")

print("API key loaded successfully!")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    google_api_key=google_api_key
)

print("LLM initialized: gemini-2.0-flash-exp")



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

print("System prompt configured")



def customer_support_agent(state: MessagesState) -> dict:
    """
    The main agent node that processes customer messages
    and generates helpful responses with full conversation context.
    """
    messages = [system_prompt] + state["messages"]
    
    response = llm.invoke(messages)
    
    return {"messages": [response]}

print("Customer support agent node defined")



builder = StateGraph(MessagesState)

builder.add_node("agent", customer_support_agent)

builder.add_edge(START, "agent")
builder.add_edge("agent", END)

print("Graph structure defined")



memory = MemorySaver()

chatbot = builder.compile(checkpointer=memory)

print("Chatbot compiled with memory")
print("\n" + "="*70)
print("CUSTOMER SUPPORT CHATBOT READY (Powered by Gemini)!")
print("="*70 + "\n")



def send_message(user_input: str, session_id: str = "default_customer"):
    time.sleep(12)
    """
    Send a message to the chatbot and display the conversation.
    
    Args:
        user_input: The customer's message
        session_id: Unique ID for this customer's conversation thread
    """
    print(f"Customer: {user_input}")
    
    result = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": session_id}}
    )
    
    agent_response = result["messages"][-1].content
    print(f"Agent: {agent_response}\n")
    print("-" * 70 + "\n")
    
    return agent_response


def start_conversation(session_id: str = "default_customer"):
    """
    Start an interactive customer support conversation.
    Type 'exit' or 'quit' to end the session.
    """
    print("\n" + "="*70)
    print("CUSTOMER SUPPORT SESSION STARTED")
    print("="*70)
    print(f"Session ID: {session_id}")
    print("Type your message and press Enter.")
    print("Type 'exit' or 'quit' to end the session.\n")
    print("="*70 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print("\nAgent: Thank you for contacting support! Have a great day!")
            print("\nSession ended.\n")
            break
        
        if not user_input:
            continue
        
        result = chatbot.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": session_id}}
        )
        
        agent_message = result["messages"][-1]
        print(f"\n Agent: {agent_message.content}\n")
        print("-" * 70 + "\n")




if __name__ == "__main__":
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        CUSTOMER SUPPORT CHATBOT - INTERACTIVE MODE                ║
║                    (Gemini 2.5 Flash Edition)                      ║
║                                                                    ║
║  This chatbot demonstrates:                                        ║
║  Stateful conversation (remembers context)                     ║
║  MessagesState for conversation history                        ║
║  MemorySaver checkpointer for persistent memory               ║
║  Empathetic customer support behavior                          ║
║  Multi-turn conversations with context awareness               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    start_conversation("interactive_session")