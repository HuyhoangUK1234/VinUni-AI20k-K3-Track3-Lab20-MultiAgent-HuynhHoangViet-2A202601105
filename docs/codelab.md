---
title: "Multi-Agent Research System: Supervisor, Researcher, Analyst, Writer"
description: "XĂ¢y dá»±ng há»‡ thá»‘ng nghiĂªn cá»©u multi-agent vá»›i LangGraph, so sĂ¡nh vá»›i single-agent baseline qua benchmark latency/cost/quality."
author: "VinUni Codelab"
duration: 240
category: "General"
updated: "2026-08-20"
day: "20"
sequence: 1
keywords: ["AI", "Multi-Agent", "LangGraph", "LLM", "Agents", "Benchmark"]
level: "intermediate"
requiresSubmission: true
workMode: "individual"
overview:
  summary: "Báº¡n sáº½ xĂ¢y dá»±ng má»™t research assistant gá»“m nhiá»u agent (Supervisor Ä‘iá»u phá»‘i Researcher, Analyst, Writer) trĂªn ná»n LangGraph, sau Ä‘Ă³ benchmark há»‡ thá»‘ng nĂ y vá»›i má»™t single-agent baseline Ä‘á»ƒ tráº£ lá»i cĂ¢u há»i: khi nĂ o multi-agent thá»±c sá»± Ä‘Ă¡ng dĂ¹ng?"
  knowledge:
    - "Python cÆ¡ báº£n (function, class, type hints)"
    - "ÄĂ£ tá»«ng gá»i LLM API (OpenAI hoáº·c tÆ°Æ¡ng Ä‘Æ°Æ¡ng)"
    - "Hiá»ƒu khĂ¡i niá»‡m prompt vĂ  structured output"
    - "Biáº¿t dĂ¹ng git, terminal, virtualenv"
  conceptFlow:
    - "Single-agent baseline: má»™t agent lĂ m táº¥t cáº£ â€” nhanh nhÆ°ng dá»… loĂ£ng context"
    - "TĂ¡ch vai trĂ²: Researcher tĂ¬m nguá»“n, Analyst phĂ¢n tĂ­ch, Writer tá»•ng há»£p"
    - "Supervisor/Router: quyáº¿t Ä‘á»‹nh gá»i agent nĂ o, khi nĂ o dá»«ng"
    - "Shared state: nguá»“n thĂ´ng tin duy nháº¥t truyá»n qua cĂ¡c agent"
    - "Guardrails: max iterations, timeout, retry Ä‘á»ƒ agent khĂ´ng cháº¡y vĂ´ háº¡n"
    - "Trace + Benchmark: Ä‘o latency/cost/quality thay vĂ¬ nhĂ¬n output báº±ng cáº£m tĂ­nh"
  phases:
    - time: "0-30'"
      owner: "Há»c viĂªn"
      title: "Setup & Baseline"
      description: "CĂ i mĂ´i trÆ°á»ng, cháº¡y skeleton, implement LLM client vĂ  single-agent baseline."
    - time: "30-90'"
      owner: "Há»c viĂªn"
      title: "Supervisor & Workflow"
      description: "Implement routing policy trong Supervisor vĂ  build LangGraph workflow vá»›i stop condition."
    - time: "90-150'"
      owner: "Há»c viĂªn"
      title: "Worker Agents"
      description: "Implement Researcher (search), Analyst (phĂ¢n tĂ­ch), Writer (tá»•ng há»£p) vá»›i shared state."
    - time: "150-210'"
      owner: "Há»c viĂªn"
      title: "Trace & Benchmark"
      description: "Gáº¯n tracing (LangSmith/Langfuse), cháº¡y benchmark single vs multi-agent, viáº¿t report."
    - time: "210-240'"
      owner: "Cáº£ lá»›p"
      title: "Peer Review & Exit Ticket"
      description: "Review chĂ©o theo rubric, tráº£ lá»i cĂ¢u há»i khi nĂ o nĂªn/khĂ´ng nĂªn dĂ¹ng multi-agent."
  outcomes:
    - "Thiáº¿t káº¿ Ä‘Æ°á»£c role rĂµ rĂ ng cho nhiá»u agent, khĂ´ng overlap"
    - "XĂ¢y dá»±ng shared state Ä‘á»§ thĂ´ng tin cho handoff giá»¯a cĂ¡c agent"
    - "ThĂªm guardrail tá»‘i thiá»ƒu: max iterations, timeout, retry/fallback, validation"
    - "Trace Ä‘Æ°á»£c luá»“ng cháº¡y vĂ  giáº£i thĂ­ch agent nĂ o lĂ m gĂ¬, tá»‘n bao nhiĂªu"
    - "Benchmark single-agent vs multi-agent theo quality, latency, cost"
  reassurance: "Starter repo Ä‘Ă£ cĂ³ sáºµn khung production-grade (config, schema, test, CI). Báº¡n chá»‰ cáº§n Ä‘iá»n logic vĂ o cĂ¡c Ä‘iá»ƒm IMPLEMENTED â€” má»—i Ä‘iá»ƒm Ä‘á»u cĂ³ docstring hÆ°á»›ng dáº«n, vĂ  test sáº½ bĂ¡o rĂµ khi báº¡n hoĂ n thĂ nh Ä‘Ăºng."
