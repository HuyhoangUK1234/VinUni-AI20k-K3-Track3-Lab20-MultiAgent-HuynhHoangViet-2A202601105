# Design Template

## Problem

Hệ thống cần xử lý các câu hỏi nghiên cứu về AI agents và multi-agent systems. Đầu ra mong muốn là một câu trả lời có cấu trúc, có phân tích trung gian và có nguồn tham chiếu từ offline corpus.

Query demo chính:

```text
Compare single-agent and multi-agent architectures for complex research tasks
```

## Why multi-agent?

Single-agent baseline nhanh và đơn giản, nhưng không tách rõ các bước nghiên cứu, phân tích và viết. Với tác vụ nghiên cứu cần evidence trail, citation và debug, multi-agent phù hợp hơn vì mỗi agent có trách nhiệm riêng:

- Researcher tập trung tìm nguồn.
- Analyst tập trung phân tích và rút insight.
- Writer tập trung tổng hợp thành câu trả lời cuối.
- Supervisor kiểm soát route và điểm dừng.

Trade-off chính là multi-agent tốn latency và token hơn, nhưng đổi lại có trace, shared state và citation coverage tốt hơn.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Chọn route tiếp theo và dừng workflow khi hoàn tất | `ResearchState` | `route_history`, trace event | Route sai hoặc lặp vô hạn |
| Researcher | Tìm nguồn từ offline corpus và tạo research notes | Query, max sources | `sources`, `research_notes` | Không tìm thấy nguồn phù hợp |
| Analyst | Phân tích research notes thành insight | `research_notes`, `sources` | `analysis_notes` | Phân tích thiếu nếu research notes rỗng |
| Writer | Viết final answer có citations | Query, notes, sources | `final_answer` | Citation coverage thấp |
| Critic | Kiểm tra chất lượng/citation ở mức cơ bản | `final_answer`, `sources` | Critic findings trong `agent_results` | Bỏ sót claim không có nguồn |

## Shared state

| Field | Lý do cần có |
|---|---|
| `request` | Lưu query, audience và số nguồn tối đa |
| `iteration` | Kiểm soát số vòng chạy |
| `route_history` | Debug thứ tự agent đã chạy |
| `sources` | Lưu nguồn đã retrieval từ corpus |
| `research_notes` | Handoff từ Researcher sang Analyst |
| `analysis_notes` | Handoff từ Analyst sang Writer |
| `final_answer` | Kết quả cuối cùng trả cho user |
| `agent_results` | Lưu output/metadata của từng agent, gồm token usage |
| `trace` | Theo dõi sự kiện runtime |
| `errors` | Ghi lỗi hoặc cảnh báo không làm crash workflow |

## Routing policy

```text
Start
  -> Supervisor
  -> researcher nếu chưa có research_notes
  -> analyst nếu có research_notes nhưng chưa có analysis_notes
  -> writer nếu có analysis_notes nhưng chưa có final_answer
  -> done nếu đã có final_answer hoặc đạt max_iterations
```

Route demo:

```text
researcher -> analyst -> writer -> done
```

## Guardrails

- Max iterations: lấy từ `Settings.max_iterations`, mặc định 6.
- Timeout: lấy từ `Settings.timeout_seconds`, mặc định 60 giây.
- Retry: `LLMClient` có retry khi bật live OpenAI call.
- Fallback: mặc định dùng local deterministic LLM fallback nếu không bật live LLM.
- Validation: Pydantic schema cho query, source document, agent result và benchmark metrics.

## Benchmark plan

| Query | Metric | Expected outcome |
|---|---|---|
| Compare single-agent and multi-agent architectures for complex research tasks | Latency | Single-agent nhanh hơn |
| Same query | Token usage | Multi-agent dùng nhiều token hơn |
| Same query | Citation coverage | Multi-agent cao hơn vì dùng offline corpus |
| Same query | Quality heuristic | Multi-agent cao hơn do có research + analysis + sources |
| Same query | Failure rate | Cả hai không lỗi ở happy path |
