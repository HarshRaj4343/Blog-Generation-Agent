import os

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from exa_py import Exa

from load_llm import llm
from state import BlogAgentState
from system_prompts import RESEARCH_PROMPT


@tool
def exa_search_tool(query: str) -> str:
    """
    Search the web using Exa.
    """
    exa = Exa(api_key=os.getenv("EXA_API_KEY"))
    results = exa.search(
        query,
        num_results=5,
        contents={"highlights": True},
    )

    output = []

    for r in results.results:
        output.append(
            f"""
            Title: {r.title}
            URL: {r.url}
            Highlights: {' '.join(r.highlights or [])}
            """
        )

    return "\n\n".join(output)


research_model = llm.bind_tools([exa_search_tool])


def research(state: BlogAgentState) -> BlogAgentState:
    """
    Perform research based on the state of the blog agent.
    """
    if not state["needs_research"]:
        return {"research_results": ""}

    summaries = []
    for query in state["queries"]:
        messages = [
            SystemMessage(content=RESEARCH_PROMPT),
            HumanMessage(content=query),
        ]
        response = research_model.invoke(messages)

        if response.tool_calls:
            messages.append(response)
            for tool_call in response.tool_calls:
                tool_result = exa_search_tool.invoke(tool_call["args"])
                messages.append(
                    ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
                )
            response = research_model.invoke(messages)

        summaries.append(f"Research results for query '{query}':\n{response.content}")

    return {"research_results": "\n\n".join(summaries)}
