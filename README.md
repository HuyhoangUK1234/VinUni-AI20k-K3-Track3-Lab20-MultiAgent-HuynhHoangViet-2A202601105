# Lab 20: Multi-Agent Research System Starter

Starter repo cho bĂ i lab **Multi-Agent Systems**: xĂ¢y dá»±ng há»‡ thá»‘ng nghiĂªn cá»©u gá»“m **Supervisor + Researcher + Analyst + Writer** vĂ  benchmark vá»›i single-agent baseline.

> Má»¥c tiĂªu cá»§a repo nĂ y lĂ  cung cáº¥p **production-grade skeleton** Ä‘á»ƒ há»c viĂªn phĂ¡t triá»ƒn code cĂ¡ nhĂ¢n. CĂ¡c pháº§n logic quan trá»ng Ä‘Æ°á»£c Ä‘á»ƒ á»Ÿ dáº¡ng `TODO` Ä‘á»ƒ há»c viĂªn tá»± triá»ƒn khai.

## Learning outcomes

Sau 2 giá» lab, há»c viĂªn cáº§n cĂ³ thá»ƒ:

1. Thiáº¿t káº¿ role rĂµ rĂ ng cho nhiá»u agent.
2. XĂ¢y dá»±ng shared state Ä‘á»§ thĂ´ng tin cho handoff.
3. ThĂªm guardrail tá»‘i thiá»ƒu: max iterations, timeout, retry/fallback, validation.
4. Trace Ä‘Æ°á»£c luá»“ng cháº¡y vĂ  giáº£i thĂ­ch agent nĂ o lĂ m gĂ¬.
5. Benchmark single-agent vs multi-agent theo quality, latency, cost.

## Architecture má»¥c tiĂªu

```text
User Query
   |
   v
Supervisor / Router
   |------> Researcher Agent  -> research_notes
   |------> Analyst Agent     -> analysis_notes
   |------> Writer Agent      -> final_answer
   |
   v
Trace + Benchmark Report
```

## Cáº¥u trĂºc repo

```text
.
â”œâ”€â”€ src/multi_agent_research_lab/
â”‚   â”œâ”€â”€ agents/              # Agent interfaces + skeletons
â”‚   â”œâ”€â”€ core/                # Config, state, schemas, errors
â”‚   â”œâ”€â”€ graph/               # LangGraph workflow skeleton
â”‚   â”œâ”€â”€ services/            # LLM, search, storage clients
â”‚   â”œâ”€â”€ evaluation/          # Benchmark/evaluation skeleton
â”‚   â”œâ”€â”€ observability/       # Logging/tracing hooks
â”‚   â””â”€â”€ cli.py               # CLI entrypoint
â”œâ”€â”€ configs/                 # YAML configs for lab variants
â”œâ”€â”€ docs/                    # Lab guide, rubric, design notes
â”œâ”€â”€ tests/                   # Unit tests for skeleton behavior
â”œâ”€â”€ notebooks/               # Optional notebook entrypoint
â”œâ”€â”€ scripts/                 # Helper scripts
â”œâ”€â”€ .env.example             # Environment variables template
â”œâ”€â”€ pyproject.toml           # Python project config
â”œâ”€â”€ Dockerfile               # Containerized dev/runtime
â””â”€â”€ Makefile                 # Common commands
```

## Quickstart

### 1. Táº¡o mĂ´i trÆ°á»ng

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev,llm]"
cp .env.example .env
```

### 2. Cáº¥u hĂ¬nh API keys

Má»Ÿ `.env` vĂ  Ä‘iá»n key cáº§n thiáº¿t.

```bash
OPENAI_API_KEY=...
# optional
LANGSMITH_API_KEY=...
TAVILY_API_KEY=...
```

### 3. Cháº¡y smoke test

```bash
make test
python -m multi_agent_research_lab.cli --help
```

### 4. Cháº¡y baseline skeleton

```bash
python -m multi_agent_research_lab.cli baseline \
  --query "Research GraphRAG state-of-the-art and write a 500-word summary"
```

Lá»‡nh nĂ y chá»‰ cháº¡y khung baseline tá»‘i giáº£n. Há»c viĂªn cáº§n tá»± triá»ƒn khai logic LLM thá»±c táº¿ trong `src/multi_agent_research_lab/services/llm_client.py`.

### 5. Cháº¡y multi-agent skeleton

```bash
python -m multi_agent_research_lab.cli multi-agent \
  --query "Research GraphRAG state-of-the-art and write a 500-word summary"
```

Máº·c Ä‘á»‹nh lá»‡nh sáº½ bĂ¡o cĂ¡c `TODO` cáº§n lĂ m. ÄĂ¢y lĂ  chá»§ Ä‘Ă­ch cá»§a starter repo.

## Milestones trong 2 giá» lab

| Thá»i lÆ°á»£ng | Milestone | File gá»£i Ă½ |
|---:|---|---|
| 0-15' | Setup, cháº¡y baseline skeleton | `cli.py`, `services/llm_client.py` |
| 15-45' | Build Supervisor / router | `agents/supervisor.py`, `graph/workflow.py` |
| 45-75' | ThĂªm Researcher, Analyst, Writer | `agents/*.py`, `core/state.py` |
| 75-95' | Trace + benchmark single vs multi | `observability/tracing.py`, `evaluation/benchmark.py` |
| 95-115' | Peer review theo rubric | `docs/peer_review_rubric.md` |
| 115-120' | Exit ticket | `docs/lab_guide.md` |

## Quy Æ°á»›c production trong repo

- TĂ¡ch rĂµ `agents`, `services`, `core`, `graph`, `evaluation`, `observability`.
- KhĂ´ng hard-code API key trong code.
- Táº¥t cáº£ input/output chĂ­nh dĂ¹ng Pydantic schema.
- CĂ³ type hints, linting, formatting, unit test tá»‘i thiá»ƒu.
- CĂ³ logging/tracing hook ngay tá»« Ä‘áº§u.
- KhĂ´ng Ä‘á»ƒ agent cháº¡y vĂ´ háº¡n: dĂ¹ng `max_iterations`, `timeout_seconds`.
- CĂ³ benchmark report thay vĂ¬ chá»‰ demo output Ä‘áº¹p.

## TODO chĂ­nh cho há»c viĂªn

TĂ¬m trong code cĂ¡c marker:

```bash
grep -R "IMPLEMENTED" -n src tests docs
```

CĂ¡c pháº§n há»c viĂªn cáº§n tá»± lĂ m:

1. Implement LLM client.
2. Implement web/search client hoáº·c mock search source.
3. Implement routing decision trong Supervisor.
4. Implement tá»«ng worker agent.
5. Build LangGraph workflow.
6. ThĂªm tracing provider tháº­t: LangSmith, Langfuse hoáº·c OpenTelemetry.
7. Viáº¿t benchmark report.

## Deliverables

Há»c viĂªn ná»™p:

1. GitHub repo cĂ¡ nhĂ¢n.
2. Screenshot trace hoáº·c link trace.
3. `reports/benchmark_report.md` so sĂ¡nh single vs multi-agent.
4. Má»™t Ä‘oáº¡n giáº£i thĂ­ch failure mode vĂ  cĂ¡ch fix.

## References

- Anthropic: Building effective agents â€” https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK orchestration/handoffs â€” https://developers.openai.com/api/docs/guides/agents/orchestration
- LangGraph concepts â€” https://langchain-ai.github.io/langgraph/concepts/
- LangSmith tracing â€” https://docs.smith.langchain.com/
- Langfuse tracing â€” https://langfuse.com/docs
