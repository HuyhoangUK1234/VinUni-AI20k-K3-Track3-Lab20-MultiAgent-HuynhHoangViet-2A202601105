# BĂ¡o cĂ¡o triá»ƒn khai há»‡ thá»‘ng Multi-Agent Research

## 1. Tá»•ng quan

Dá»± Ă¡n xĂ¢y dá»±ng má»™t há»‡ thá»‘ng nghiĂªn cá»©u Ä‘a tĂ¡c tá»­ gá»“m bá»‘n vai trĂ² chĂ­nh:
Supervisor, Researcher, Analyst vĂ  Writer. Má»¥c tiĂªu cá»§a há»‡ thá»‘ng lĂ  nháº­n má»™t
cĂ¢u há»i nghiĂªn cá»©u, tĂ¬m nguá»“n dá»¯ liá»‡u liĂªn quan, phĂ¢n tĂ­ch thĂ´ng tin, sau Ä‘Ă³
viáº¿t cĂ¢u tráº£ lá»i cuá»‘i cĂ¹ng cĂ³ trĂ­ch dáº«n nguá»“n.

PhiĂªn báº£n hiá»‡n táº¡i Ä‘Ă£ thay tháº¿ cĂ¡c pháº§n skeleton `IMPLEMENTED` báº±ng má»™t luá»“ng
cháº¡y hoĂ n chá»‰nh. Há»‡ thá»‘ng cĂ³ thá»ƒ cháº¡y offline, khĂ´ng phá»¥ thuá»™c vĂ o API key, nhá»
vĂ o `LLMClient` fallback cá»¥c bá»™ vĂ  bá»™ dá»¯ liá»‡u mock trong thÆ° má»¥c
`ai_agent_offline_research_corpus_v2`.

## 2. Kiáº¿n trĂºc há»‡ thá»‘ng

Luá»“ng xá»­ lĂ½ chĂ­nh:

```text
User Query
   |
   v
Supervisor
   |
   +--> Researcher
   |
   +--> Analyst
   |
   +--> Writer
   |
   v
Final Answer + Trace
```

CĂ¡c thĂ nh pháº§n chĂ­nh:

- `SupervisorAgent`: quyáº¿t Ä‘á»‹nh agent nĂ o cháº¡y tiáº¿p dá»±a trĂªn tráº¡ng thĂ¡i hiá»‡n táº¡i.
- `ResearcherAgent`: truy xuáº¥t nguá»“n tá»« corpus offline vĂ  táº¡o ghi chĂº nghiĂªn cá»©u.
- `AnalystAgent`: phĂ¢n tĂ­ch ghi chĂº nghiĂªn cá»©u thĂ nh insight cĂ³ cáº¥u trĂºc.
- `WriterAgent`: tá»•ng há»£p cĂ¢u tráº£ lá»i cuá»‘i cĂ¹ng vĂ  thĂªm danh sĂ¡ch nguá»“n.
- `MultiAgentWorkflow`: Ä‘iá»u phá»‘i toĂ n bá»™ vĂ²ng cháº¡y.
- `SearchClient`: tĂ¬m kiáº¿m trong corpus offline.
- `LLMClient`: cung cáº¥p giao diá»‡n gá»i LLM, cĂ³ fallback offline.

## 3. Shared State

Há»‡ thá»‘ng sá»­ dá»¥ng `ResearchState` lĂ m tráº¡ng thĂ¡i dĂ¹ng chung giá»¯a cĂ¡c agent. ÄĂ¢y lĂ 
nguá»“n dá»¯ liá»‡u trung tĂ¢m Ä‘á»ƒ cĂ¡c agent Ä‘á»c, ghi vĂ  truyá»n thĂ´ng tin cho nhau.

CĂ¡c trÆ°á»ng quan trá»ng:

