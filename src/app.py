import streamlit as st
from chatbot.chatbot import get_response_stream
import time
from src.firebase import FirebaseAuth

def app():
    # Inisialisasi Firebase Auth
    firebase_auth = FirebaseAuth()
    
    # Pastikan user sudah login
    if 'user_id' not in st.session_state or not st.session_state.user_id:
        st.warning("Sesi Anda telah berakhir. Silakan login kembali.")
        st.session_state.page = 'login'
        st.rerun()
    
    # Setup halaman
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
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar untuk opsi
    with st.sidebar:
        st.write(f"Selamat datang, **{st.session_state.username}**!")
        
        # Tombol untuk melihat riwayat chat
        if st.button("Lihat Riwayat Chat"):
            st.session_state.show_history = True
        
        # Tombol logout
        if st.button("Logout"):
            firebase_auth.logout_user()
            st.session_state.logged_in = False
            st.session_state.user_id = None
            if 'token' in st.session_state:
                del st.session_state.token
            st.session_state.page = 'login'
            st.rerun()
    
    # Tampilkan riwayat chat jika tombol ditekan
    if 'show_history' in st.session_state and st.session_state.show_history:
        show_chat_history(firebase_auth)
        return
    
    # Membuat tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Chatbot 1", "Chatbot 2", "Chatbot 3", "Chatbot 4"])
    
    # Inisialisasi history untuk setiap tab jika belum ada
    if "history_tab1" not in st.session_state:
        try:
            # Coba ambil riwayat chat dari Firestore untuk model llama4
            chat_history = firebase_auth.get_user_chat_history(st.session_state.user_id, limit=20, model_type="llama4")
            if chat_history:
                st.session_state.history_tab1 = []
                # Urutkan berdasarkan timestamp (terlama dulu)
                sorted_history = sorted(chat_history, key=lambda x: x.get('timestamp', 0) if x.get('timestamp') is not None else 0)
                for chat in sorted_history:
                    st.session_state.history_tab1.append({"role": "user", "content": chat['prompt']})
                    st.session_state.history_tab1.append({"role": "assistant", "content": chat['response']})
            else:
                st.session_state.history_tab1 = []
        except Exception as e:
            st.session_state.history_tab1 = []
            st.error(f"Error loading chat history: {e}")
    
    if "history_tab2" not in st.session_state:
        try:
            # Coba ambil riwayat chat dari Firestore untuk model deepseek
            chat_history = firebase_auth.get_user_chat_history(st.session_state.user_id, limit=20, model_type="deepseek")
            if chat_history:
                st.session_state.history_tab2 = []
                # Urutkan berdasarkan timestamp (terlama dulu)
                sorted_history = sorted(chat_history, key=lambda x: x.get('timestamp', 0) if x.get('timestamp') is not None else 0)
                for chat in sorted_history:
                    st.session_state.history_tab2.append({"role": "user", "content": chat['prompt']})
                    st.session_state.history_tab2.append({"role": "assistant", "content": chat['response']})
            else:
                st.session_state.history_tab2 = []
        except Exception as e:
            st.session_state.history_tab2 = []
            st.error(f"Error loading chat history: {e}")
            
    if "history_tab3" not in st.session_state:
        try:
            # Coba ambil riwayat chat dari Firestore untuk model llama3
            chat_history = firebase_auth.get_user_chat_history(st.session_state.user_id, limit=20, model_type="llama3")
            if chat_history:
                st.session_state.history_tab3 = []
                # Urutkan berdasarkan timestamp (terlama dulu)
                sorted_history = sorted(chat_history, key=lambda x: x.get('timestamp', 0) if x.get('timestamp') is not None else 0)
                for chat in sorted_history:
                    st.session_state.history_tab3.append({"role": "user", "content": chat['prompt']})
                    st.session_state.history_tab3.append({"role": "assistant", "content": chat['response']})
            else:
                st.session_state.history_tab3 = []
        except Exception as e:
            st.session_state.history_tab3 = []
            st.error(f"Error loading chat history: {e}")
            
    if "history_tab4" not in st.session_state:
        try:
            # Coba ambil riwayat chat dari Firestore untuk model gemini.flash
            chat_history = firebase_auth.get_user_chat_history(st.session_state.user_id, limit=20, model_type="gemini.flash")
            if chat_history:
                st.session_state.history_tab4 = []
                # Urutkan berdasarkan timestamp (terlama dulu)
                sorted_history = sorted(chat_history, key=lambda x: x.get('timestamp', 0) if x.get('timestamp') is not None else 0)
                for chat in sorted_history:
                    st.session_state.history_tab4.append({"role": "user", "content": chat['prompt']})
                    st.session_state.history_tab4.append({"role": "assistant", "content": chat['response']})
            else:
                st.session_state.history_tab4 = []
        except Exception as e:
            st.session_state.history_tab4 = []
            st.error(f"Error loading chat history: {e}")

    
    # Tab 1: Chatbot 1 (Llama 4 Maverick)
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
                    response_stream = get_response_stream(user_input_tab1, "llama4")
                    
                    # Streaming respons dan menampilkannya secara bertahap
                    for chunk in response_stream:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")  # Menambahkan indikator streaming
                    
                    # Menampilkan respons final tanpa indikator
                    response_placeholder.markdown(full_response)
            
            # Menambahkan respons AI ke riwayat percakapan tab 1
            st.session_state.history_tab1.append({"role": "assistant", "content": full_response})
            
            # Simpan ke Firestore
            firebase_auth.save_chat_history(
                user_id=st.session_state.user_id,
                model_type="llama4",
                prompt=user_input_tab1,
                response=full_response
            )
            
    # Tab 2: Chatbot 2 (Deepseek-R1)
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
            
            # Simpan ke Firestore
            firebase_auth.save_chat_history(
                user_id=st.session_state.user_id,
                model_type="deepseek",
                prompt=user_input_tab2,
                response=full_response
            )
            
    # Tab 3: Chatbot 3 (LLaMA 3 70B Versatile)
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
            
            # Simpan ke Firestore
            firebase_auth.save_chat_history(
                user_id=st.session_state.user_id,
                model_type="llama3",
                prompt=user_input_tab3,
                response=full_response
            )
            
    # Tab 4: Chatbot 4 (Gemini 2.5)       
    with tab4:
        st.markdown("""
            <div class="custom-info-box">
            <p class='ra-bot1'>
                Bot ini menggunakan model <i class="warna"><b>Gemini 2.5</b></i> dari Google
            </p>
            </div>
        """, unsafe_allow_html=True)
        chat_container4 = st.container()
        user_input_tab4 = st.chat_input("Tanyakan sesuatu ke Chatbot 4...")
        with chat_container4:
            for msg in st.session_state.history_tab4:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        if user_input_tab4:
            st.session_state.history_tab4.append({"role": "user", "content": user_input_tab4})
            with chat_container4:
                with st.chat_message("user"):
                    st.markdown(user_input_tab4)
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    full_response = ""
                    response_stream = get_response_stream(user_input_tab4, "gemini.flash")
                    for chunk in response_stream:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
            st.session_state.history_tab4.append({"role": "assistant", "content": full_response})
            
            # Simpan ke Firestore
            firebase_auth.save_chat_history(
                user_id=st.session_state.user_id,
                model_type="gemini.flash",
                prompt=user_input_tab4,
                response=full_response
            )
            
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.9em;'>© 2025 by Rachmat Adriansyah</div>",
        unsafe_allow_html=True
    )