---

## Kiáº¿n trĂºc tá»•ng thá»ƒ

Hai cĂ¡ch lĂ m báº¡n sáº½ so sĂ¡nh trong lab:

```mermaid
flowchart LR
    subgraph A["Single-agent baseline"]
        Q1([User Query]) --> S1["Má»™t agent lĂ m táº¥t cáº£:<br/>search + phĂ¢n tĂ­ch + viáº¿t"]
        S1 --> A1([Answer])
    end

    subgraph B["Multi-agent workflow"]
        Q2([User Query]) --> SUP{{"Supervisor<br/>(Router)"}}
        SUP -->|"chÆ°a cĂ³ sources"| R["Researcher<br/>â†’ sources, research_notes"]
        SUP -->|"chÆ°a cĂ³ analysis"| AN["Analyst<br/>â†’ analysis_notes"]
        SUP -->|"Ä‘á»§ dá»¯ liá»‡u"| W["Writer<br/>â†’ final_answer"]
        R --> SUP
        AN --> SUP
        W --> DONE([Answer + Trace])
        SUP -->|"max_iterations"| STOP([Stop guardrail])
    end
```

Luá»“ng má»™t láº§n cháº¡y multi-agent Ä‘iá»ƒn hĂ¬nh (shared state chuyá»n qua tá»«ng bÆ°á»›c):

```mermaid
flowchart TD
    U([User gá»­i query]) --> S1{{"Supervisor kiá»ƒm tra state<br/>â†’ chÆ°a cĂ³ sources"}}
    S1 -->|route| R["Researcher<br/>search + tá»•ng há»£p nguá»“n<br/>ghi vĂ o state: sources, research_notes"]
    R --> S2{{"Supervisor kiá»ƒm tra state<br/>â†’ chÆ°a cĂ³ analysis_notes"}}
    S2 -->|route| A["Analyst<br/>Ä‘á»c research_notes, Ä‘Ă¡nh giĂ¡ nguá»“n<br/>ghi vĂ o state: analysis_notes"]
    A --> S3{{"Supervisor kiá»ƒm tra state<br/>â†’ Ä‘á»§ dá»¯ liá»‡u Ä‘á»ƒ viáº¿t"}}
    S3 -->|route| W["Writer<br/>tá»•ng há»£p thĂ nh final_answer<br/>kĂ¨m citations trá» vá» sources"]
    W --> DONE([Tráº£ final_answer cho User])

    T["Má»—i bÆ°á»›c Ä‘á»u ghi vĂ o<br/>route_history + trace"]
    S1 -.-> T
    S2 -.-> T
    S3 -.-> T

    style T fill:#fff3bf,stroke:#e6b800
```

## 1. Thuáº­t ngá»¯ cáº§n biáº¿t

