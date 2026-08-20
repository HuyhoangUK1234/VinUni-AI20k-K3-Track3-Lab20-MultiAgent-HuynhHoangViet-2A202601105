"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult, SourceDocument
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def __init__(
        self,
        search_client: SearchClient | None = None,
        llm_client: LLMClient | None = None,
    ) -> None:
        self.search_client = search_client or SearchClient()
        self.llm_client = llm_client or LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`.
        """

        sources = self.search_client.search(
            state.request.query,
            max_results=state.request.max_sources,
        )
        state.sources = self._dedupe_sources([*state.sources, *sources])
        prompt = self._build_prompt(state)
        response = self.llm_client.complete(
            system_prompt=(
                "You are a careful research assistant. "
                "Produce concise notes with source ids."
            ),
            user_prompt=prompt,
        )
        state.research_notes = response.content
        state.agent_results.append(
            AgentResult(
                agent=AgentName.RESEARCHER,
                content=response.content,
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
            {
                "source_count": len(state.sources),
                "source_titles": [source.title for source in state.sources],
            },
        )
        return state

    def _build_prompt(self, state: ResearchState) -> str:
        source_lines = [
            f"[{index}] {source.title}: {source.snippet}"
            for index, source in enumerate(state.sources, start=1)
        ]
        return (
            f"Research query: {state.request.query}\n"
            f"Audience: {state.request.audience}\n"
            "Sources:\n"
            + "\n".join(source_lines)
        )

    def _dedupe_sources(self, sources: list[SourceDocument]) -> list[SourceDocument]:
        seen: set[str] = set()
        deduped: list[SourceDocument] = []
        for source in sources:
            key = source.url or source.title
            if key in seen:
                continue
            seen.add(key)
            deduped.append(source)
        return deduped
