# 📚 StudyMate — Asisten Belajar AI

Final Project: **LLM-Based Tools and Gemini API Integration for Data Scientists** (Hacktiv8)

Chatbot berbasis AI (Gemini API) yang membantu siswa/mahasiswa belajar berbagai mata pelajaran
dengan gaya bahasa dan domain pengetahuan yang bisa dikustomisasi.

## 🎯 Use Case
**Education Bot** — asisten belajar personal yang menjawab pertanyaan seputar materi pelajaran,
memberi penjelasan yang mudah dipahami, dan merekomendasikan topik lanjutan untuk dipelajari.

## ✨ Parameter Kreatif yang Dikonfigurasi
| Parameter | Deskripsi |
|---|---|
| **Gaya Bahasa** | Santai (seperti teman belajar) atau Formal (seperti tutor profesional) |
| **Domain Pengetahuan** | Umum, Matematika, Sains (IPA), Pemrograman & Data Science, Bahasa Inggris |

Parameter teknis (temperature, max output tokens, model Gemini) sudah di-set default di dalam
kode (`app.py`) agar sidebar tetap ringkas dan fokus ke parameter yang relevan untuk pengguna akhir.
Nilai default: `temperature=0.7`, `max_output_tokens=512`, `model=gemini-3.8-flash`. Ubah konstanta
`DEFAULT_TEMPERATURE`, `DEFAULT_MAX_TOKENS`, `DEFAULT_MODEL` di `app.py` jika ingin menyesuaikan.

## 🧠 Fitur Tambahan
- **Memory percakapan**: bot mengingat konteks chat sebelumnya dalam satu sesi (menggunakan
  `session_state` + Gemini `start_chat` history), sehingga jawaban tetap nyambung dengan
  pertanyaan-pertanyaan sebelumnya.
- **Rekomendasi topik lanjutan**: setiap jawaban relevan disertai saran topik belajar berikutnya
  (💡 Rekomendasi topik lanjutan).
- **Reset memory**: tombol di sidebar untuk menghapus riwayat percakapan kapan saja.

## 🛠️ Tech Stack
- **Python 3.9+**
- **Streamlit** — UI chatbot interaktif
- **Gemini API** (`google-generativeai`) — model LLM

## 🚀 Cara Menjalankan

1. Clone repository ini:
   ```bash
   git clone <URL_REPO_ANDA>
   cd studymate-chatbot
   ```

2. Buat virtual environment (opsional tapi disarankan):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Dapatkan Gemini API Key gratis di [Google AI Studio](https://aistudio.google.com/app/apikey),
   lalu salin `.env.example` menjadi `.env` dan isi:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Aplikasi otomatis membaca API key dari file `.env` ini — tidak perlu diinput lagi di UI.

5. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

6. Buka browser ke `http://localhost:8501`.

## 📁 Struktur Proyek
```
studymate-chatbot/
├── app.py              # Aplikasi utama chatbot (Streamlit + Gemini API)
├── requirements.txt    # Daftar dependencies
├── .env.example         # Contoh file environment variable
├── .gitignore
└── README.md
```

## 📸 Screenshot
Lihat folder `screenshots/` atau bagian submission untuk tangkapan layar antarmuka aplikasi.

## 👤 Author
Final Project — Hacktiv8 Data Science Program