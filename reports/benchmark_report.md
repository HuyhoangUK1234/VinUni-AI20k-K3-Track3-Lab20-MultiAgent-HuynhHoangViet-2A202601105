# Benchmark Report

This report compares runs using latency, estimated cost, quality, citation coverage, token usage, and failure rate. Quality is a lightweight heuristic intended for lab iteration.

| Run | Latency (s) | Input tok. | Output tok. | Total tok. | Cost (USD) | Quality | Citation cov. | Failure rate | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| single-agent-baseline | 0.00 | 45 | 84 | 129 |  | 4.0 | 0% | 0% | 0 sources, 0 routed steps |
| multi-agent-offline-corpus | 3.08 | 1807 | 179 | 1986 |  | 10.0 | 100% | 0% | 5 sources, 4 routed steps |

## Summary

- Highest quality run: `multi-agent-offline-corpus`.
- Fastest run: `single-agent-baseline`.
- Review traces alongside this table before making production decisions.

## LangSmith Trace

- Project: `lab20`
- Latest trace: https://smith.langchain.com/o/eacdc454-5f48-4596-9275-57d7094d1036/projects/p/352c4226-c0c9-49ad-a3bf-7ba0a6f28204/r/01a01de5-220c-7c40-80aa-9b0a4742600b?poll=true

## Demo Notes

- Single-agent baseline is faster because it performs one generation step.
- Multi-agent workflow is slower because it retrieves sources, analyzes notes, and writes with citations.
- Token usage is estimated by the local LLM fallback unless USE_LIVE_LLM=true.

## Failure Mode and Fix

Failure mode observed during implementation: the system initially tried to use live external
providers whenever API keys were present in `.env`. In an offline or restricted lab environment,
this could cause connection failures and make the demo non-reproducible.

Fix: `LLMClient` now uses a deterministic local fallback by default and only calls a live LLM
when `USE_LIVE_LLM=true`. `SearchClient` also uses the offline corpus in
`ai_agent_offline_research_corpus_v2`, so benchmark results are stable and repeatable. LangSmith
tracing is enabled for CLI runs, but disabled during pytest to keep tests deterministic.

## Route History

- Baseline: ['single-step']
- Multi-agent: ['researcher', 'analyst', 'writer', 'done']

## Multi-Agent Sources

- [1] Single-Agent vs Multi-Agent Architectures for Complex Research Tasks / Evaluation methodology and metrics (offline-corpus://AIAGENT-01:A04)
- [2] Single-Agent vs Multi-Agent Architectures for Complex Research Tasks / Comparative analysis and boundary conditions (offline-corpus://AIAGENT-01:A06)
- [3] Single-Agent vs Multi-Agent Architectures for Complex Research Tasks / Conceptual overview and research framing (offline-corpus://AIAGENT-01:A01)
- [4] Single-Agent vs Multi-Agent Architectures for Complex Research Tasks / Architecture and mechanisms (offline-corpus://AIAGENT-01:A02)
- [5] Single-Agent vs Multi-Agent Architectures for Complex Research Tasks / Implementation patterns and anti-patterns (offline-corpus://AIAGENT-01:A03)