def show_chat_history(firebase_auth):
    """
    Tampilkan riwayat chat pengguna dari Firestore
    """
    st.title("Riwayat Chat")
    
    # Pilihan filter berdasarkan model
    model_filter = st.selectbox(
        "Filter berdasarkan model:",
        ["Semua", "Llama 4 Maverick", "Deepseek-R1", "LLaMA 3 70B", "Gemini 2.5"]
    )
    
    # Konversi model yang dipilih ke model_type yang disimpan di database
    model_type_map = {
        "Semua": None,
        "Llama 4 Maverick": "llama4",
        "Deepseek-R1": "deepseek",
        "LLaMA 3 70B": "llama3",
        "Gemini 2.5": "gemini.flash"
    }
    
    selected_model_type = model_type_map[model_filter]
    
    try:
        # Ambil riwayat chat
        chat_history = firebase_auth.get_user_chat_history(
            st.session_state.user_id, 
            limit=100, 
            model_type=selected_model_type
        )
        
        if not chat_history:
            st.info("Belum ada riwayat chat.")
            if st.button("Kembali ke Chat"):
                st.session_state.show_history = False
                st.rerun()
            return
        
        # Tampilkan riwayat chat
        for i, chat in enumerate(chat_history):
            # Format timestamp jika tersedia
            timestamp_str = "unknown"
            if 'timestamp' in chat and chat['timestamp'] is not None:
                try:
                    # Jika timestamp adalah objek Firestore Timestamp
                    if hasattr(chat['timestamp'], 'seconds'):
                        import datetime
                        timestamp = datetime.datetime.fromtimestamp(chat['timestamp'].seconds)
                        timestamp_str = timestamp.strftime("%d-%m-%Y %H:%M:%S")
                    else:
                        timestamp_str = str(chat['timestamp'])
                except:
                    timestamp_str = str(chat['timestamp'])
            
            # Tampilkan informasi model
            model_display = {
                "llama4": "Llama 4 Maverick",
                "deepseek": "Deepseek-R1",
                "llama3": "LLaMA 3 70B",
                "gemini.flash": "Gemini 2.5"
            }.get(chat.get('model_type', 'unknown'), chat.get('model_type', 'unknown'))
            
            with st.expander(f"Chat {i+1} - {model_display} - {timestamp_str}"):
                st.markdown("**Pertanyaan:**")
                st.write(chat['prompt'])
                st.markdown("**Jawaban:**")
                st.write(chat['response'])
                
                # Tombol untuk menghapus chat
                if st.button(f"Hapus Chat ini", key=f"delete_{chat['chat_id']}"):
                    if firebase_auth.delete_chat(chat['chat_id']):
                        st.success("Chat berhasil dihapus!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Gagal menghapus chat.")
        
    except Exception as e:
        st.error(f"Error menampilkan riwayat chat: {e}")
        st.info("Anda mungkin perlu membuat indeks di Firebase Console sesuai dengan pesan error.")
    
    # Tombol kembali
    if st.button("Kembali ke Chat"):
        st.session_state.show_history = False
        st.rerun()