- `request`: cĂ¢u há»i nghiĂªn cá»©u ban Ä‘áº§u.
- `route_history`: lá»‹ch sá»­ cĂ¡c bÆ°á»›c Ä‘iá»u phá»‘i.
- `sources`: danh sĂ¡ch nguá»“n tĂ¬m Ä‘Æ°á»£c.
- `research_notes`: ghi chĂº cá»§a Researcher.
- `analysis_notes`: phĂ¢n tĂ­ch cá»§a Analyst.
- `final_answer`: cĂ¢u tráº£ lá»i cuá»‘i cĂ¹ng cá»§a Writer.
- `agent_results`: káº¿t quáº£ chi tiáº¿t cá»§a tá»«ng agent.
- `trace`: sá»± kiá»‡n trace phá»¥c vá»¥ debug.
- `errors`: danh sĂ¡ch lá»—i hoáº·c cáº£nh bĂ¡o khi cháº¡y workflow.

Thiáº¿t káº¿ nĂ y giĂºp viá»‡c handoff giá»¯a cĂ¡c agent rĂµ rĂ ng hÆ¡n, trĂ¡nh phá»¥ thuá»™c vĂ o
transcript tá»± do vĂ  há»— trá»£ benchmark/debug dá»… hÆ¡n.

## 4. CĂ¡ch triá»ƒn khai tá»«ng agent

### Supervisor

Supervisor Ä‘Ă³ng vai trĂ² router. Agent nĂ y kiá»ƒm tra cĂ¡c trÆ°á»ng cĂ²n thiáº¿u trong
`ResearchState` Ä‘á»ƒ quyáº¿t Ä‘á»‹nh bÆ°á»›c tiáº¿p theo:

- ChÆ°a cĂ³ `research_notes` thĂ¬ chuyá»ƒn sang `researcher`.
- ÄĂ£ cĂ³ nghiĂªn cá»©u nhÆ°ng chÆ°a cĂ³ `analysis_notes` thĂ¬ chuyá»ƒn sang `analyst`.
- ÄĂ£ cĂ³ phĂ¢n tĂ­ch nhÆ°ng chÆ°a cĂ³ `final_answer` thĂ¬ chuyá»ƒn sang `writer`.
- Khi Ä‘Ă£ cĂ³ cĂ¢u tráº£ lá»i cuá»‘i cĂ¹ng thĂ¬ chuyá»ƒn sang `done`.

Supervisor cÅ©ng kiá»ƒm soĂ¡t `max_iterations` Ä‘á»ƒ trĂ¡nh workflow cháº¡y vĂ´ háº¡n.

### Researcher

Researcher dĂ¹ng `SearchClient` Ä‘á»ƒ tĂ¬m cĂ¡c nguá»“n liĂªn quan Ä‘áº¿n query. Trong phiĂªn
báº£n hiá»‡n táº¡i, nguá»“n Ä‘Æ°á»£c láº¥y tá»« thÆ° má»¥c `ai_agent_offline_research_corpus_v2`.

SearchClient Ä‘á»c cĂ¡c file JSON trong `topics/`, sau Ä‘Ă³ index:

- `knowledge_articles`
- `source_documents`

Má»—i káº¿t quáº£ Ä‘Æ°á»£c chuáº©n hĂ³a thĂ nh `SourceDocument`, gá»“m tiĂªu Ä‘á», URL ná»™i bá»™,
snippet vĂ  metadata. VĂ­ dá»¥ URL nguá»“n:

```text
offline-corpus://AIAGENT-01:A04
```

### Analyst

Analyst Ä‘á»c `research_notes` vĂ  táº¡o `analysis_notes`. Vai trĂ² cá»§a agent nĂ y lĂ 
rĂºt ra cĂ¡c Ä‘iá»ƒm chĂ­nh, nháº­n diá»‡n thĂ´ng tin quan trá»ng vĂ  chuáº©n bá»‹ Ä‘áº§u vĂ o tá»‘t
hÆ¡n cho Writer.

Náº¿u thiáº¿u `research_notes`, Analyst sáº½ ghi cáº£nh bĂ¡o vĂ o `state.errors` thay vĂ¬
lĂ m workflow bá»‹ crash.

