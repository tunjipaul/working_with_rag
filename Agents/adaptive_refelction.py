import os
from typing import Literal, TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field

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


class QualityScore(BaseModel):
    """Structured quality scoring for reflection."""

    clarity: int = Field(
        description="How clear and understandable is the content? (1-5)", ge=1, le=5
    )
    completeness: int = Field(
        description="How complete and thorough is the content? (1-5)", ge=1, le=5
    )
    accuracy: int = Field(
        description="How accurate and correct is the content? (1-5)", ge=1, le=5
    )
    feedback: str = Field(description="Specific feedback on what needs improvement")

    def is_approved(self) -> bool:
        """Check if all scores meet the threshold."""
        return self.clarity >= 4 and self.completeness >= 4 and self.accuracy >= 4

    def __str__(self):
        return f"Clarity: {self.clarity}, Completeness: {self.completeness}, Accuracy: {self.accuracy}"


class AdaptiveReflectionState(TypedDict):
    """State for adaptive reflection with quality metrics."""

    task: str
    draft: str
    scores: list[QualityScore]
    iterations: int
    final_output: str


MAX_ITERATIONS = 3


def generator(state: AdaptiveReflectionState) -> dict:
    """Generate or refine based on quality scores."""
    if state["iterations"] == 0:
        prompt = f"""Create a response for this task:

Task: {state['task']}

Provide a clear, complete, and accurate answer."""
        print("\nGenerating initial draft...")
    else:
        last_score = state["scores"][-1]
        prompt = f"""Improve this draft based on the quality feedback:

Task: {state['task']}

Current draft: {state['draft']}

Quality Scores: {last_score}
Feedback: {last_score.feedback}

Create an improved version addressing the feedback."""
        print(f"\nRefining (iteration {state['iterations']})...")
        print(f"Previous scores: {last_score}")

    response = llm.invoke([HumanMessage(content=prompt)])
    print("Draft created")

    return {"draft": response.content}


def critic(state: AdaptiveReflectionState) -> dict:
    """Evaluate draft with structured quality scoring."""
    llm_with_structure = llm.with_structured_output(QualityScore)

    prompt = f"""Evaluate this response on three criteria (score 1-5 each):

Task: {state['task']}

Response: {state['draft']}

Criteria:
1. Clarity (1-5): Is it clear and easy to understand?
2. Completeness (1-5): Does it fully address the task?
3. Accuracy (1-5): Is the information correct?

For each score below 4, provide specific feedback on what needs improvement.
If all scores are 4 or above, the response is approved."""

    print("\nCritiquing draft...")
    score = llm_with_structure.invoke([HumanMessage(content=prompt)])

    print(f"Quality Scores: {score}")
    print(f"Feedback: {score.feedback}")

    scores = state.get("scores", []) + [score]

    return {"scores": scores, "iterations": state["iterations"] + 1}


def finalizer(state: AdaptiveReflectionState) -> dict:
    """Set final output."""
    print("\nReflection complete!")

    if state["scores"]:
        final_score = state["scores"][-1]
        print(f"\nFinal Quality Scores: {final_score}")

    return {"final_output": state["draft"]}


def should_refine(state: AdaptiveReflectionState) -> Literal["generator", "finalizer"]:
    """Decide if refinement is needed based on quality scores."""
    if not state.get("scores"):
        return "generator"

    last_score = state["scores"][-1]

    if last_score.is_approved():
        print("\nAll scores >= 4! Approved.")
        return "finalizer"

    if state["iterations"] >= MAX_ITERATIONS:
        print(f"\nMax iterations ({MAX_ITERATIONS}) reached.")
        return "finalizer"

    print(f"\nScores below threshold. Refining...")
    return "generator"


reflection_builder = StateGraph(AdaptiveReflectionState)

reflection_builder.add_node("generator", generator)
reflection_builder.add_node("critic", critic)
reflection_builder.add_node("finalizer", finalizer)

reflection_builder.add_edge(START, "generator")
reflection_builder.add_edge("generator", "critic")
reflection_builder.add_conditional_edges(
    "critic", should_refine, {"generator": "generator", "finalizer": "finalizer"}
)
reflection_builder.add_edge("finalizer", END)

adaptive_reflection_agent = reflection_builder.compile()

print("Adaptive Reflection agent created with quality metrics")


def test_adaptive_reflection(task: str):
    """Test the adaptive reflection agent."""
    print("\n" + "=" * 80)
    print(f"Task: {task}")
    print("=" * 80)

    result = adaptive_reflection_agent.invoke(
        {"task": task, "draft": "", "scores": [], "iterations": 0, "final_output": ""}
    )

    print("\n" + "=" * 80)
    print("FINAL OUTPUT:")
    print("=" * 80)
    print(result["final_output"])

    print("\n" + "=" * 80)
    print("SCORE PROGRESSION:")
    print("=" * 80)
    for i, score in enumerate(result["scores"], 1):
        print(f"\nIteration {i}: {score}")
        print(f"  Feedback: {score.feedback}")

    print(f"\nTotal iterations: {result['iterations']}")
    print("=" * 80 + "\n")

    return result


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ADAPTIVE REFLECTION WITH QUALITY METRICS")
    print("=" * 80)

    test_adaptive_reflection(
        "Explain what machine learning is in simple terms for a beginner"
    )

    test_adaptive_reflection(
        "Write a professional email requesting a meeting with your manager"
    )
