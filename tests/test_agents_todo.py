"""Agent behavior tests."""

from multi_agent_research_lab.agents import SupervisorAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow


def test_supervisor_routes_to_first_missing_step() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))
    state = SupervisorAgent().run(state)
    assert state.route_history == ["researcher"]

    state.research_notes = "Research is complete."
    state = SupervisorAgent().run(state)
    assert state.route_history[-1] == "analyst"

    state.analysis_notes = "Analysis is complete."
    state = SupervisorAgent().run(state)
    assert state.route_history[-1] == "writer"

    state.final_answer = "Final answer."
    state = SupervisorAgent().run(state)
    assert state.route_history[-1] == "done"


def test_workflow_runs_end_to_end() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))
    result = MultiAgentWorkflow().run(state)
    assert result.sources
    assert result.research_notes
    assert result.analysis_notes
    assert result.final_answer
    assert result.route_history == ["researcher", "analyst", "writer", "done"]
