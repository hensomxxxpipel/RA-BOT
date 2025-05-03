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

# Inisialisasi tracer dan callback
tracer = LangChainTracer(project_name="chatbot-groq")
callback_manager = CallbackManager([tracer])

# Inisialisasi LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
    streaming=True,
    temperature=0.7,
    callback_manager=callback_manager,
)

memory = ConversationBufferMemory(return_messages=True)

def get_response_stream(user_input):
    memory.chat_memory.add_user_message(user_input)  # Menambahkan pesan pengguna ke memori
    messages = memory.chat_memory.messages  # Mendapatkan seluruh riwayat pesan

    full_response = ""
    # Streaming respons dari LLM
    for chunk in llm.stream(messages):
        if hasattr(chunk, "content") and chunk.content:
            time.sleep(0.05)  # Perlambatan untuk efek streaming
            content = chunk.content
            full_response += content
            yield content  # Mengirimkan chunk respons

    # Menambahkan respons AI ke memori
    memory.chat_memory.add_ai_message(full_response)