| Thuáº­t ngá»¯ gá»‘c | Báº£n cháº¥t khĂ¡i niá»‡m | Minh hoáº¡ trá»±c quan |
| --- | --- | --- |
| Agent | Má»™t "nhĂ¢n viĂªn" LLM cĂ³ vai trĂ², prompt vĂ  cĂ´ng cá»¥ riĂªng, nháº­n input tá»« state vĂ  tráº£ output cĂ³ cáº¥u trĂºc | Researcher nhÆ° thá»±c táº­p sinh chuyĂªn Ä‘i tĂ¬m tĂ i liá»‡u; Writer nhÆ° biĂªn táº­p viĂªn chá»‰ lo viáº¿t |
| Supervisor / Router | Agent Ä‘iá»u phá»‘i: nhĂ¬n state hiá»‡n táº¡i vĂ  quyáº¿t Ä‘á»‹nh bÆ°á»›c tiáº¿p theo lĂ  gá»i ai hoáº·c dá»«ng | TrÆ°á»Ÿng nhĂ³m Ä‘á»©ng báº£ng phĂ¢n cĂ´ng: "chÆ°a cĂ³ nguá»“n â†’ gá»i Researcher; Ä‘á»§ phĂ¢n tĂ­ch â†’ gá»i Writer" |
| Shared state | Cáº¥u trĂºc dá»¯ liá»‡u duy nháº¥t Ä‘Æ°á»£c truyá»n qua má»i agent, chá»©a toĂ n bá»™ ngá»¯ cáº£nh cá»§a phiĂªn lĂ m viá»‡c | Tá» há»“ sÆ¡ vá»¥ viá»‡c chuyá»n tay trong vÄƒn phĂ²ng â€” ai lĂ m xong pháº§n mĂ¬nh thĂ¬ ghi thĂªm vĂ o |
| Handoff | Viá»‡c má»™t agent hoĂ n thĂ nh vĂ  chuyá»ƒn quyá»n xá»­ lĂ½ (kĂ¨m state) cho agent khĂ¡c | Researcher ná»™p `research_notes` vĂ o há»“ sÆ¡ rá»“i chuyá»ƒn bĂ n cho Analyst |
| LangGraph | Framework xĂ¢y workflow dáº¡ng Ä‘á»“ thá»‹: node lĂ  agent, edge lĂ  luá»“ng chuyá»ƒn, cĂ³ conditional routing | SÆ¡ Ä‘á»“ dĂ¢y chuyá»n sáº£n xuáº¥t: má»—i tráº¡m má»™t viá»‡c, cĂ³ nhĂ¡nh ráº½ tĂ¹y tĂ¬nh tráº¡ng sáº£n pháº©m |
| Guardrail | CÆ¡ cháº¿ cháº·n agent cháº¡y sai/vĂ´ háº¡n: max iterations, timeout, retry, validation | Cáº§u dao tá»± ngáº¯t â€” vĂ²ng láº·p Supervisorâ†”Researcher quĂ¡ 6 láº§n thĂ¬ há»‡ thá»‘ng dá»«ng, khĂ´ng Ä‘á»‘t token vĂ´ Ă­ch |
| Trace | Báº£n ghi tá»«ng bÆ°á»›c cháº¡y: agent nĂ o Ä‘Æ°á»£c gá»i, input/output gĂ¬, tá»‘n bao nhiĂªu token/thá»i gian | Há»™p Ä‘en mĂ¡y bay â€” khi káº¿t quáº£ sai, má»Ÿ trace ra xem sai tá»« bÆ°á»›c nĂ o |
| Benchmark | So sĂ¡nh cĂ³ sá»‘ liá»‡u giá»¯a cĂ¡c cĂ¡ch lĂ m (latency, cost, quality) thay vĂ¬ cáº£m tĂ­nh | Äua hai Ä‘á»™i cĂ¹ng Ä‘á» bĂ i, cháº¥m báº±ng Ä‘á»“ng há»“ + hĂ³a Ä‘Æ¡n token + rubric, khĂ´ng cháº¥m báº±ng "trĂ´ng cĂ³ váº» hay" |

## 2. Má»¥c tiĂªu & Ä‘áº§u ra

Báº¡n hoĂ n thĂ nh khi:

1. `python -m multi_agent_research_lab.cli baseline --query "..."` tráº£ vá» cĂ¢u tráº£ lá»i tháº­t tá»« LLM (khĂ´ng cĂ²n placeholder).
2. `python -m multi_agent_research_lab.cli multi-agent --query "..."` cháº¡y háº¿t workflow Supervisor â†’ Researcher â†’ Analyst â†’ Writer vĂ  in ra `final_answer` kĂ¨m `route_history`.
3. CĂ³ trace xem Ä‘Æ°á»£c (LangSmith/Langfuse screenshot hoáº·c link) cho Ă­t nháº¥t 1 láº§n cháº¡y multi-agent.
4. CĂ³ file `reports/benchmark_report.md` so sĂ¡nh single vs multi-agent vá»›i Ă­t nháº¥t 3 metric: latency, cost, quality.
5. `make lint` vĂ  `make test` pass; khĂ´ng cĂ²n `implementation marker` khi cháº¡y cĂ¡c lá»‡nh trĂªn.

