"""Tracing hooks.

This file intentionally avoids binding to one provider. Students can plug in LangSmith,
Langfuse, OpenTelemetry, or simple JSON traces.
"""

import os
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from time import perf_counter
from typing import Any

from multi_agent_research_lab.core.config import get_settings


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
    """Minimal span context that can be exported or mirrored to an observability provider."""

    started = perf_counter()
    span: dict[str, Any] = {"name": name, "attributes": attributes or {}, "duration_seconds": None}
    langsmith_context = _langsmith_trace(name, span["attributes"])
    langsmith_run = None
    try:
        langsmith_run = langsmith_context.__enter__() if langsmith_context else None
        yield span
    except Exception as exc:
        if langsmith_run is not None:
            with suppress(Exception):
                langsmith_run.end(error=str(exc))
        raise
    finally:
        span["duration_seconds"] = perf_counter() - started
        if langsmith_run is not None:
            with suppress(Exception):
                langsmith_run.end(outputs={"span": span})
        if langsmith_context is not None:
            with suppress(Exception):
                langsmith_context.__exit__(None, None, None)


def _langsmith_trace(name: str, attributes: dict[str, Any]) -> Any | None:
    settings = get_settings()
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return None
    if not settings.langsmith_api_key:
        return None
    try:
        from langsmith import Client
        from langsmith.run_helpers import trace
    except ImportError:
        return None
    os.environ["LANGSMITH_TRACING_V2"] = "true"
    return trace(
        name,
        run_type="chain",
        inputs={"attributes": attributes},
        project_name=settings.langsmith_project,
        tags=["multi-agent-research-lab"],
        metadata={"app_env": settings.app_env},
        client=Client(api_key=settings.langsmith_api_key),
    )
