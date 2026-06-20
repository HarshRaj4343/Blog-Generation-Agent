import operator
from typing import Annotated, Literal, TypedDict


class BlogAgentState(TypedDict, total=False):
    topic: str
    needs_research: bool
    mode: Literal["closed_book", "hybrid", "open_book"]
    queries: list[str]
    research_results: str
    plan: list[str]
    section_plan: str
    sections: Annotated[list[str], operator.add]
    final_blog: str
