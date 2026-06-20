from load_llm import llm
from system_prompts import ROUTER_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from state import BlogAgentState
from pydantic import BaseModel
from typing import Literal

class RouteSchema(BaseModel):
    needs_research: bool
    mode: Literal[
        "closed_book",
        "hybrid",
        "open_book"
    ]
    queries: list[str]

route_model = llm.with_structured_output(RouteSchema)

def router(state: BlogAgentState) -> BlogAgentState:
    decision = route_model.invoke([
        SystemMessage(content=ROUTER_PROMPT),
        HumanMessage(content=state["topic"])
    ])
    return {
        "mode": decision.mode,
        "needs_research": decision.needs_research,
        "queries": decision.queries,
    }
