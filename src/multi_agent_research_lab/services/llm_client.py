"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass
from time import perf_counter

from tenacity import retry, stop_after_attempt, wait_exponential

from multi_agent_research_lab.core.config import get_settings


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client.

    The default path is deterministic and offline-friendly so tests and lab demos run without
    external credentials. When `OPENAI_API_KEY` is set and the OpenAI package is installed, the
    same interface can call a real model.
    """

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion.

        Keep retry, timeout, and token logging here rather than inside agents.
        """

        settings = get_settings()
        if settings.use_live_llm and settings.openai_api_key:
            try:
                return self._complete_with_openai(system_prompt, user_prompt)
            except Exception:
                return self._complete_locally(system_prompt, user_prompt)
        return self._complete_locally(system_prompt, user_prompt)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        reraise=True,
    )
    def _complete_with_openai(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        settings = get_settings()
        try:
            from openai import OpenAI
        except ImportError:
            return self._complete_locally(system_prompt, user_prompt)

        started = perf_counter()
        client = OpenAI(api_key=settings.openai_api_key, timeout=settings.timeout_seconds)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or ""
        usage = response.usage
        input_tokens = None if usage is None else usage.prompt_tokens
        output_tokens = None if usage is None else usage.completion_tokens
        cost = self._estimate_cost_usd(input_tokens, output_tokens)
        elapsed_note = f"\n\n[model_latency_seconds={perf_counter() - started:.2f}]"
        return LLMResponse(
            content=content.strip() + elapsed_note,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        )

    def _complete_locally(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        words = (system_prompt + " " + user_prompt).split()
        input_tokens = max(1, int(len(words) * 1.3))
        focus = self._first_non_empty_line(user_prompt)
        content = (
            f"{focus}\n\n"
            "Key points:\n"
            "- The request was handled with the local deterministic LLM fallback.\n"
            "- Use real provider credentials when live model reasoning is required.\n"
            "- The output is concise, traceable, and suitable for offline workflow tests."
        )
        output_tokens = max(1, int(len(content.split()) * 1.3))
        return LLMResponse(content=content, input_tokens=input_tokens, output_tokens=output_tokens)

    def _estimate_cost_usd(
        self,
        input_tokens: int | None,
        output_tokens: int | None,
    ) -> float | None:
        if input_tokens is None or output_tokens is None:
            return None
        return (input_tokens * 0.00000015) + (output_tokens * 0.00000060)

    def _first_non_empty_line(self, text: str) -> str:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:240]
        return "Generated response"
