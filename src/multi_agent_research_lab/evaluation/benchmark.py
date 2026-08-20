"""Benchmark skeleton for single-agent vs multi-agent."""

from collections.abc import Callable
from time import perf_counter

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState

Runner = Callable[[str], ResearchState]


def run_benchmark(
    run_name: str, query: str, runner: Runner
) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and derive lightweight quality metrics."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    cost = _estimate_total_cost(state)
    input_tokens, output_tokens = _token_usage(state)
    citation_coverage = _citation_coverage(state)
    failure_rate = 1.0 if state.errors else 0.0
    quality_score = _quality_score(state, citation_coverage, failure_rate)
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=(
            None if input_tokens is None or output_tokens is None else input_tokens + output_tokens
        ),
        estimated_cost_usd=cost,
        quality_score=quality_score,
        citation_coverage=citation_coverage,
        failure_rate=failure_rate,
        notes=f"{len(state.sources)} sources, {len(state.route_history)} routed steps",
    )
    return state, metrics


def _token_usage(state: ResearchState) -> tuple[int | None, int | None]:
    input_tokens = 0
    output_tokens = 0
    found = False
    for result in state.agent_results:
        raw_input = result.metadata.get("input_tokens")
        raw_output = result.metadata.get("output_tokens")
        if isinstance(raw_input, int):
            input_tokens += raw_input
            found = True
        if isinstance(raw_output, int):
            output_tokens += raw_output
            found = True
    if not found:
        return None, None
    return input_tokens, output_tokens


def _estimate_total_cost(state: ResearchState) -> float | None:
    costs: list[float] = []
    for result in state.agent_results:
        cost = result.metadata.get("cost_usd")
        if isinstance(cost, int | float):
            costs.append(float(cost))
    if not costs:
        return None
    return sum(costs)


def _citation_coverage(state: ResearchState) -> float:
    if not state.sources:
        return 0.0
    if not state.final_answer:
        return 0.0
    cited = sum(
        1
        for index in range(1, len(state.sources) + 1)
        if f"[{index}]" in state.final_answer
    )
    return cited / len(state.sources)


def _quality_score(state: ResearchState, citation_coverage: float, failure_rate: float) -> float:
    score = 0.0
    if state.research_notes:
        score += 2.0
    if state.analysis_notes:
        score += 2.0
    if state.final_answer:
        score += 3.0
    score += 2.0 * citation_coverage
    score += 1.0 if not state.errors else 0.0
    score -= 2.0 * failure_rate
    return max(0.0, min(10.0, score))
