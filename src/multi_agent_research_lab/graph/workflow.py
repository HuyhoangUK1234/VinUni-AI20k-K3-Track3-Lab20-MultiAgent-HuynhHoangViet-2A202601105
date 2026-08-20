"""LangGraph workflow skeleton."""

from time import perf_counter

from multi_agent_research_lab.agents import (
    AnalystAgent,
    ResearcherAgent,
    SupervisorAgent,
    WriterAgent,
)
from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import AgentExecutionError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.observability.tracing import trace_span


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> dict[str, BaseAgent]:
        """Create the executable graph node registry.

        Suggested nodes: supervisor, researcher, analyst, writer, optional critic.
        """

        return {
            "supervisor": SupervisorAgent(),
            "researcher": ResearcherAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
        }

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state.
        """

        settings = get_settings()
        graph = self.build()
        started = perf_counter()

        with trace_span("multi_agent_workflow", {"query": state.request.query}) as span:
            while True:
                if perf_counter() - started > settings.timeout_seconds:
                    state.errors.append("Workflow stopped because timeout_seconds was reached.")
                    break

                supervisor = graph["supervisor"]
                state = supervisor.run(state)
                route = state.route_history[-1]
                if route == "done":
                    break

                worker = graph.get(route)
                if worker is None:
                    raise AgentExecutionError(f"Supervisor selected unknown route: {route}")
                state = worker.run(state)

            span["final_route_history"] = state.route_history
            span["error_count"] = len(state.errors)
            state.add_trace_event(
                "workflow",
                {
                    "route_history": state.route_history,
                    "error_count": len(state.errors),
                    "duration_seconds": perf_counter() - started,
                },
            )
        return state