### Writer

Writer Ä‘á»c query gá»‘c, research notes, analysis notes vĂ  danh sĂ¡ch nguá»“n. Agent
nĂ y táº¡o `final_answer` vĂ  thĂªm pháº§n `Sources` á»Ÿ cuá»‘i Ä‘á»ƒ Ä‘áº£m báº£o cĂ¢u tráº£ lá»i cĂ³
truy xuáº¥t nguá»“n rĂµ rĂ ng.

## 5. Corpus offline

Bá»™ dá»¯ liá»‡u mock náº±m trong:

```text
ai_agent_offline_research_corpus_v2
```

Corpus nĂ y gá»“m 30 topic vá» AI agents vĂ  multi-agent systems. Má»—i topic cĂ³:

- bĂ i viáº¿t kiáº¿n thá»©c dĂ i;
- source documents;
- fact bank;
- failure modes;
- case studies;
- data tables;
- glossary;
- rubric Ä‘Ă¡nh giĂ¡.

Viá»‡c dĂ¹ng corpus offline giĂºp benchmark á»•n Ä‘á»‹nh hÆ¡n vĂ¬ khĂ´ng phá»¥ thuá»™c internet,
khĂ´ng bá»‹ thay Ä‘á»•i káº¿t quáº£ do search engine, vĂ  dá»… tĂ¡i láº­p trong mĂ´i trÆ°á»ng lab.

## 6. LLM Client

`LLMClient` Ä‘Æ°á»£c thiáº¿t káº¿ theo hÆ°á»›ng provider-agnostic. Agent khĂ´ng gá»i trá»±c tiáº¿p
OpenAI SDK mĂ  gá»i qua `LLMClient.complete()`.

Máº·c Ä‘á»‹nh há»‡ thá»‘ng dĂ¹ng fallback offline Ä‘á»ƒ Ä‘áº£m báº£o cháº¡y Ä‘Æ°á»£c ngay cáº£ khi khĂ´ng
cĂ³ API key. Náº¿u muá»‘n dĂ¹ng LLM tháº­t, cĂ³ thá»ƒ báº­t:

```text
USE_LIVE_LLM=true
OPENAI_API_KEY=...
```

CĂ¡ch nĂ y giĂºp repo phĂ¹ há»£p cáº£ hai tĂ¬nh huá»‘ng:

- cháº¡y lab offline báº±ng mock data;
- nĂ¢ng cáº¥p sang provider tháº­t khi cáº§n demo cháº¥t lÆ°á»£ng cao hÆ¡n.

## 7. Benchmark vĂ  kiá»ƒm thá»­

CĂ¡c kiá»ƒm tra Ä‘Ă£ cháº¡y:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

Káº¿t quáº£:

```text
5 passed
```

Kiá»ƒm tra lint:

```powershell
$env:RUFF_CACHE_DIR='C:\Users\thanh\AppData\Local\Temp\ruff-cache-malab'
.\.venv\Scripts\python.exe -m ruff check src tests
```

Káº¿t quáº£:

```text
All checks passed!
```

Kiá»ƒm tra type:

```powershell
.\.venv\Scripts\python.exe -m mypy src --cache-dir C:\Users\thanh\AppData\Local\Temp\mypy-cache-malab
```

Káº¿t quáº£:

```text
Success: no issues found in 28 source files
```

## 8. Káº¿t quáº£ cháº¡y thá»­

Lá»‡nh cháº¡y thá»­:

```powershell
.\.venv\Scripts\python.exe -m multi_agent_research_lab.cli multi-agent --query "Compare single-agent and multi-agent architectures for complex research tasks"
```

Workflow tráº£ vá» route history:

```text
researcher -> analyst -> writer -> done
```

Káº¿t quáº£ cho tháº¥y há»‡ thá»‘ng Ä‘Ă£:

