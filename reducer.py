from state import BlogAgentState


def reducer(state: BlogAgentState) -> BlogAgentState:
    return {"final_blog": "\n\n".join(state["sections"])}
