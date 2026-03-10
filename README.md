# astridr-interfaces

Base abstract classes and data types extracted from the [Astridr](https://github.com/larrymandras/astridr) agent framework monorepo. Install this package to implement a custom provider, channel, tool, or memory backend without depending on the full framework.

## Exported interfaces and types

### Providers (`astridr_interfaces.providers`)

| Name | Kind | Description |
|------|------|-------------|
| `BaseProvider` | ABC | Abstract LLM provider — implement `chat()` and `health_check()` |
| `Message` | dataclass | A single message in a conversation (role, content, tool calls) |
| `ToolCall` | dataclass | A tool invocation requested by the LLM |
| `ToolDefinition` | dataclass | JSON Schema definition for a tool the LLM can call |
| `LLMResponse` | dataclass | Response payload from an LLM (content, tool calls, token counts, cost) |
| `ProviderError` | exception | Base error for provider failures |
| `ContextOverflowError` | exception | Context window exceeded |
| `AllProvidersFailedError` | exception | Every provider in the failover chain failed |

### Channels (`astridr_interfaces.channels`)

| Name | Kind | Description |
|------|------|-------------|
| `BaseChannel` | ABC | Abstract communication channel — implement `start()`, `send()`, `send_typing()`, `stop()` |
| `IncomingMessage` | dataclass | A message received from a channel |
| `OutgoingMessage` | dataclass | A message to send via a channel |
| `Attachment` | dataclass | File attachment (image, document, audio, etc.) |
| `InlineButton` | dataclass | Inline button for approval gates and interactive responses |
| `MessageHandler` | type alias | `Callable[[IncomingMessage], Coroutine[Any, Any, None]]` |

### Tools (`astridr_interfaces.tools`)

| Name | Kind | Description |
|------|------|-------------|
| `BaseTool` | ABC | Abstract tool — implement `execute()`. Has `approval_tier` (`read_only`, `supervised`, `autonomous`) |
| `ToolResult` | dataclass | Result from a tool execution (success, output, error, data) |

### Memory (`astridr_interfaces.memory`)

| Name | Kind | Description |
|------|------|-------------|
| `BaseMemory` | ABC | Abstract memory backend — implement `save()`, `search()`, `forget()`, `recent()`, `load_index()`, `rebuild_index()` |
| `MemoryEntry` | dataclass | A single memory entry (id, content, category, topic, score) |
| `IndexReport` | dataclass | Report from a memory index rebuild operation |

## Installation

```bash
pip install astridr-interfaces
```

Or from source:

```bash
pip install git+https://github.com/larrymandras/Astridr_Interfaces.git
```

## Usage

### Implement a custom provider

```python
from astridr_interfaces import BaseProvider, Message, ToolDefinition, LLMResponse

class MyProvider(BaseProvider):
    name = "my-provider"

    async def chat(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> LLMResponse:
        # Call your LLM API here
        return LLMResponse(content="Hello!")

    async def health_check(self) -> bool:
        return True
```

### Implement a custom channel

```python
from astridr_interfaces import BaseChannel, MessageHandler, OutgoingMessage

class MyChannel(BaseChannel):
    channel_id = "my-channel"

    async def start(self, on_message: MessageHandler) -> None:
        # Start listening for messages
        ...

    async def send(self, message: OutgoingMessage) -> None:
        # Send a message
        ...

    async def send_typing(self, chat_id: str) -> None:
        ...

    async def stop(self) -> None:
        ...
```

### Implement a custom tool

```python
from astridr_interfaces import BaseTool, ToolResult

class MyTool(BaseTool):
    name = "my_tool"
    description = "Does something useful"
    parameters = {"type": "object", "properties": {"query": {"type": "string"}}}
    approval_tier = "read_only"

    async def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=True, output="Done!")
```

### Implement a custom memory backend

```python
from astridr_interfaces import BaseMemory, MemoryEntry, IndexReport

class MyMemory(BaseMemory):
    async def save(self, content: str, category: str = "fact", topic: str | None = None) -> str:
        ...

    async def search(self, query: str, limit: int = 10) -> list[MemoryEntry]:
        ...

    async def forget(self, memory_id: str) -> bool:
        ...

    async def recent(self, limit: int = 20) -> list[MemoryEntry]:
        ...

    async def load_index(self, max_lines: int = 100) -> str:
        ...

    async def rebuild_index(self) -> IndexReport:
        ...
```

## Requirements

- Python >= 3.11
- No runtime dependencies (stdlib only: `abc`, `dataclasses`, `typing`, `pathlib`)