- tĂ¬m Ä‘Æ°á»£c nguá»“n tá»« offline corpus;
- táº¡o research notes;
- táº¡o analysis notes;
- táº¡o final answer;
- ghi trace cho tá»«ng bÆ°á»›c;
- khĂ´ng phĂ¡t sinh lá»—i trong `state.errors`.

## 9. Failure modes vĂ  cĂ¡ch xá»­ lĂ½

### Failure mode 1: Workflow cháº¡y vĂ´ háº¡n

Nguy cÆ¡: Supervisor cĂ³ thá»ƒ Ä‘iá»u phá»‘i láº·p láº¡i náº¿u state khĂ´ng Ä‘Æ°á»£c cáº­p nháº­t Ä‘Ăºng.

CĂ¡ch xá»­ lĂ½: thĂªm `max_iterations` trong config vĂ  Supervisor sáº½ dá»«ng workflow khi
vÆ°á»£t quĂ¡ giá»›i háº¡n.

### Failure mode 2: KhĂ´ng cĂ³ API key hoáº·c khĂ´ng gá»i Ä‘Æ°á»£c OpenAI

Nguy cÆ¡: há»‡ thá»‘ng bá»‹ lá»—i khi cháº¡y trong mĂ´i trÆ°á»ng lab offline.

CĂ¡ch xá»­ lĂ½: `LLMClient` máº·c Ä‘á»‹nh dĂ¹ng fallback offline. Chá»‰ khi báº­t
`USE_LIVE_LLM=true` thĂ¬ má»›i gá»i OpenAI.

### Failure mode 3: Nguá»“n tĂ¬m kiáº¿m khĂ´ng á»•n Ä‘á»‹nh

Nguy cÆ¡: náº¿u dĂ¹ng web search tháº­t, káº¿t quáº£ cĂ³ thá»ƒ thay Ä‘á»•i theo thá»i gian.

CĂ¡ch xá»­ lĂ½: dĂ¹ng corpus offline Ä‘á»ƒ benchmark cĂ³ tĂ­nh tĂ¡i láº­p.

### Failure mode 4: Citation khĂ´ng rĂµ rĂ ng

Nguy cÆ¡: Writer táº¡o cĂ¢u tráº£ lá»i nhÆ°ng khĂ´ng chá»‰ ra nguá»“n.

CĂ¡ch xá»­ lĂ½: Writer luĂ´n thĂªm danh sĂ¡ch `Sources` dá»±a trĂªn `state.sources`, cĂ²n
metadata lÆ°u `citation_id` cá»§a corpus.

## 10. Káº¿t luáº­n

Há»‡ thá»‘ng hiá»‡n táº¡i Ä‘Ă£ chuyá»ƒn tá»« skeleton sang má»™t workflow multi-agent cĂ³ thá»ƒ cháº¡y
end-to-end. Thiáº¿t káº¿ tĂ¡ch rĂµ vai trĂ² agent, service layer, shared state,
workflow orchestration, tracing vĂ  benchmark. PhiĂªn báº£n nĂ y phĂ¹ há»£p Ä‘á»ƒ demo lab,
kiá»ƒm thá»­ offline vĂ  lĂ m ná»n Ä‘á»ƒ nĂ¢ng cáº¥p sang LLM/search provider tháº­t.

CĂ¡c hÆ°á»›ng cáº£i tiáº¿n tiáº¿p theo:

- nĂ¢ng cháº¥t lÆ°á»£ng fallback local Ä‘á»ƒ tĂ³m táº¯t sĂ¡t ná»™i dung corpus hÆ¡n;
- thĂªm Critic vĂ o workflow chĂ­nh;
- sinh bĂ¡o cĂ¡o benchmark tá»± Ä‘á»™ng vĂ o `reports/`;
- há»— trá»£ chá»n topic corpus cá»¥ thá»ƒ báº±ng CLI option;
- thĂªm citation audit Ä‘á»ƒ kiá»ƒm tra tá»«ng claim cĂ³ nguá»“n phĂ¹ há»£p.
