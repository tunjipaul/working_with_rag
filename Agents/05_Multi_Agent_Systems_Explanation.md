# Multi-Agent Systems with LangGraph

## 📚 Overview

This notebook teaches how to build **multi-agent systems** using **LangGraph**, addressing the fundamental question: **when should you use multiple specialized agents instead of one complex agent?**

---

## 🎯 Learning Objectives

- Understand when to use multiple agents vs one complex agent
- Build supervised multi-agent systems (orchestrator pattern)
- Implement collaborative agents (handoff pattern)
- Manage state across multiple agents

---

## ❌ The Problem with Single Agents

A single agent handling everything becomes:

- **Complicated** - Too many tools and responsibilities
- **Slow** - Has to think about everything
- **Error-prone** - Jack-of-all-trades, master of none
- **Hard to debug** - Where did it go wrong?

### Example:

```
User: "Research Python and write a report"

SINGLE AGENT:
  One agent does everything
  ❌ Complex, slow

MULTI-AGENT:
  Researcher Agent → Finds information
  Writer Agent → Creates report
  Editor Agent → Polishes output
  ✅ Specialized, modular, debuggable
```

---

## ✅ Multi-Agent Benefits

1. **Specialization** - Each agent expert in one thing
2. **Modularity** - Easy to add/remove agents
3. **Easier debugging** - Know which agent failed
4. **Scalability** - Add agents as needs grow

### When to Use Each Approach

**Single Agent:**

- ✅ Simple, focused tasks
- ✅ Few tools (1-3)
- ✅ One clear skill needed

**Multiple Agents:**

- ✅ Complex workflows
- ✅ Multiple domains/skills
- ✅ Tasks needing collaboration
- ✅ Quality needs multiple perspectives

---

## 🏗️ Pattern 1: Supervised Multi-Agent (Orchestrator)

### How It Works

A **supervisor agent** routes work to **specialist workers**:

```
User Query
   ↓
SUPERVISOR (Project Manager)
   ↓
"This needs research" → RESEARCHER
                           ↓
                       Result back to SUPERVISOR
   ↓
"Now calculate" → CALCULATOR
                     ↓
                 Result back to SUPERVISOR
   ↓
"Done!" → Final Answer
```

### Key Features

- **Centralized control** - Supervisor acts as project manager
- **Dynamic routing** - Supervisor decides which specialist to call
- **Specialists loop back** - All specialists report results to supervisor
- **Best for:** Tasks requiring dynamic delegation (e.g., customer support)

### Implementation Components

#### Specialist Tools

```python
@tool
def research_tool(query: str) -> str:
    """Research information (simulated)."""
    # Returns research results

@tool
def calculator_tool(expression: str) -> str:
    """Perform calculations."""
    # Returns calculation results

@tool
def writer_tool(topic: str) -> str:
    """Write content about a topic."""
    # Returns written content
```

#### Specialist Agents

- **Researcher Agent** - Uses `research_tool` to find information
- **Calculator Agent** - Uses `calculator_tool` for math
- **Writer Agent** - Uses `writer_tool` to create content

#### Supervisor Agent

```python
class RouteDecision(BaseModel):
    """Decision on which agent to call next."""
    next_agent: Literal["researcher", "calculator", "writer", "FINISH"]
    reasoning: str

supervisor_llm = llm.with_structured_output(RouteDecision)
```

The supervisor:

- Analyzes the conversation state
- Decides which specialist to call next
- Routes to appropriate agent or finishes

#### Graph Structure

```
START → supervisor → [researcher|calculator|writer] → supervisor → END
```

All specialists loop back to the supervisor for centralized control.

---

## 🤝 Pattern 2: Collaborative Multi-Agent (Handoff)

### How It Works

Agents **pass work directly** to each other in a pipeline, each with **specialized tools**:

```
User Query
   ↓
ANALYZER (with keyword extraction tool) → Extracts key topics
   ↓
RESEARCHER (with knowledge base search tool) → Finds detailed info
   ↓
FORMATTER (with markdown formatting tool) → Creates final output
   ↓
END
```

Like an **assembly line** - each agent has tools and adds value before passing forward.

### Key Difference from Orchestrator

| Aspect       | Collaborative      | Orchestrator     |
| ------------ | ------------------ | ---------------- |
| **Workflow** | Fixed pipeline     | Dynamic routing  |
| **Control**  | Distributed        | Centralized      |
| **Best for** | Predictable stages | Varying tasks    |
| **Example**  | Data processing    | Customer support |

### Implementation Components

#### Specialized Tools

```python
@tool
def extract_keywords(text: str) -> str:
    """Extract key topics and keywords from text."""
    # Returns extracted keywords

@tool
def search_knowledge_base(keywords: str) -> str:
    """Search knowledge base for information about keywords."""
    # Returns research results

@tool
def format_as_summary(content: str, style: str = "detailed") -> str:
    """Format content as a well-structured summary."""
    # Returns formatted output
```

#### Collaborative Agents

**Agent 1: Analyzer**

