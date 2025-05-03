import streamlit as st
from chatbot.chatbot import get_response_stream
import time

# Setup halaman
st.set_page_config(page_title="RA-BOT", layout="wide")
st.markdown("""
    <style>
        .ra-title {
            font-size: 5vw;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .ra-description {
            font-size: 1rem;
            text-align: justify;
            margin: auto;
        }
        
        .ra-bot1 {
            font-size: 1rem;
            text-align: left;
            margin: auto;
        }
        
        .custom-info-box {
            background-color: rgba(61, 157, 243, 0.2);
            color: rgb(199, 235, 255);
            border-left: 6px solid rgb(61, 157, 243);
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            font-family: "Source Sans Pro", sans-serif;
        }
        
        .warna{
            color: rgb(255, 75, 75);
        }
    </style>
""", unsafe_allow_html=True)

# Tampilkan judul dan deskripsi
st.markdown("""
    <h2 class='ra-title'>🤖 RA-BOT</h2>
    <p class='ra-description'>
        <b>RA-BOT</b> merupakan sebuah chatbot interaktif yang didukung oleh berbagai model Language Model (LLM) untuk membantu pengguna dalam beragam topik dan percakapan. Dirancang dengan antarmuka yang sederhana dan intuitif, RA-Bot dapat digunakan untuk berdiskusi, mencari informasi, atau sekadar berinteraksi secara natural. Sistem ini terbagi dalam beberapa tab yang masing-masing dioptimalkan untuk model chatbot yang berbeda, sehingga jika Anda kurang puas dengan respons dari satu model, Anda dapat mencoba model lainnya dengan mudah.
    </p>
""", unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)

# Membuat tabs
tab1, tab2, tab3 = st.tabs(["Chatbot 1", "Chatbot 2", "Chatbot 3"])

# Inisialisasi history untuk setiap tab jika belum ada
if "history_tab1" not in st.session_state:
    st.session_state.history_tab1 = []
if "history_tab2" not in st.session_state:
    st.session_state.history_tab2 = []
if "history_tab3" not in st.session_state:
    st.session_state.history_tab3 = []

# Tab 1: Chatbot 1
with tab1:
    st.markdown("""
        <div class="custom-info-box">
        <p class='ra-bot1'>
            Bot ini menggunakan model <i class="warna"><b>Llama 4 Maverick</b></i> dari Meta AI
        </p>
        </div>
    """, unsafe_allow_html=True)
    
    
    # Buat container untuk chat messages
    chat_container = st.container()
    
    # Buat input di bagian bawah
    user_input_tab1 = st.chat_input("Tanyakan sesuatu ke Chatbot 1...")
    
    # Tampilkan percakapan sebelumnya untuk tab 1
    with chat_container:
        for msg in st.session_state.history_tab1:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if user_input_tab1:
        # Menambahkan pesan pengguna ke riwayat tab 1
        st.session_state.history_tab1.append({"role": "user", "content": user_input_tab1})
        
        # Menampilkan pesan pengguna terbaru dalam container
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input_tab1)
        
            # Menampilkan respons AI
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
        
                # Mendapatkan respons streaming dari chatbot
                # response_stream = get_response_stream(user_input_tab1)
                response_stream = get_response_stream(user_input_tab1, "llama4")
                
                # Streaming respons dan menampilkannya secara bertahap
                for chunk in response_stream:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")  # Menambahkan indikator streaming
                
                # Menampilkan respons final tanpa indikator
                response_placeholder.markdown(full_response)
        
        # Menambahkan respons AI ke riwayat percakapan tab 1
        st.session_state.history_tab1.append({"role": "assistant", "content": full_response})
        

# Tab 2: Chatbot 2
with tab2:
    st.markdown("""
        <div class="custom-info-box">
        <p class='ra-bot1'>
            Bot ini menggunakan model <i class="warna"><b>Deepseek-R1</b></i>. Jirrr gabisa bindo loh ya nguawur rek 😁😂
        </p>
        </div>
    """, unsafe_allow_html=True)

    chat_container2 = st.container()
    user_input_tab2 = st.chat_input("Tanyakan sesuatu ke Chatbot 2...")

    with chat_container2:
        for msg in st.session_state.history_tab2:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if user_input_tab2:
        st.session_state.history_tab2.append({"role": "user", "content": user_input_tab2})

        with chat_container2:
            with st.chat_message("user"):
                st.markdown(user_input_tab2)
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                response_stream = get_response_stream(user_input_tab2, "deepseek")
                for chunk in response_stream:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)

        st.session_state.history_tab2.append({"role": "assistant", "content": full_response})

# Tab 3: Chatbot 3
with tab3:
    
    st.markdown("""
        <div class="custom-info-box">
        <p class='ra-bot1'>
            Bot ini menggunakan model <i class="warna"><b>LLaMA 3 70B Versatile</b></i> dari Meta AI
        </p>
        </div>
    """, unsafe_allow_html=True)

    chat_container3 = st.container()
    user_input_tab3 = st.chat_input("Tanyakan sesuatu ke Chatbot 3...")

    with chat_container3:
        for msg in st.session_state.history_tab3:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if user_input_tab3:
        st.session_state.history_tab3.append({"role": "user", "content": user_input_tab3})

        with chat_container3:
            with st.chat_message("user"):
                st.markdown(user_input_tab3)
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                response_stream = get_response_stream(user_input_tab3, "llama3")
                for chunk in response_stream:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)

        st.session_state.history_tab3.append({"role": "assistant", "content": full_response})

st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>© 2025 by Rachmat Adriansyah</div>",
    unsafe_allow_html=True
)