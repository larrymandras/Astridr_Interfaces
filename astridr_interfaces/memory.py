"""Base memory interface — all memory backends implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MemoryEntry:
    """A single memory entry returned from search or recall."""

    id: str
    content: str
    category: str  # "fact", "preference", "decision", "solution", "log"
    topic: str | None
    source_file: Path
    score: float = 0.0
    created_at: str = ""
    metadata: dict = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


@dataclass
class IndexReport:
    """Report from a memory index rebuild operation."""

    files_indexed: int
    entries_indexed: int = 0
    duration_ms: int = 0
    errors: list[str] | None = None


class BaseMemory(ABC):
    """Abstract base class for memory backends.

    The primary implementation is MarkdownMemoryStore (file-first).
    SQLite FTS5 and sqlite-vec are derived indexes, not primary stores.
    """

    @abstractmethod
    async def save(
        self,
        content: str,
        category: str = "fact",
        topic: str | None = None,
    ) -> str:
        """Save a memory entry. Returns the file path where it was saved."""
        ...

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[MemoryEntry]:
        """Search memories using hybrid FTS5 + vector search."""
        ...

    @abstractmethod
    async def forget(self, memory_id: str) -> bool:
        """Remove a specific memory entry. Returns True if found and removed."""
        ...

    @abstractmethod
    async def recent(self, limit: int = 20) -> list[MemoryEntry]:
        """Get the most recent memory entries."""
        ...

    @abstractmethod
    async def load_index(self, max_lines: int = 100) -> str:
        """Load the MEMORY.md index file (Layer 1). Always injected into system prompt."""
        ...

    @abstractmethod
    async def rebuild_index(self) -> IndexReport:
        """Re-index all markdown files from scratch. Nuclear option for corruption."""
        ...
