import streamlit as st
from chatbot.chatbot import get_response_stream
import time

# Setup halaman
st.set_page_config(page_title="RA-Bot", layout="wide")
st.title("🤖 RA-Bot merupakan Chatbot yang menggunakan berbagai model llm.")

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
    st.header("Chatbot 1")
    # st.markdown
    
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
                response_stream = get_response_stream(user_input_tab1)
                
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
    st.header("Chatbot 2")
    st.info("Chatbot 2 menggunakan model alternatif yang akan diimplementasikan.")
    
    # Buat container untuk chat messages
    chat_container2 = st.container()
    
    # Buat input di bagian bawah
    user_input_tab2 = st.chat_input("Tanyakan sesuatu ke Chatbot 2...")
    
    # Tampilkan percakapan sebelumnya untuk tab 2
    with chat_container2:
        for msg in st.session_state.history_tab2:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if user_input_tab2:
        # Menambahkan pesan pengguna ke riwayat tab 2
        st.session_state.history_tab2.append({"role": "user", "content": user_input_tab2})
        
        # Menampilkan pesan pengguna terbaru dalam container
        with chat_container2:
            with st.chat_message("user"):
                st.markdown(user_input_tab2)
        
            # Placeholder untuk implementasi model chatbot 2
            with st.chat_message("assistant"):
                st.markdown("Chatbot 2 akan segera diimplementasikan. Ini adalah respons placeholder.")
        
        # Menambahkan respons placeholder ke riwayat percakapan tab 2
        st.session_state.history_tab2.append({"role": "assistant", "content": "Chatbot 2 akan segera diimplementasikan. Ini adalah respons placeholder."})

# Tab 3: Chatbot 3
with tab3:
    st.header("Chatbot 3")
    st.info("Chatbot 3 menggunakan model alternatif yang akan diimplementasikan.")
    
    # Buat container untuk chat messages
    chat_container3 = st.container()
    
    # Buat input di bagian bawah
    user_input_tab3 = st.chat_input("Tanyakan sesuatu ke Chatbot 3...")
    
    # Tampilkan percakapan sebelumnya untuk tab 3
    with chat_container3:
        for msg in st.session_state.history_tab3:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if user_input_tab3:
        # Menambahkan pesan pengguna ke riwayat tab 3
        st.session_state.history_tab3.append({"role": "user", "content": user_input_tab3})
        
        # Menampilkan pesan pengguna terbaru dalam container
        with chat_container3:
            with st.chat_message("user"):
                st.markdown(user_input_tab3)
        
            # Placeholder untuk implementasi model chatbot 3
            with st.chat_message("assistant"):
                st.markdown("Chatbot 3 akan segera diimplementasikan. Ini adalah respons placeholder.")
        
        # Menambahkan respons placeholder ke riwayat percakapan tab 3
        st.session_state.history_tab3.append({"role": "assistant", "content": "Chatbot 3 akan segera diimplementasikan. Ini adalah respons placeholder."})

st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>© 2025 by Rachmat Adriansyah</div>",
    unsafe_allow_html=True
)