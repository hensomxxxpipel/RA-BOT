# ra_Chatbot

Proyek ini adalah implementasi chatbot berbasis **Groq LLM** yang digabungkan dengan **Langchain** dan **Streamlit** untuk antarmuka pengguna. Chatbot ini menggunakan pemrosesan percakapan berbasis aliran (streaming) untuk memberikan respons secara bertahap kepada pengguna.

## Fitur

- **Chatbot dengan Respons Streaming**: Respons dari chatbot ditampilkan secara bertahap seiring dengan progres streaming.
- **Penggunaan Groq LLM**: Chatbot ini menggunakan model Groq LLM untuk menghasilkan respons berbasis input pengguna.
- **Antarmuka Pengguna dengan Streamlit**: Antarmuka pengguna yang sederhana dan interaktif dengan Streamlit.
- **Penyimpanan Riwayat Percakapan**: Riwayat percakapan disimpan menggunakan `st.session_state` sehingga percakapan sebelumnya tetap bisa diakses.

## Instalasi

1. Clone repositori ini ke dalam mesin lokal Anda:
    ```bash
    git clone https://github.com/username/chatbot_project.git
    cd chatbot_project
    ```

2. Buat dan aktifkan lingkungan virtual (opsional tapi disarankan):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Linux/macOS
    venv\Scripts\activate     # Untuk Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Buat file `.env` dan tambahkan API Key yang dibutuhkan (misalnya API key untuk Groq) dalam format:
    ```
    GROQ_API_KEY=your_api_key_here
    ```

5. Jalankan aplikasi Streamlit:
    ```bash
    streamlit run app.py
    ```

## Penggunaan

Setelah aplikasi berjalan, Anda akan melihat antarmuka chatbot di browser Anda. Masukkan pertanyaan atau pesan di input chat, dan chatbot akan memberikan respons secara bertahap. Riwayat percakapan akan tersimpan selama sesi berlangsung.

## Dependencies

- `streamlit`: Untuk membangun antarmuka pengguna.
- `langchain`: Untuk mengelola alur percakapan dan integrasi dengan LLM.
- `groq`: Untuk mengakses model Groq LLM.
- `langsmith`: Untuk pengelolaan alur kerja Langchain.
- `dotenv`: Untuk memuat variabel lingkungan dari file `.env`.



