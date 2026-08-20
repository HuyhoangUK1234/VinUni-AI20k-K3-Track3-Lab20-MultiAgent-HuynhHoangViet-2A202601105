"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`.
        """

        if not state.research_notes:
            state.errors.append("Analyst skipped because research_notes is missing.")
            state.analysis_notes = "No research notes were available for analysis."
        else:
            response = self.llm_client.complete(
                system_prompt=(
                    "You are an analyst. Extract key claims, confidence, weak evidence, "
                    "and implications from research notes."
                ),
                user_prompt=(
                    f"Query: {state.request.query}\n"
                    f"Research notes:\n{state.research_notes}\n\n"
                    "Return concise structured analysis."
                ),
            )
            state.analysis_notes = response.content
            state.agent_results.append(
                AgentResult(
                    agent=AgentName.ANALYST,
                    content=response.content,
                    metadata={
                        "input_tokens": response.input_tokens,
                        "output_tokens": response.output_tokens,
                        "cost_usd": response.cost_usd,
                    },
                )
            )
        state.add_trace_event(
            self.name,
            {
                "has_research_notes": state.research_notes is not None,
                "analysis_length": len(state.analysis_notes or ""),
            },
        )
        return state
