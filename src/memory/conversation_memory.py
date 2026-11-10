# src/memory/conversation_memory.py
"""
voxi — Conversation Memory Module
Stores and manages multi-turn conversation history.
"""

from src.config.settings import MAX_CONVERSATION_HISTORY


class ConversationMemory:
    """Maintains conversation context across multiple turns."""

    def __init__(self) -> None:
        """Initialize empty message history."""
        self.history: list[dict[str, str]] = []
        print("✅ Conversation memory initialized")

    def add_user_message(self, message: str) -> None:
        """
        Add a user message to history and enforce window limits.

        Args:
            message: User input text.
        """
        self.history.append({
            "role": "user",
            "content": message
        })
        self._trim()

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant response to history and enforce window limits.

        Args:
            message: Assistant output text.
        """
        self.history.append({
            "role": "assistant",
            "content": message
        })
        self._trim()

    def get_history(self) -> list[dict[str, str]]:
        """
        Get conversation history for LLM context excluding current prompt.

        Returns:
            list[dict[str, str]]: Prior conversation messages.
        """
        if not self.history:
            return []
        # Exclude the last message (it's the current user input)
        return self.history[:-1]

    def _trim(self) -> None:
        """Keep only the last N turns to prevent context overflow."""
        max_messages: int = MAX_CONVERSATION_HISTORY * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]

    def clear(self) -> None:
        """Clear all conversation history."""
        self.history = []
        print("🔄 Memory cleared")

    def summary(self) -> str:
        """
        Return a summary of current memory state.

        Returns:
            str: Human-readable summary string.
        """
        turns: int = len(self.history) // 2
        return f"💾 Memory: {turns} turns stored (max {MAX_CONVERSATION_HISTORY})"
