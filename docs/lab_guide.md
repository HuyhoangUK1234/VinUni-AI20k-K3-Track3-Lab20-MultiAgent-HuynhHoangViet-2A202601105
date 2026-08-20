# Lab Guide: Multi-Agent Research System

## Scenario

Báº¡n cáº§n xĂ¢y dá»±ng má»™t research assistant cĂ³ thá»ƒ nháº­n cĂ¢u há»i dĂ i, tĂ¬m thĂ´ng tin, phĂ¢n tĂ­ch vĂ  viáº¿t cĂ¢u tráº£ lá»i cuá»‘i cĂ¹ng. Lab yĂªu cáº§u so sĂ¡nh hai cĂ¡ch lĂ m:

1. **Single-agent baseline**: má»™t agent lĂ m toĂ n bá»™.
2. **Multi-agent workflow**: Supervisor Ä‘iá»u phá»‘i Researcher, Analyst, Writer.

## Quy táº¯c quan trá»ng

- KhĂ´ng thĂªm agent náº¿u khĂ´ng cĂ³ lĂ½ do rĂµ rĂ ng.
- Má»—i agent pháº£i cĂ³ responsibility riĂªng.
- Shared state pháº£i Ä‘á»§ rĂµ Ä‘á»ƒ debug.
- Pháº£i cĂ³ trace hoáº·c log cho tá»«ng bÆ°á»›c.
- Pháº£i benchmark, khĂ´ng chá»‰ nhĂ¬n output báº±ng cáº£m tĂ­nh.

## Milestone 1: Baseline

File gá»£i Ă½:

- `src/multi_agent_research_lab/cli.py`
- `src/multi_agent_research_lab/services/llm_client.py`

IMPLEMENTED: thay baseline placeholder báº±ng má»™t call LLM tháº­t.

## Milestone 2: Supervisor

File gá»£i Ă½:

- `src/multi_agent_research_lab/agents/supervisor.py`
- `src/multi_agent_research_lab/graph/workflow.py`

IMPLEMENTED: implement routing policy.

Gá»£i Ă½ cĂ¢u há»i thiáº¿t káº¿:

- Khi nĂ o gá»i Researcher?
- Khi nĂ o gá»i Analyst?
- Khi nĂ o gá»i Writer?
- Khi nĂ o stop?
- Náº¿u agent fail thĂ¬ retry hay fallback?

## Milestone 3: Worker agents

File gá»£i Ă½:

- `src/multi_agent_research_lab/agents/researcher.py`
- `src/multi_agent_research_lab/agents/analyst.py`
- `src/multi_agent_research_lab/agents/writer.py`

IMPLEMENTED: implement tá»«ng worker.

## Milestone 4: Trace vĂ  benchmark

File gá»£i Ă½:

- `src/multi_agent_research_lab/observability/tracing.py`
- `src/multi_agent_research_lab/evaluation/benchmark.py`
- `src/multi_agent_research_lab/evaluation/report.py`

Benchmark tá»‘i thiá»ƒu:

| Metric | CĂ¡ch Ä‘o gá»£i Ă½ |
|---|---|
| Latency | wall-clock time |
| Cost | token usage hoáº·c provider usage |
| Quality | rubric 0-10 do peer review |
| Citation coverage | sá»‘ claims cĂ³ source / tá»•ng claims chĂ­nh |
| Failure rate | sá»‘ query fail / tá»•ng query |

## Troubleshooting

### macOS: lá»—i SSL certificate khi gá»i API qua HTTPS (Tavily, OpenAI, ...)

Triá»‡u chá»©ng: khi implement `SearchClient` (hoáº·c báº¥t ká»³ HTTPS call nĂ o) trĂªn macOS, báº¡n cĂ³ thá»ƒ gáº·p lá»—i kiá»ƒu:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
unable to get local issuer certificate
```

NguyĂªn nhĂ¢n: Python cĂ i tá»« python.org trĂªn macOS **khĂ´ng dĂ¹ng** certificate store cá»§a há»‡ Ä‘iá»u hĂ nh, nĂªn khĂ´ng tĂ¬m tháº¥y CA bundle há»£p lá»‡. ÄĂ¢y lĂ  lá»—i mĂ´i trÆ°á»ng, **khĂ´ng pháº£i** do API key sai.

CĂ¡ch kháº¯c phá»¥c (chá»n 1 trong 3):

1. **Cháº¡y script cĂ i certificate Ä‘i kĂ¨m Python** (nhanh nháº¥t):

   ```bash
   /Applications/Python\ 3.12/Install\ Certificates.command
   ```

   (thay `3.12` báº±ng version Python cá»§a báº¡n)

2. **DĂ¹ng `certifi` trong code** â€” thĂªm `certifi` vĂ o dependencies, rá»“i táº¡o SSL context khi gá»i HTTPS:

   ```python
   import certifi
   import ssl
   from urllib.request import urlopen

   ssl_context = ssl.create_default_context(cafile=certifi.where())
   urlopen(request, timeout=timeout, context=ssl_context)
   ```

3. **Set biáº¿n mĂ´i trÆ°á»ng** trá» tá»›i CA bundle cá»§a certifi (khĂ´ng cáº§n Ä‘á»•i code):

   ```bash
   export SSL_CERT_FILE=$(python -m certifi)
   ```

## Exit ticket

Má»—i nhĂ³m tráº£ lá»i 2 cĂ¢u:

1. Case nĂ o nĂªn dĂ¹ng multi-agent? VĂ¬ sao?
2. Case nĂ o khĂ´ng nĂªn dĂ¹ng multi-agent? VĂ¬ sao?
