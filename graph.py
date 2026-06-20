from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from Orchestrator import orchestrator
from Research import research
from Router import router
from reducer import reducer
from state import BlogAgentState
from worker import worker

def classifier(state: BlogAgentState) -> Literal["Research", "Orchestrator"]:
    """
    Classify the state of the blog agent to determine the next step in the graph.
    """
    if state["needs_research"]:
        return "Research"
    return "Orchestrator"


def assign_workers(state: BlogAgentState) -> list[Send]:
    return [
        Send(
            "Worker",
            {
                "topic": state["topic"],
                "research_results": state.get("research_results", ""),
                "section_plan": section_plan,
            },
        )
        for section_plan in state["plan"]
    ]


graph = StateGraph(BlogAgentState)
graph.add_node("Router", router)
graph.add_node("Research", research)
graph.add_node("Orchestrator", orchestrator)
graph.add_node("Worker", worker)
graph.add_node("Reducer", reducer)


graph.add_edge(START, "Router")
graph.add_conditional_edges("Router", classifier)
graph.add_edge("Research", "Orchestrator")
graph.add_conditional_edges("Orchestrator", assign_workers, ["Worker"])
graph.add_edge("Worker", "Reducer")
graph.add_edge("Reducer", END)
graph = graph.compile()


png_data = graph.get_graph().draw_mermaid_png()

with open("workflow.png", "wb") as f:
    f.write(png_data)