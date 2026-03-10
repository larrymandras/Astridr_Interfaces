"""Astridr Interfaces — base abstract classes for the Astridr agent framework."""

from astridr_interfaces.channels import (
    Attachment,
    BaseChannel,
    IncomingMessage,
    InlineButton,
    MessageHandler,
    OutgoingMessage,
)
from astridr_interfaces.memory import (
    BaseMemory,
    IndexReport,
    MemoryEntry,
)
from astridr_interfaces.providers import (
    AllProvidersFailedError,
    BaseProvider,
    ContextOverflowError,
    LLMResponse,
    Message,
    ProviderError,
    ToolCall,
    ToolDefinition,
)
from astridr_interfaces.tools import (
    BaseTool,
    ToolResult,
)

__all__ = [
    # Providers
    "BaseProvider",
    "Message",
    "ToolCall",
    "ToolDefinition",
    "LLMResponse",
    "ProviderError",
    "ContextOverflowError",
    "AllProvidersFailedError",
    # Channels
    "BaseChannel",
    "IncomingMessage",
    "OutgoingMessage",
    "Attachment",
    "InlineButton",
    "MessageHandler",
    # Tools
    "BaseTool",
    "ToolResult",
    # Memory
    "BaseMemory",
    "MemoryEntry",
    "IndexReport",
]