## 3. Chuáº©n bá»‹

**CĂ´ng cá»¥:**

- Python 3.11+ (khuyáº¿n nghá»‹ 3.12), `git`, terminal (macOS/Linux/WSL).
- Editor cĂ³ Python support (VS Code / Kiro / PyCharm).

**API keys (Ä‘iá»n vĂ o `.env`):**

- `OPENAI_API_KEY` â€” báº¯t buá»™c (hoáº·c provider tÆ°Æ¡ng Ä‘Æ°Æ¡ng, tá»± Ä‘iá»u chá»‰nh `llm_client.py`).
- `TAVILY_API_KEY` â€” tĂ¹y chá»n; náº¿u khĂ´ng cĂ³, implement mock search trong `services/search_client.py`.
- `LANGSMITH_API_KEY` hoáº·c `LANGFUSE_*` â€” tĂ¹y chá»n cho tracing (khuyáº¿n nghá»‹ cĂ³ Ă­t nháº¥t má»™t).

**Setup mĂ´i trÆ°á»ng:**

```bash
git clone https://github.com/VinUni-AI20k/VinUni-AI20k-K3-Track3-Lab20-MultiAgent.git
cd VinUni-AI20k-K3-Track3-Lab20-MultiAgent
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,llm]"
cp .env.example .env   # rá»“i Ä‘iá»n API keys
make test              # 4 tests pháº£i pass ngay tá»« Ä‘áº§u
```

> **macOS lÆ°u Ă½:** náº¿u gáº·p `SSLCertVerificationError` khi gá»i API, xem má»¥c Troubleshooting trong `docs/lab_guide.md` (fix báº±ng `certifi` hoáº·c `Install Certificates.command`).

## 4. Thá»±c hĂ nh

TĂ¬m toĂ n bá»™ Ä‘iá»ƒm cáº§n lĂ m báº±ng: `grep -R "IMPLEMENTED" -n src tests docs`

### BÆ°á»›c 1 â€” LLM client & Baseline (0-30')

- Implement `services/llm_client.py`: gá»i LLM tháº­t, tráº£ structured output.
- Sá»­a command `baseline` trong `cli.py`: thay placeholder báº±ng má»™t call LLM end-to-end.
- **Káº¿t quáº£ mong Ä‘á»£i:** cháº¡y `make run-baseline` in ra cĂ¢u tráº£ lá»i tháº­t, ghi láº¡i latency vĂ  token usage Ä‘á»ƒ so sĂ¡nh sau.

### BÆ°á»›c 2 â€” Supervisor & Workflow (30-90')

- Implement routing policy trong `agents/supervisor.py`: dá»±a vĂ o state (Ä‘Ă£ cĂ³ `sources`? Ä‘Ă£ cĂ³ `analysis_notes`?) Ä‘á»ƒ quyáº¿t Ä‘á»‹nh route tiáº¿p theo.
- Implement `graph/workflow.py`: build LangGraph vá»›i cĂ¡c node supervisor/researcher/analyst/writer, conditional edges, vĂ  stop condition (dĂ¹ng `max_iterations` tá»« config).
- **Káº¿t quáº£ mong Ä‘á»£i:** `make run-multi` khĂ´ng cĂ²n bĂ¡o `implementation marker` á»Ÿ workflow; `route_history` trong output thá»ƒ hiá»‡n Ä‘Ăºng thá»© tá»± routing.

### BÆ°á»›c 3 â€” Worker agents (90-150')

- `agents/researcher.py`: gá»i `SearchClient` (Tavily hoáº·c mock), ghi `sources` + `research_notes` vĂ o state.
- `agents/analyst.py`: Ä‘á»c `research_notes`, sinh `analysis_notes` (so sĂ¡nh, Ä‘Ă¡nh giĂ¡ Ä‘á»™ tin cáº­y nguá»“n).
- `agents/writer.py`: tá»•ng há»£p thĂ nh `final_answer` cĂ³ citation trá» vá» `sources`.
- **Káº¿t quáº£ mong Ä‘á»£i:** cháº¡y end-to-end ra `final_answer` cĂ³ trĂ­ch dáº«n; state chá»©a Ä‘á»§ dá»¯ liá»‡u trung gian Ä‘á»ƒ debug.

### BÆ°á»›c 4 â€” Trace & Benchmark (150-210')

