import os
from typing import Literal, TypedDict, Annotated
from dotenv import load_dotenv
import operator

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found! Please set it in your .env file.")

print("API key loaded")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", temperature=0.3, api_key=google_api_key
)

print("LLM initialized: Gemini 2.5 Flash Lite")


class PlanExecuteReflectState(TypedDict):
    """Hybrid state combining Plan-Execute and Reflection."""

    input: str
    plan: list[str]
    current_step: int
    results: Annotated[list[str], operator.add]
    draft: str
    critique: str
    reflection_iterations: int
    final_output: str


MAX_REFLECTION_ITERATIONS = 2


def planner(state: PlanExecuteReflectState) -> dict:
    """Create a step-by-step plan."""
    prompt = f"""Create a step-by-step plan for this task:

Task: {state['input']}

Return a numbered list of concrete steps. Keep it simple (3-5 steps).
Each step should be clear and actionable."""

    response = llm.invoke([HumanMessage(content=prompt)])

    lines = response.content.split("\n")
    steps = [
        line.strip()
        for line in lines
        if line.strip() and any(char.isdigit() for char in line[:3])
    ]

    print("\nPLAN CREATED:")
    for step in steps:
        print(f"  {step}")
    print()

    return {"plan": steps, "current_step": 0, "results": [], "reflection_iterations": 0}


def executor(state: PlanExecuteReflectState) -> dict:
    """Execute current step."""
    if state["current_step"] >= len(state["plan"]):
        return {}

    current_step = state["plan"][state["current_step"]]

    print(f"Executing: {current_step}")

    prompt = f"""Previous results: {state.get('results', [])}

Execute this step: {current_step}

Provide a clear result for this step."""

    response = llm.invoke([HumanMessage(content=prompt)])

    result = f"Step {state['current_step'] + 1} result: {response.content}"
    print(f"Done\n")

    return {"results": [result], "current_step": state["current_step"] + 1}


def should_continue_execution(
    state: PlanExecuteReflectState,
) -> Literal["executor", "generator"]:
    """Decide if more steps to execute."""
    if state["current_step"] < len(state["plan"]):
        return "executor"
    return "generator"


def generator(state: PlanExecuteReflectState) -> dict:
    """Generate initial output from execution results."""
    if state["reflection_iterations"] == 0:
        prompt = f"""Synthesize these execution results into a complete answer:

Original task: {state['input']}

Execution results:
{chr(10).join(state['results'])}

Create a clear, comprehensive final answer."""
        print("\nGenerating initial draft from execution results...")
    else:
        prompt = f"""Improve this draft based on the critique:

Task: {state['input']}

Current draft: {state['draft']}

Critique: {state['critique']}

Create an improved version addressing the critique."""
        print(
            f"\nRefining draft (reflection iteration {state['reflection_iterations']})..."
        )

    response = llm.invoke([HumanMessage(content=prompt)])
    print("Draft created")

    return {"draft": response.content}


def critic(state: PlanExecuteReflectState) -> dict:
    """Evaluate the generated output."""
    prompt = f"""Evaluate this response for quality:

Task: {state['input']}

Response: {state['draft']}

Provide constructive critique. Consider:
- Is it clear and well-organized?
- Does it fully address the task?
- Is it appropriate for the target audience?

If it's excellent, start with "APPROVED:".
Otherwise, provide specific improvements needed."""

    print("\nCritiquing draft...")
    response = llm.invoke([HumanMessage(content=prompt)])
    critique = response.content

    print(f"Critique: {critique[:150]}...")

    return {
        "critique": critique,
        "reflection_iterations": state["reflection_iterations"] + 1,
    }


def should_refine(
    state: PlanExecuteReflectState,
) -> Literal["generator", "finalizer"]:
    """Decide if refinement is needed."""
    if "APPROVED" in state.get("critique", "").upper():
        print("\nApproved!")
        return "finalizer"

    if state["reflection_iterations"] >= MAX_REFLECTION_ITERATIONS:
        print(f"\nMax reflection iterations ({MAX_REFLECTION_ITERATIONS}) reached.")
        return "finalizer"

    print("\nRefining based on critique...")
    return "generator"


def finalizer(state: PlanExecuteReflectState) -> dict:
    """Set final output."""
    print("\nPlan-Execute-Reflect complete!")
    return {"final_output": state["draft"]}


plan_execute_reflect_builder = StateGraph(PlanExecuteReflectState)

plan_execute_reflect_builder.add_node("planner", planner)
plan_execute_reflect_builder.add_node("executor", executor)
plan_execute_reflect_builder.add_node("generator", generator)
plan_execute_reflect_builder.add_node("critic", critic)
plan_execute_reflect_builder.add_node("finalizer", finalizer)

plan_execute_reflect_builder.add_edge(START, "planner")
plan_execute_reflect_builder.add_edge("planner", "executor")
plan_execute_reflect_builder.add_conditional_edges(
    "executor",
    should_continue_execution,
    {"executor": "executor", "generator": "generator"},
)
plan_execute_reflect_builder.add_edge("generator", "critic")
plan_execute_reflect_builder.add_conditional_edges(
    "critic", should_refine, {"generator": "generator", "finalizer": "finalizer"}
)
plan_execute_reflect_builder.add_edge("finalizer", END)

plan_execute_reflect_agent = plan_execute_reflect_builder.compile()

print("Plan-Execute-Reflect hybrid agent created")


def test_hybrid_agent(task: str):
    """Test the Plan-Execute-Reflect hybrid agent."""
    print("\n" + "=" * 80)
    print(f"Task: {task}")
    print("=" * 80)

    result = plan_execute_reflect_agent.invoke(
        {
            "input": task,
            "plan": [],
            "current_step": 0,
            "results": [],
            "draft": "",
            "critique": "",
            "reflection_iterations": 0,
            "final_output": "",
        }
    )

    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY:")
    print("=" * 80)
    print(f"\nPlan ({len(result['plan'])} steps):")
    for step in result["plan"]:
        print(f"  {step}")

    print(f"\nExecution Results:")
    for i, res in enumerate(result["results"], 1):
        print(f"  {i}. {res[:100]}...")

    print(f"\nReflection Iterations: {result['reflection_iterations']}")

    if result.get("critique"):
        print(f"\nFinal Critique: {result['critique'][:150]}...")

    print("\n" + "=" * 80)
    print("FINAL OUTPUT:")
    print("=" * 80)
    print(result["final_output"])
    print("=" * 80 + "\n")

    return result


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("PLAN-EXECUTE-REFLECT HYBRID AGENT")
    print("=" * 80)

    test_hybrid_agent(
        "Research the benefits of Python programming, create a summary, and make it beginner-friendly"
    )

    test_hybrid_agent(
        "Explain how machine learning works, provide examples, and make it accessible to non-technical people"
    )
