"""Base provider interface — all LLM providers implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass
class Message:
    """A single message in a conversation."""

    role: str  # "system", "user", "assistant", "tool"
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None
    timestamp: float | None = None
    name: str | None = None


@dataclass
class ToolCall:
    """A tool call requested by the LLM."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolDefinition:
    """Schema definition for a tool the LLM can call."""

    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    content: str | None = None
    tool_calls: list[ToolCall] | None = None
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: int = 0
    finish_reason: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


class ErrorClassification(str, Enum):
    """Classification of a provider error for retry/failover decisions."""

    TRANSIENT = "transient"       # 5xx, unknown — retry with backoff
    PERMANENT = "permanent"       # 4xx auth/client errors — fail immediately
    RATE_LIMITED = "rate_limited" # 429 — wait rate_limit_cooldown_seconds


# HTTP status codes that map to each classification
_PERMANENT_CODES = {400, 401, 403}
_RATE_LIMITED_CODES = {429}
_TRANSIENT_CODES = {500, 502, 503, 504}


class ProviderError(Exception):
    """Error from an LLM provider."""

    def __init__(
        self,
        message: str,
        http_status: int | None = None,
        provider: str = "",
        classification: ErrorClassification | None = None,
    ):
        super().__init__(message)
        self.http_status = http_status
        self.provider = provider

        if classification is not None:
            # Explicit classification wins
            self.classification: ErrorClassification = classification
        elif http_status in _PERMANENT_CODES:
            self.classification = ErrorClassification.PERMANENT
        elif http_status in _RATE_LIMITED_CODES:
            self.classification = ErrorClassification.RATE_LIMITED
        else:
            # TRANSIENT codes, None, or any other status — default to TRANSIENT
            self.classification = ErrorClassification.TRANSIENT


class ContextOverflowError(ProviderError):
    """Context window exceeded — route to compaction, not failover."""

    pass


class AllProvidersFailedError(ProviderError):
    """All providers in the failover chain have failed."""

    def __init__(self) -> None:
        super().__init__("All providers in failover chain failed", provider="failover")


class BaseProvider(ABC):
    """Abstract base class for LLM providers.

    Every provider (OpenRouter, Ollama, direct Anthropic, etc.)
    implements this interface.
    """

    name: str

    @abstractmethod
    async def chat(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Send messages to the LLM and get a response.

        Args:
            messages: Conversation history.
            tools: Available tools the LLM can call.
            model: Override the default model.
            temperature: Sampling temperature.

        Returns:
            LLMResponse with content and/or tool calls.

        Raises:
            ProviderError: If the API call fails.
            ContextOverflowError: If the context window is exceeded.
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is reachable and operational."""
        ...
