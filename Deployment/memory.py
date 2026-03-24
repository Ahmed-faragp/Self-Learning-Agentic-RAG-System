import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains import ConversationChain
from langchain_core.messages import messages_from_dict, messages_to_dict

load_dotenv()

llm = ChatOpenAI(
    model_name="meta-llama/llama-3-8b-instruct",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY")
)

def save_memory_to_file():
    messages = conversation.memory.chat_memory.messages
    with open("memory.json", "w") as f:
        json.dump(messages_to_dict(messages), f,indent=2)

def load_memory_from_file():
    try:
        with open("memory.json", "r") as f:
            messages_dict = json.load(f)
            messages = messages_from_dict(messages_dict)

        history = ChatMessageHistory()
        history.messages = messages
        return history

    except FileNotFoundError:
        print("No memory file found. Starting with empty memory.")
        return ChatMessageHistory()

history = load_memory_from_file()

memory = ConversationSummaryMemory(
    chat_memory=history,
    llm=llm,
)

conversation = ConversationChain(
    memory=memory,
    llm=llm,
)
def get_memory_messages():
    role_map = {
        "human": "user",
        "ai": "assistant",
        "system": "system"
    }

    return [
        {"role": role_map[m.type], "content": m.content}
        for m in conversation.memory.chat_memory.messages
    ]

print("Before conversation:")
print(memory.buffer)

conversation.predict(input="Hello")

print("\nAfter conversation:")
print(memory.buffer)