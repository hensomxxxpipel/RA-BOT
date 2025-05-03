import os
import time
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain.callbacks.manager import CallbackManager

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Callback & Tracer untuk semua model
tracer = LangChainTracer(project_name="chatbot-groq")
callback_manager = CallbackManager([tracer])

# Inisialisasi LLM dengan model berbeda
llm_models = {
    "llama4": ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
        streaming=True,
        temperature=0.7,
        callback_manager=callback_manager,
    ),
    "deepseek": ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="deepseek-r1-distill-llama-70b",
        streaming=True,
        temperature=0.7,
        callback_manager=callback_manager,
    ),
    "llama3": ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        streaming=True,
        temperature=0.7,
        callback_manager=callback_manager,
    ),
}

# Memori untuk tiap model
memories = {
    "llama4": ConversationBufferMemory(return_messages=True),
    "deepseek": ConversationBufferMemory(return_messages=True),
    "llama3": ConversationBufferMemory(return_messages=True),
}

# Fungsi untuk mengambil respons sesuai model
def get_response_stream(user_input, model_key):
    memory = memories[model_key]
    llm = llm_models[model_key]

    memory.chat_memory.add_user_message(user_input)
    messages = memory.chat_memory.messages

    full_response = ""
    for chunk in llm.stream(messages):
        if hasattr(chunk, "content") and chunk.content:
            time.sleep(0.05)
            content = chunk.content
            full_response += content
            yield content

    memory.chat_memory.add_ai_message(full_response)
