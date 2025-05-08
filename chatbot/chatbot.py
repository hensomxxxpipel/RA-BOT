import os
import time
import random
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
# from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain.callbacks.manager import CallbackManager

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CLAUDE_API_KEY_A = os.getenv("CLAUDE_API_KEY_A")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    # "claude3.a": ChatAnthropic(
    #     api_key=CLAUDE_API_KEY_A,
    #     model="claude-3-7-sonnet-20250219",
    #     temperature=0.7,
    #     streaming=True,
    #     callback_manager=callback_manager,
    # ),
    "gemini.flash": ChatGoogleGenerativeAI(
        api_key=GEMINI_API_KEY,
        model="gemini-2.5-pro-exp-03-25",
        temperature=0.7,
        streaming=True,
        callback_manager=callback_manager,
    ),
}

# Memori untuk tiap model
memories = {
    "llama4": ConversationBufferMemory(return_messages=True),
    "deepseek": ConversationBufferMemory(return_messages=True),
    "llama3": ConversationBufferMemory(return_messages=True),
    # "claude3.a": ConversationBufferMemory(return_messages=True),
    "gemini.flash": ConversationBufferMemory(return_messages=True),
}

# Fungsi untuk mengambil respons sesuai model
def get_response_stream(user_input, model_key):
    try:
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
        
    except Exception as e:
        messages = [
            "Maaf, terjadi kesalahan saat menghasilkan jawaban. Silakan coba beberapa saat lagi atau gunakan alternatif chatbot jika diperlukan.",
            "Ups! Kami mengalami kendala teknis saat memproses permintaan Anda. Cobalah beberapa saat lagi atau coba gunakan model lain.",
            "Sepertinya ada gangguan saat sistem mencoba memberikan respon. Mohon ulangi permintaan Anda nanti atau pilih chatbot lain untuk mencoba.",
            "Permintaan Anda tidak dapat diproses saat ini. Silakan tunggu beberapa saat dan coba kembali, atau gunakan chatbot lainnya untuk solusi."
        ]
        
        error_message = random.choice(messages)
        
        chunk_size = 10
        for i in range(0, len(error_message), chunk_size):
            chunk = error_message[i:i + chunk_size]
            yield chunk
            time.sleep(0.05)