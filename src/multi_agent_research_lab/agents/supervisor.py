"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route.
        """

        settings = get_settings()
        route = self._select_route(state, max_iterations=settings.max_iterations)
        state.record_route(route)
        state.add_trace_event(
            self.name,
            {
                "next_route": route,
                "iteration": state.iteration,
                "has_research": state.research_notes is not None,
                "has_analysis": state.analysis_notes is not None,
                "has_final_answer": state.final_answer is not None,
            },
        )
        state.agent_results.append(
            AgentResult(
                agent=AgentName.SUPERVISOR,
                content=f"Next route: {route}",
                metadata={"iteration": state.iteration},
            )
        )
        return state

    def _select_route(self, state: ResearchState, max_iterations: int) -> str:
        if state.iteration >= max_iterations:
            state.errors.append("Supervisor stopped workflow because max_iterations was reached.")
            return "done"
        if state.final_answer:
            return "done"
        if not state.research_notes:
            return "researcher"
        if not state.analysis_notes:
            return "analyst"
        return "writer"
