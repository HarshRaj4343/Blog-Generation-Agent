from langchain_core.messages import HumanMessage, SystemMessage

from load_llm import llm
from state import BlogAgentState
from system_prompts import WORKER_PROMPT


def worker(state: BlogAgentState) -> BlogAgentState:
    response = llm.invoke(
        [
            SystemMessage(content=WORKER_PROMPT),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n\n"
                    f"Section blueprint:\n{state['section_plan']}\n\n"
                    "Research results:\n"
                    f"{state.get('research_results', 'No external research was required.')}"
                )
            ),
        ]
    )
    return {"sections": [response.content]}
