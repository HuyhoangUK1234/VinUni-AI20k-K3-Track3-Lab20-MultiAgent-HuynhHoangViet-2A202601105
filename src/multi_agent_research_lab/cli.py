"""Command-line entrypoint for the lab starter."""

from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import AgentName, AgentResult, ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.storage import LocalArtifactStore

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


def _parse_query(query: str) -> ResearchQuery:
    try:
        return ResearchQuery(query=query)
    except ValidationError as exc:
        console.print(
            Panel.fit(
                f"Invalid query: {exc.errors()[0]['msg']}",
                title="Input Error",
                style="red",
            )
        )
        raise typer.Exit(code=1) from exc


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the single-agent baseline."""

    _init()
    request = _parse_query(query)
    state = ResearchState(request=request)
    response = LLMClient().complete(
        system_prompt="You are a single-agent research assistant.",
        user_prompt=(
            f"Research and answer this query for {request.audience}: {request.query}. "
            "Keep the response concise and mention when external search was not used."
        ),
    )
    state.final_answer = response.content
    console.print(Panel.fit(state.final_answer, title="Single-Agent Baseline"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow."""

    _init()
    state = ResearchState(request=_parse_query(query))
    workflow = MultiAgentWorkflow()
    result = workflow.run(state)
    console.print(result.model_dump_json(indent=2))


@app.command()
def benchmark(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Report path under reports/"),
    ] = "benchmark_report.md",
) -> None:
    """Compare single-agent baseline with the multi-agent workflow."""

    _init()
    request = _parse_query(query)

    def baseline_runner(raw_query: str) -> ResearchState:
        baseline_state = ResearchState(request=ResearchQuery(query=raw_query))
        response = LLMClient().complete(
            system_prompt="You are a single-agent research assistant.",
            user_prompt=(
                f"Research and answer this query for {request.audience}: {raw_query}. "
                "Keep the response concise and mention when external search was not used."
            ),
        )
        baseline_state.final_answer = response.content
        baseline_state.agent_results.append(
            AgentResult(
                agent=AgentName.WRITER,
                content=response.content,
                metadata={
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "cost_usd": response.cost_usd,
                },
            )
        )
        return baseline_state

    def multi_agent_runner(raw_query: str) -> ResearchState:
        return MultiAgentWorkflow().run(ResearchState(request=ResearchQuery(query=raw_query)))

    baseline_state, baseline_metrics = run_benchmark(
        "single-agent-baseline",
        request.query,
        baseline_runner,
    )
    multi_state, multi_metrics = run_benchmark(
        "multi-agent-offline-corpus",
        request.query,
        multi_agent_runner,
    )
    report = render_markdown_report([baseline_metrics, multi_metrics])
    report += _render_benchmark_details(baseline_state, multi_state)
    path = LocalArtifactStore().write_text(output, report)
    console.print(Panel.fit(str(path), title="Benchmark Report Written", style="green"))
    console.print(report)


def _render_benchmark_details(
    baseline_state: ResearchState,
    multi_state: ResearchState,
) -> str:
    source_lines = [
        f"- [{index}] {source.title} ({source.url or 'no url'})"
        for index, source in enumerate(multi_state.sources, start=1)
    ]
    if not source_lines:
        source_lines = ["- No sources collected."]

    return (
        "\n## Demo Notes\n\n"
        "- Single-agent baseline is faster because it performs one generation step.\n"
        "- Multi-agent workflow is slower because it retrieves sources, analyzes notes, "
        "and writes with citations.\n"
        "- Token usage is estimated by the local LLM fallback unless USE_LIVE_LLM=true.\n\n"
        "## Route History\n\n"
        f"- Baseline: {baseline_state.route_history or ['single-step']}\n"
        f"- Multi-agent: {multi_state.route_history}\n\n"
        "## Multi-Agent Sources\n\n"
        + "\n".join(source_lines)
        + "\n"
    )


if __name__ == "__main__":
    app()