- Tool: `extract_keywords`
- Identifies key topics from the task
- Passes keywords to next agent

**Agent 2: Researcher**

- Tool: `search_knowledge_base`
- Finds comprehensive information about keywords
- Passes research results to next agent

**Agent 3: Formatter**

- Tool: `format_as_summary`
- Creates well-formatted output
- Produces final result

#### State Management

```python
class CollaborativeState(TypedDict):
    """State for collaborative agents."""
    messages: Annotated[list, operator.add]
    task: str                    # Original task
    keywords: str                # From analyzer agent
    research_results: str        # From researcher agent
    formatted_output: str        # From formatter agent
```

#### Graph Structure

```
START → analyzer → researcher → formatter → END
```

Linear pipeline where each agent has TOOLS and takes ACTIONS!

---

## 🔑 What Makes TRUE Multi-Agent Systems

**All patterns share these requirements:**

1. ✅ **Tools bound to agents** - `llm.bind_tools([...])`
2. ✅ **Tool invocation logic** - Check `response.tool_calls` and invoke
3. ✅ **Autonomous decisions** - LLM decides when to use tools
4. ✅ **Real actions** - Agents interact with environment via tools

> **Without tools = Multi-step LLM chain, NOT true multi-agent!**

---

## 📊 Pattern Comparison Table

| Aspect          | Supervised (Orchestrator) | Collaborative (Handoff)  |
| --------------- | ------------------------- | ------------------------ |
| **Control**     | Centralized (supervisor)  | Distributed              |
| **Routing**     | Dynamic                   | Fixed pipeline           |
| **Best For**    | Varying task types        | Predictable workflows    |
| **Example**     | Customer support routing  | Data processing pipeline |
| **Complexity**  | Medium                    | Low                      |
| **Flexibility** | High                      | Low                      |
| **Debugging**   | Moderate                  | Easy                     |

---

## 💡 Design Principles

1. **Specialization over Generalization** - Narrow, focused agents perform better
2. **Explicit State Management** - Use TypedDict for clear state contracts
3. **Direct Tool Calls When Needed** - For reliability, call tools directly from state when appropriate
4. **Simple Tools** - Start with basic tools, add complexity only when needed

---

## 🎯 Key Takeaways

- **Start simple** - One agent first, split as complexity grows
- **Clear responsibilities** - Each agent has one specialized job
- **Choose the right pattern** - Match pattern to task structure
- **Tools are essential** - No tools means no true agency
- **Test individually** - Verify each agent works before integrating
- **Monitor carefully** - Multi-agent systems add complexity

---

## 🚀 Practice Exercise

### Challenge: Build a Content Creation Pipeline

**Objective:** Create a collaborative multi-agent system that transforms raw ideas into polished blog posts.

#### Requirements

Build a **3-agent pipeline** using the collaborative (handoff) pattern:

1. **Brainstormer Agent**

   - Tool: `generate_ideas(topic: str) -> str`
   - Generates 3-5 key points about the topic
   - Returns bullet points of ideas

2. **Writer Agent**

   - Tool: `draft_content(ideas: str) -> str`
   - Takes ideas and writes a draft blog post
   - Returns structured content with intro, body, conclusion

3. **Editor Agent**
   - Tool: `improve_writing(draft: str) -> str`
   - Polishes the draft for clarity and flow
   - Returns final polished version

#### Implementation Steps

1. **Define your tools** - Create the 3 tools above (simulated output is fine)
2. **Create custom state** - What fields do you need to pass between agents?
3. **Build the 3 agents** - Each with `llm.bind_tools([...])` and tool invocation logic
4. **Construct the graph** - Linear pipeline: brainstormer → writer → editor
5. **Test it** - Try: "Create a blog post about machine learning"

#### Success Criteria

✅ All 3 agents have tools bound  
✅ State passes information through the pipeline  
✅ Each agent invokes its tool  
✅ Final output is polished content  
✅ Graph compiles and runs without errors

#### Bonus Challenges

- **Add a 4th agent** - Fact-checker that validates claims

#### Tips

- Start by copying the collaborative pattern structure
- Keep tools simple - they can return hardcoded examples
- Test each agent individually before connecting them
- Use print statements to see the pipeline flow

---

## 📝 Summary

### What You Learned

1. **Why Multi-Agent**

   - Specialization vs generalization
   - Modularity and debuggability
   - When to split vs keep single agent

2. **Supervised Pattern (Orchestrator)**

   - Centralized orchestration with supervisor
   - Supervisor dynamically routes to specialist agents
   - Each specialist has dedicated tools
   - Best for tasks requiring dynamic delegation

3. **Collaborative Pattern (Handoff)**
   - Fixed linear pipeline workflow
   - Agents pass work sequentially
   - Each agent has specialized tools
   - Best for predictable, stage-based processing

### You've Mastered

- ✅ Multi-Agent Architecture Patterns
- ✅ Tool-equipped Agent Design
- ✅ Agent Coordination Strategies
- ✅ State Management Across Agents
- ✅ Production-Ready Patterns

**You're ready to build real-world multi-agent systems!** 🎉
