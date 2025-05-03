import streamlit as st
from chatbot.chatbot import get_response_stream

# Setup halaman
st.set_page_config(page_title="Chatbot Groq Langchain", layout="wide")
st.title("🤖 Chatbot dengan Groq + Langchain")

# Simpan riwayat obrolan
if "history" not in st.session_state:
    st.session_state.history = []

# Tampilkan percakapan sebelumnya (pesan pengguna dan AI)
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input pengguna
user_input = st.chat_input("Tanyakan sesuatu...")

if user_input:
    # Menambahkan pesan pengguna ke riwayat
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Menampilkan pesan pengguna terbaru
    with st.chat_message("user"):
        st.markdown(user_input)

    # Menampilkan respons AI
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # Mendapatkan respons streaming dari chatbot
        response_stream = get_response_stream(user_input)
        
        # Streaming respons dan menampilkannya secara bertahap
        for chunk in response_stream:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")  # Menambahkan indikator streaming
        
        # Menampilkan respons final tanpa indikator
        response_placeholder.markdown(full_response)
    
    # Menambahkan respons AI ke riwayat percakapan
    st.session_state.history.append({"role": "assistant", "content": full_response})
    
    
# groq.RateLimitError: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jkw0dpcqfcetk8saczqnarey` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99918, Requested 340. Please try again in 3m42.547999999s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