- Implement `observability/tracing.py` vá»›i LangSmith/Langfuse (hoáº·c OpenTelemetry).
- Implement `evaluation/benchmark.py` + `evaluation/report.py`: cháº¡y cĂ¹ng bá»™ query qua cáº£ baseline vĂ  multi-agent, Ä‘o latency/cost/quality/citation coverage/failure rate.
- Viáº¿t `reports/benchmark_report.md`.
- **Káº¿t quáº£ mong Ä‘á»£i:** má»Ÿ Ä‘Æ°á»£c trace UI tháº¥y tá»«ng agent step; report cĂ³ báº£ng sá»‘ liá»‡u so sĂ¡nh vĂ  1 Ä‘oáº¡n phĂ¢n tĂ­ch failure mode.

### BÆ°á»›c 5 â€” Peer review & Exit ticket (210-240')

- Review chĂ©o theo `docs/peer_review_rubric.md` (5 tiĂªu chĂ­ Ă— 0-2 Ä‘iá»ƒm).
- Tráº£ lá»i exit ticket trong `docs/lab_guide.md`: case nĂ o nĂªn / khĂ´ng nĂªn dĂ¹ng multi-agent, vĂ¬ sao.

## 5. Kiá»ƒm tra káº¿t quáº£

**Tá»± kiá»ƒm tra:**

```bash
make lint        # ruff: pháº£i "All checks passed!"
make test        # pytest: táº¥t cáº£ pass
make run-baseline
make run-multi   # khĂ´ng cĂ²n panel "Expected TODO"
grep -R "IMPLEMENTED" -n src | wc -l   # cĂ¡c TODO cá»‘t lĂµi Ä‘Ă£ Ä‘Æ°á»£c thay báº±ng implementation
```

**Lá»—i thÆ°á»ng gáº·p:**

| Lá»—i | NguyĂªn nhĂ¢n | CĂ¡ch xá»­ lĂ½ |
| --- | --- | --- |
| `implementation marker: implement MultiAgentWorkflow.run` | ChÆ°a implement workflow â€” Ä‘Ă¢y lĂ  hĂ nh vi máº·c Ä‘á»‹nh cá»§a starter | LĂ m BÆ°á»›c 2 |
| `SSLCertVerificationError` trĂªn macOS | Python khĂ´ng tĂ¬m tháº¥y CA bundle cá»§a há»‡ Ä‘iá»u hĂ nh | Xem Troubleshooting trong `docs/lab_guide.md`: dĂ¹ng `certifi` hoáº·c cháº¡y `Install Certificates.command` |
| Workflow láº·p vĂ´ háº¡n Supervisor â†” Researcher | Thiáº¿u stop condition / khĂ´ng tÄƒng `iteration` | DĂ¹ng `state.record_route()` vĂ  check `max_iterations` tá»« `Settings` |
| `401 Unauthorized` khi gá»i LLM | ChÆ°a Ä‘iá»n key vĂ o `.env` hoáº·c chÆ°a `cp .env.example .env` | Kiá»ƒm tra `.env`, khĂ´ng hard-code key trong code |
| Output multi-agent kĂ©m hÆ¡n baseline | BĂ¬nh thÆ°á»ng! Multi-agent khĂ´ng pháº£i lĂºc nĂ o cÅ©ng tháº¯ng | Ghi nháº­n vĂ o benchmark report vĂ  phĂ¢n tĂ­ch trade-off â€” Ä‘Ă¢y chĂ­nh lĂ  learning outcome |

## 6. Ná»™p bĂ i

Artefact cáº§n ná»™p:

1. **Link GitHub repo cĂ¡ nhĂ¢n** â€” code hoĂ n chá»‰nh, `make lint` + `make test` pass, khĂ´ng cĂ²n `implementation marker` á»Ÿ luá»“ng chĂ­nh.
2. **Trace evidence** â€” screenshot hoáº·c link LangSmith/Langfuse cá»§a Ă­t nháº¥t 1 láº§n cháº¡y multi-agent end-to-end.
3. **`reports/benchmark_report.md`** â€” báº£ng so sĂ¡nh single vs multi-agent (tá»‘i thiá»ƒu: latency, cost, quality) + 1 Ä‘oáº¡n giáº£i thĂ­ch failure mode gáº·p pháº£i vĂ  cĂ¡ch fix.
4. **Exit ticket** â€” tráº£ lá»i 2 cĂ¢u há»i trong `docs/lab_guide.md` (khi nĂ o nĂªn / khĂ´ng nĂªn dĂ¹ng multi-agent).
