"""Optional critic agent skeleton for bonus work."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings.
        """

        findings: list[str] = []
        if not state.final_answer:
            findings.append("Final answer is missing.")
        if not state.sources:
            findings.append("No sources were collected.")
        if state.sources and state.final_answer:
            cited_count = sum(
                1
                for index in range(1, len(state.sources) + 1)
                if f"[{index}]" in state.final_answer
            )
            coverage = cited_count / len(state.sources)
            if coverage < 0.5:
                findings.append("Citation coverage is below 50%.")
        if not findings:
            findings.append("No blocking quality issues found.")

        content = "\n".join(f"- {finding}" for finding in findings)
        state.agent_results.append(
            AgentResult(
                agent=AgentName.CRITIC,
                content=content,
                metadata={"finding_count": len(findings)},
            )
        )
        state.add_trace_event(self.name, {"findings": findings})
        return state
