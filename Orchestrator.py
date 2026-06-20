from load_llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from schemas import BlogPlan
from state import BlogAgentState
from system_prompts import ORCHESTRATOR_PROMPT

planning_model = llm.with_structured_output(BlogPlan)


def orchestrator(state: BlogAgentState) -> BlogAgentState:
    plan = planning_model.invoke(
        [SystemMessage(content=ORCHESTRATOR_PROMPT),HumanMessage(content=(
                    f"Topic: {state['topic']}\n"
                    "Research Results: "
                    f"{state.get('research_results', 'No external research was required.')}"
                )),])
    return {"plan": plan.sections}
