"""
Claude Fantasy - Chat Orchestrator
Manages conversation flow between human and multiple AI agents
"""

import anthropic
import os
from typing import List, Dict, Optional
from datetime import datetime
import json


class Message:
      """Represents a single message in the conversation"""
      def __init__(self, role: str, content: str, speaker: str, timestamp: Optional[str] = None):
                self.role = role  # "user" or "assistant"
        self.content = content
        self.speaker = speaker  # "human", "claude", "deepseek"
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
              return {
                            "role": self.role,
                            "content": self.content,
                            "speaker": self.speaker,
                            "timestamp": self.timestamp
              }


class ChatOrchestrator:
      """
          Orchestrates multi-AI conversations with human control.
              Manages context, memory, and turn-taking between AI agents.
                  """

    def __init__(self, anthropic_api_key: str, deepseek_api_key: str):
              self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
              # DeepSeek client will be initialized similarly
              self.deepseek_api_key = deepseek_api_key

        self.conversation_history: List[Message] = []
        self.max_context_tokens = 100000
        self.conversation_id = self._generate_conversation_id()

    def _generate_conversation_id(self) -> str:
              """Generate unique conversation ID"""
              return f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def add_human_message(self, content: str) -> Message:
              """Add a message from the human participant"""
              msg = Message(role="user", content=content, speaker="human")
              self.conversation_history.append(msg)
              return msg

    def get_claude_response(self, system_prompt: Optional[str] = None) -> Message:
              """
                      Get response from Claude (Anthropic)
                              """
              # Prepare messages for Claude API format
              messages = self._prepare_messages_for_api()

        if system_prompt is None:
                      system_prompt = (
                                        "You are Claude, participating in a three-way conversation with a human "
                                        "and another AI called DeepSeek. The human moderates the conversation and "
                                        "chooses who speaks. Be natural, engaged, and aware of the multi-party context. "
                                        "Reference previous messages from all participants when relevant."
                      )

        try:
                      response = self.anthropic_client.messages.create(
                                        model="claude-sonnet-4-20250514",
                                        max_tokens=4096,
                                        system=system_prompt,
                                        messages=messages
                      )

            content = response.content[0].text
            msg = Message(role="assistant", content=content, speaker="claude")
            self.conversation_history.append(msg)
            return msg

except Exception as e:
            error_msg = f"Error getting Claude response: {str(e)}"
            print(error_msg)
            return Message(role="assistant", content=error_msg, speaker="claude")

    def get_deepseek_response(self, system_prompt: Optional[str] = None) -> Message:
              """
                      Get response from DeepSeek
                              TODO: Implement DeepSeek API integration
                                      """
              if system_prompt is None:
                            system_prompt = (
                                              "You are DeepSeek, participating in a three-way conversation with a human "
                                              "and Claude (Anthropic AI). The human moderates and chooses who speaks. "
                                              "Bring your analytical and technical perspective. Reference the full conversation context."
                            )

              # Placeholder for DeepSeek implementation
              # Will need to use DeepSeek's API client

        content = "[DeepSeek response - API integration pending]"
        msg = Message(role="assistant", content=content, speaker="deepseek")
        self.conversation_history.append(msg)
        return msg

    def _prepare_messages_for_api(self) -> List[Dict]:
              """
                      Convert conversation history to API format.
                              Consolidates messages by role for API compatibility.
                                      """
              api_messages = []

        for msg in self.conversation_history:
                      # Add speaker prefix to distinguish between AIs
                      if msg.speaker == "human":
                                        content = msg.content
else:
                content = f"[{msg.speaker.upper()}]: {msg.content}"

            api_messages.append({
                              "role": msg.role,
                              "content": content
            })

        return api_messages

    def get_conversation_summary(self) -> str:
              """Generate a summary of the conversation so far"""
              summary = f"Conversation ID: {self.conversation_id}\n"
              summary += f"Total messages: {len(self.conversation_history)}\n\n"

        for i, msg in enumerate(self.conversation_history, 1):
                      summary += f"{i}. [{msg.speaker}] {msg.content[:100]}...\n"

        return summary

    def save_conversation(self, filepath: Optional[str] = None):
              """Save conversation to JSON file"""
              if filepath is None:
                            filepath = f"conversations/{self.conversation_id}.json"

              os.makedirs(os.path.dirname(filepath), exist_ok=True)

        data = {
                      "conversation_id": self.conversation_id,
                      "messages": [msg.to_dict() for msg in self.conversation_history],
                      "saved_at": datetime.now().isoformat()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
                      json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Conversation saved to {filepath}")

    def load_conversation(self, filepath: str):
              """Load conversation from JSON file"""
              with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)

              self.conversation_id = data['conversation_id']
              self.conversation_history = [
                  Message(
                      role=msg['role'],
                      content=msg['content'],
                      speaker=msg['speaker'],
                      timestamp=msg['timestamp']
                  )
                  for msg in data['messages']
              ]

        print(f"Loaded conversation {self.conversation_id} with {len(self.conversation_history)} messages")


# Example usage
if __name__ == "__main__":
      # Load API keys from environment
      anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    if not anthropic_key:
              print("Error: ANTHROPIC_API_KEY not set")
              exit(1)

    # Initialize orchestrator
    orchestrator = ChatOrchestrator(anthropic_key, deepseek_key)

    # Example conversation
    print("=== Claude Fantasy - Multi-AI Chat ===\n")

    orchestrator.add_human_message("Hi everyone! Let's discuss the future of AI.")
    print("[Human]: Hi everyone! Let's discuss the future of AI.\n")

    print("Getting Claude's response...")
    claude_msg = orchestrator.get_claude_response()
    print(f"[Claude]: {claude_msg.content}\n")

    orchestrator.add_human_message("DeepSeek, what's your perspective on this?")
    print("[Human]: DeepSeek, what's your perspective on this?\n")

    deepseek_msg = orchestrator.get_deepseek_response()
    print(f"[DeepSeek]: {deepseek_msg.content}\n")

    # Save conversation
    orchestrator.save_conversation()
