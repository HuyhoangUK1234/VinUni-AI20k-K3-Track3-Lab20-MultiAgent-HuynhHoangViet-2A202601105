"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown."""

    lines = [
        "# Benchmark Report",
        "",
        "This report compares runs using latency, estimated cost, quality, citation coverage, "
        "token usage, and failure rate. Quality is a lightweight heuristic intended for lab "
        "iteration.",
        "",
        "| Run | Latency (s) | Input tok. | Output tok. | Total tok. | Cost (USD) | "
        "Quality | Citation cov. | Failure rate | Notes |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in metrics:
        input_tokens = "" if item.input_tokens is None else str(item.input_tokens)
        output_tokens = "" if item.output_tokens is None else str(item.output_tokens)
        total_tokens = "" if item.total_tokens is None else str(item.total_tokens)
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        citation = "" if item.citation_coverage is None else f"{item.citation_coverage:.0%}"
        failure = "" if item.failure_rate is None else f"{item.failure_rate:.0%}"
        lines.append(
            f"| {item.run_name} | {item.latency_seconds:.2f} | {input_tokens} | "
            f"{output_tokens} | {total_tokens} | {cost} | {quality} | {citation} | "
            f"{failure} | {item.notes} |"
        )
    if metrics:
        best = max(metrics, key=lambda item: item.quality_score or 0)
        fastest = min(metrics, key=lambda item: item.latency_seconds)
        lines.extend(
            [
                "",
                "## Summary",
                "",
                f"- Highest quality run: `{best.run_name}`.",
                f"- Fastest run: `{fastest.run_name}`.",
                "- Review traces alongside this table before making production decisions.",
            ]
        )
    return "\n".join(lines) + "\n"
