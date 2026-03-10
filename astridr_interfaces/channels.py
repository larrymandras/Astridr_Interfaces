"""Base channel interface — all communication channels implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine


@dataclass
class IncomingMessage:
    """A message received from a channel."""

    text: str
    sender_id: str
    chat_id: str
    channel_id: str
    timestamp: float
    reply_to_message_id: str | None = None
    attachments: list[Attachment] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class OutgoingMessage:
    """A message to send via a channel."""

    text: str
    chat_id: str
    reply_to_message_id: str | None = None
    attachments: list[Attachment] = field(default_factory=list)
    parse_mode: str | None = None  # "markdown", "html", etc.
    buttons: list[InlineButton] | None = None


@dataclass
class Attachment:
    """A file attachment (image, document, audio, etc.)."""

    file_path: str | None = None
    file_url: str | None = None
    file_bytes: bytes | None = None
    mime_type: str = "application/octet-stream"
    filename: str = "file"


@dataclass
class InlineButton:
    """An inline button for approval gates and interactive responses."""

    text: str
    callback_data: str


# Type alias for the message handler callback
MessageHandler = Callable[[IncomingMessage], Coroutine[Any, Any, None]]


class BaseChannel(ABC):
    """Abstract base class for communication channels.

    Every channel (Telegram, Slack, Email, Web, Voice)
    implements this interface.
    """

    channel_id: str

    @abstractmethod
    async def start(self, on_message: MessageHandler) -> None:
        """Start listening for messages. Calls on_message for each incoming message."""
        ...

    @abstractmethod
    async def send(self, message: OutgoingMessage) -> None:
        """Send a message to a chat."""
        ...

    @abstractmethod
    async def send_typing(self, chat_id: str) -> None:
        """Show typing indicator in the chat."""
        ...

    @abstractmethod
    async def stop(self) -> None:
        """Gracefully stop the channel listener."""
        ...
