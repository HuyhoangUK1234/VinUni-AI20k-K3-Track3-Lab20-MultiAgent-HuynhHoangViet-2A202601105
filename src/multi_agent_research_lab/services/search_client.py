"""Search client abstraction for ResearcherAgent."""

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from multi_agent_research_lab.core.schemas import SourceDocument

DEFAULT_CORPUS_ROOT = Path("ai_agent_offline_research_corpus_v2")
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class CorpusRecord:
    title: str
    citation_id: str
    text: str
    metadata: dict[str, Any]


class SearchClient:
    """Provider-agnostic search client.

    The default implementation searches the bundled offline corpus when it exists. A live
    Tavily/Bing/SerpAPI adapter can later replace this class without changing the researcher.
    """

    def __init__(self, corpus_root: Path | str = DEFAULT_CORPUS_ROOT) -> None:
        self.corpus_root = Path(corpus_root)

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.
        """

        normalized_query = " ".join(query.split())
        if not normalized_query:
            return []
        corpus_results = self._search_corpus(normalized_query, max_results=max_results)
        if corpus_results:
            return corpus_results
        return self._synthetic_search(normalized_query, max_results=max_results)

    def _search_corpus(self, query: str, max_results: int) -> list[SourceDocument]:
        records = _load_corpus_records(self.corpus_root)
        if not records:
            return []

        query_terms = _tokens(query)
        scored_records: list[tuple[float, CorpusRecord]] = []
        for record in records:
            haystack = f"{record.title} {record.text}"
            terms = _tokens(haystack)
            overlap = len(query_terms & terms)
            topic_terms = _tokens(str(record.metadata.get("topic_title", "")))
            topic_bonus = 3 if query_terms & topic_terms else 0
            title_bonus = 2 if query_terms & _tokens(record.title) else 0
            score = overlap + topic_bonus + title_bonus
            if score > 0:
                scored_records.append((score, record))

        scored_records.sort(key=lambda item: (-item[0], str(item[1].metadata.get("rank_key", ""))))
        return [
            SourceDocument(
                title=record.title,
                url=f"offline-corpus://{record.citation_id}",
                snippet=_snippet(record.text),
                metadata={**record.metadata, "citation_id": record.citation_id, "score": score},
            )
            for score, record in scored_records[:max_results]
        ]

    def _synthetic_search(self, query: str, max_results: int) -> list[SourceDocument]:
        normalized_query = " ".join(query.split())

        templates = [
            (
                "Overview",
                "Defines the topic, common terminology, and the main system components.",
            ),
            (
                "Architecture",
                "Explains design trade-offs, orchestration choices, and production constraints.",
            ),
            (
                "Evaluation",
                "Summarizes quality metrics, latency, cost tracking, and failure modes.",
            ),
            (
                "Operations",
                "Covers guardrails, tracing, retries, timeout handling, and incident response.",
            ),
            (
                "Implementation",
                "Highlights practical integration steps and testing strategies.",
            ),
        ]
        results: list[SourceDocument] = []
        for index, (title_suffix, snippet) in enumerate(templates[:max_results], start=1):
            slug = "-".join(normalized_query.lower().split())[:80]
            results.append(
                SourceDocument(
                    title=f"{title_suffix}: {normalized_query}",
                    url=f"local://research/{slug}/{index}",
                    snippet=f"{snippet} Query focus: {normalized_query}.",
                    metadata={"provider": "local_mock", "rank": index},
                )
            )
        return results


@lru_cache(maxsize=4)
def _load_corpus_records(corpus_root: Path) -> tuple[CorpusRecord, ...]:
    topics_dir = corpus_root / "topics"
    if not topics_dir.exists():
        return ()

    records: list[CorpusRecord] = []
    for topic_file in sorted(topics_dir.glob("*.json")):
        try:
            payload = json.loads(topic_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        topic = payload.get("topic", {})
        knowledge_base = payload.get("knowledge_base", {})
        topic_name = str(topic.get("name", topic_file.stem))
        topic_id = str(payload.get("benchmark_metadata", {}).get("topic_id", topic_file.stem))

        for index, article in enumerate(knowledge_base.get("knowledge_articles", []), start=1):
            article_id = str(article.get("article_id", f"A{index:02d}"))
            title = str(article.get("title", article_id))
            records.append(
                CorpusRecord(
                    title=f"{topic_name} / {title}",
                    citation_id=f"{topic_id}:{article_id}",
                    text=str(article.get("content", "")),
                    metadata={
                        "provider": "offline_corpus",
                        "record_type": "knowledge_article",
                        "topic_id": topic_id,
                        "topic_title": topic_name,
                        "article_id": article_id,
                        "rank_key": f"{topic_file.name}:article:{index:02d}",
                    },
                )
            )

        for index, document in enumerate(knowledge_base.get("source_documents", []), start=1):
            document_id = str(document.get("document_id", f"D{index:02d}"))
            title = str(document.get("title", document_id))
            records.append(
                CorpusRecord(
                    title=f"{topic_name} / {title}",
                    citation_id=f"{topic_id}:{document_id}",
                    text=str(document.get("full_text", "")),
                    metadata={
                        "provider": "offline_corpus",
                        "record_type": "source_document",
                        "topic_id": topic_id,
                        "topic_title": topic_name,
                        "document_id": document_id,
                        "document_class": document.get("document_class"),
                        "is_synthetic": bool(document.get("is_synthetic", False)),
                        "provenance_url": document.get("provenance_url"),
                        "rank_key": f"{topic_file.name}:source:{index:02d}",
                    },
                )
            )
    return tuple(records)


def _tokens(text: str) -> set[str]:
    return {token for token in TOKEN_PATTERN.findall(text.lower()) if len(token) > 2}


def _snippet(text: str, max_chars: int = 700) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."
