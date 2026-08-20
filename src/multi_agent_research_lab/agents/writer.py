"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`.
        """

        response = self.llm_client.complete(
            system_prompt=(
                "You are a technical writer. Produce a clear final answer grounded in the "
                "provided research and analysis. Include source references when available."
            ),
            user_prompt=(
                f"Query: {state.request.query}\n"
                f"Audience: {state.request.audience}\n\n"
                f"Research notes:\n{state.research_notes or 'No research notes.'}\n\n"
                f"Analysis notes:\n{state.analysis_notes or 'No analysis notes.'}\n\n"
                f"Source references:\n{self._format_sources(state)}"
            ),
        )
        citations = self._format_citations(state)
        state.final_answer = f"{response.content}\n\nSources:\n{citations}".strip()
        state.agent_results.append(
            AgentResult(
                agent=AgentName.WRITER,
                content=state.final_answer,
                metadata={
                    "source_count": len(state.sources),
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "cost_usd": response.cost_usd,
                },
            )
        )
        state.add_trace_event(
            self.name,
            {"final_answer_length": len(state.final_answer), "source_count": len(state.sources)},
        )
        return state

    def _format_sources(self, state: ResearchState) -> str:
        if not state.sources:
            return "No sources."
        return "\n".join(
            f"[{index}] {source.title} - {source.url or 'no url'}: {source.snippet}"
            for index, source in enumerate(state.sources, start=1)
        )

    def _format_citations(self, state: ResearchState) -> str:
        if not state.sources:
            return "- No external sources were collected."
        return "\n".join(
            f"- [{index}] {source.title} ({source.url or 'no url'})"
            for index, source in enumerate(state.sources, start=1)
        )
