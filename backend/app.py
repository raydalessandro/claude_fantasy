"""
Claude Fantasy - FastAPI Server
Main application server for multi-AI chat orchestration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

# Load environment variables
load_dotenv()

app = FastAPI(title="Claude Fantasy API", version="1.0.0")

# CORS middleware for frontend access
app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # In production, specify your frontend domain
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

# Initialize AI clients
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
deepseek_client = OpenAI(
      api_key=os.getenv("DEEPSEEK_API_KEY"),
      base_url="https://api.deepseek.com"
)

# In-memory conversation storage (in production, use a database)
conversations = {}


class ChatMessage(BaseModel):
      message: str
      ai: str  # "claude" or "deepseek"
    conversation_id: Optional[str] = "default"


class ChatResponse(BaseModel):
      response: str
      speaker: str
      conversation_id: str


@app.get("/")
async def root():
      """Root endpoint"""
      return {
          "app": "Claude Fantasy",
          "version": "1.0.0",
          "status": "running"
      }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
      """
          Main chat endpoint - routes message to selected AI
              """
      conv_id = message.conversation_id

    # Initialize conversation if it doesn't exist
      if conv_id not in conversations:
                conversations[conv_id] = []

      # Add human message to history
      conversations[conv_id].append({
          "role": "user",
          "content": message.message,
          "speaker": "human"
      })

    # Route to appropriate AI
      if message.ai == "claude":
                response_text = await get_claude_response(conv_id)
                speaker = "Claude"
elif message.ai == "deepseek":
        response_text = await get_deepseek_response(conv_id)
        speaker = "DeepSeek"
else:
        raise HTTPException(status_code=400, detail="Invalid AI selection")

    # Add AI response to history
      conversations[conv_id].append({
                "role": "assistant",
                "content": response_text,
                "speaker": message.ai
      })

    return ChatResponse(
              response=response_text,
              speaker=speaker,
              conversation_id=conv_id
    )


async def get_claude_response(conv_id: str) -> str:
      """Get response from Claude (Anthropic)"""
      try:
                # Prepare messages for Claude API
                messages = prepare_messages_for_api(conv_id, "claude")

        system_prompt = (
                      "You are Claude, participating in a three-way conversation with a human "
                      "and another AI called DeepSeek. The human moderates the conversation and "
                      "chooses who speaks. Be natural, engaged, and aware of the multi-party context. "
                      "Reference previous messages from all participants when relevant."
        )

        response = anthropic_client.messages.create(
                      model="claude-sonnet-4-20250514",
                      max_tokens=4096,
                      system=system_prompt,
                      messages=messages
        )

        return response.content[0].text

except Exception as e:
        print(f"Error getting Claude response: {str(e)}")
        return f"Error: Unable to get response from Claude. {str(e)}"


async def get_deepseek_response(conv_id: str) -> str:
      """Get response from DeepSeek"""
    try:
              # Prepare messages for DeepSeek API
              messages = prepare_messages_for_api(conv_id, "deepseek")

        system_prompt = (
                      "You are DeepSeek, participating in a three-way conversation with a human "
                      "and Claude (Anthropic AI). The human moderates and chooses who speaks. "
                      "Bring your analytical and technical perspective. Reference the full conversation context."
        )

        # Add system message
        messages_with_system = [{"role": "system", "content": system_prompt}] + messages

        response = deepseek_client.chat.completions.create(
                      model="deepseek-chat",
                      messages=messages_with_system,
                      stream=False
        )

        return response.choices[0].message.content

except Exception as e:
        print(f"Error getting DeepSeek response: {str(e)}")
        return f"Error: Unable to get response from DeepSeek. {str(e)}"


def prepare_messages_for_api(conv_id: str, current_ai: str):
      """
          Prepare conversation history for API format
              Add speaker labels to distinguish between AIs
                  """
    messages = []
    conversation = conversations.get(conv_id, [])

    for msg in conversation:
              speaker = msg.get("speaker", "unknown")
              content = msg["content"]

        # Add speaker prefix for AI messages to distinguish them
              if speaker not in ["human", "user"]:
                            content = f"[{speaker.upper()}]: {content}"

        messages.append({
                      "role": msg["role"],
                      "content": content
        })

    return messages


@app.get("/api/conversation/{conv_id}")
async def get_conversation(conv_id: str):
      """Get conversation history"""
    if conv_id not in conversations:
              return {"messages": []}

    return {"messages": conversations[conv_id]}


@app.delete("/api/conversation/{conv_id}")
async def clear_conversation(conv_id: str):
      """Clear conversation history"""
    if conv_id in conversations:
              del conversations[conv_id]

    return {"status": "cleared", "conversation_id": conv_id}


@app.get("/api/health")
async def health_check():
      """Health check endpoint"""
    return {
              "status": "healthy",
              "anthropic_key_set": bool(os.getenv("ANTHROPIC_API_KEY")),
              "deepseek_key_set": bool(os.getenv("DEEPSEEK_API_KEY")),
              "active_conversations": len(conversations)
    }


if __name__ == "__main__":
      import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
