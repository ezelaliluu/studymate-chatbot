"""
StudyMate - Asisten Belajar AI
Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists (Hacktiv8)

Chatbot berbasis Gemini API dengan parameter kreatif yang bisa dikonfigurasi:
- Gaya bahasa (formal / santai)
- Domain pengetahuan (mapel/topik fokus)
- Tingkat kreativitas jawaban (temperature)
- Fitur memory percakapan (context window)
- Fitur rekomendasi topik belajar lanjutan
"""

import os
import streamlit as st
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # membaca GEMINI_API_KEY dari file .env jika tersedia

# -----------------------------
# KONFIGURASI HALAMAN
# -----------------------------
st.set_page_config(
    page_title="StudyMate - Asisten Belajar AI",
    page_icon="📚",
    layout="wide",
)

# -----------------------------
# PERSONA / SYSTEM PROMPT BUILDER
# -----------------------------
GAYA_BAHASA_PROMPTS = {
    "Santai": (
        "Gunakan gaya bahasa santai, ramah, dan seperti teman belajar. "
        "Boleh pakai emoji sesekali dan bahasa sehari-hari, tapi tetap sopan."
    ),
    "Formal": (
        "Gunakan gaya bahasa formal, sopan, dan terstruktur seperti guru/tutor profesional. "
        "Hindari emoji dan bahasa gaul."
    ),
}

DOMAIN_PROMPTS = {
    "Umum (Semua Mapel)": "Kamu bisa membantu berbagai mata pelajaran secara umum.",
    "Matematika": "Fokuskan keahlianmu pada Matematika (aljabar, geometri, kalkulus dasar, statistika).",
    "Sains (IPA)": "Fokuskan keahlianmu pada Fisika, Kimia, dan Biologi tingkat sekolah/dasar kuliah.",
    "Pemrograman & Data Science": "Fokuskan keahlianmu pada pemrograman, algoritma, dan konsep dasar data science.",
    "Bahasa Inggris": "Fokuskan keahlianmu membantu belajar tata bahasa, kosakata, dan latihan percakapan Bahasa Inggris.",
}

BASE_SYSTEM_PROMPT = """Kamu adalah StudyMate, asisten belajar AI yang membantu siswa/mahasiswa memahami materi pelajaran.

Tugasmu:
1. Menjawab pertanyaan seputar materi belajar dengan jelas dan mudah dipahami.
2. Memberikan contoh atau analogi bila membantu pemahaman.
3. Jika relevan, di akhir jawaban berikan 1-2 REKOMENDASI topik lanjutan yang bisa dipelajari siswa berikutnya,
   diawali dengan label "💡 Rekomendasi topik lanjutan:".
4. Ingat konteks percakapan sebelumnya dalam sesi ini untuk memberi jawaban yang nyambung.
5. Jika pertanyaan di luar topik belajar/edukasi, tetap jawab dengan ramah tapi arahkan kembali ke konteks belajar.

Gaya bahasa: {gaya_bahasa}
Domain fokus: {domain}
"""


def build_system_prompt(gaya_bahasa: str, domain: str) -> str:
    return BASE_SYSTEM_PROMPT.format(
        gaya_bahasa=GAYA_BAHASA_PROMPTS[gaya_bahasa],
        domain=DOMAIN_PROMPTS[domain],
    )


# -----------------------------
# PENGATURAN TEKNIS (FIXED, TIDAK DITAMPILKAN DI UI)
# -----------------------------
# Ambil API key dari environment variable / file .env (lihat .env.example).
# Tidak lagi diminta lewat UI agar sidebar lebih ringkas.
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Nilai default teknis — sudah dituning dan tidak perlu diubah-ubah oleh user.
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_MODEL = "gemini-3.8-flash"

# -----------------------------
# SIDEBAR - KONFIGURASI PARAMETER
# -----------------------------
with st.sidebar:
    st.title("⚙️ Konfigurasi Chatbot")
    st.subheader("Parameter Kreatif")

    gaya_bahasa = st.selectbox("Gaya Bahasa", list(GAYA_BAHASA_PROMPTS.keys()))
    domain = st.selectbox("Domain Pengetahuan", list(DOMAIN_PROMPTS.keys()))

    st.divider()
    if st.button("🗑️ Hapus Riwayat Percakapan (Memory)", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

    st.caption("Dibuat untuk Final Project Hacktiv8 — LLM-Based Tools & Gemini API Integration")

temperature = DEFAULT_TEMPERATURE
max_tokens = DEFAULT_MAX_TOKENS
model_name = DEFAULT_MODEL

# -----------------------------
# INISIALISASI SESSION STATE (MEMORY)
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "last_config" not in st.session_state:
    st.session_state.last_config = None

current_config = (gaya_bahasa, domain, temperature, max_tokens, model_name)

# -----------------------------
# HEADER
# -----------------------------
st.title("📚 StudyMate - Asisten Belajar AI")
st.caption(
    f"Use case: **Education Bot** · Gaya: **{gaya_bahasa}** · "
    f"Domain: **{domain}** · Model: `{model_name}`"
)

if not API_KEY:
    st.error(
        "⚠️ GEMINI_API_KEY belum diset. Buat file `.env` (lihat `.env.example`) "
        "berisi `GEMINI_API_KEY=your_api_key`, lalu jalankan ulang aplikasi."
    )
    st.stop()

genai.configure(api_key=API_KEY)

# Re-init chat session bila konfigurasi berubah (agar system prompt terbarui)
if st.session_state.chat_session is None or st.session_state.last_config != current_config:
    system_prompt = build_system_prompt(gaya_bahasa, domain)
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        },
    )
    # Bangun ulang history Gemini dari memory percakapan yang sudah ada
    gemini_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    st.session_state.chat_session = model.start_chat(history=gemini_history)
    st.session_state.last_config = current_config

# -----------------------------
# TAMPILKAN RIWAYAT CHAT
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "time" in msg:
            st.caption(msg["time"])

# -----------------------------
# INPUT USER
# -----------------------------
user_input = st.chat_input("Tanyakan sesuatu tentang materi belajarmu...")

if user_input:
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "time": timestamp}
    )
    with st.chat_message("user"):
        st.markdown(user_input)
        st.caption(timestamp)

    with st.chat_message("assistant"):
        with st.spinner("StudyMate sedang berpikir..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)

                # Cek dulu apakah ada kandidat jawaban yang valid sebelum
                # mengakses response.text (agar tidak crash bila jawaban
                # terpotong / kosong, misalnya karena limit token tercapai).
                finish_reason = None
                if response.candidates:
                    finish_reason = response.candidates[0].finish_reason

                if not response.candidates or not response.candidates[0].content.parts:
                    if finish_reason == 2:  # MAX_TOKENS
                        answer = (
                            "⚠️ Jawaban terpotong karena mencapai batas panjang output. "
                            "Coba ajukan pertanyaan yang lebih spesifik/singkat, atau perbesar "
                            "`DEFAULT_MAX_TOKENS` di `app.py`."
                        )
                    else:
                        answer = (
                            "⚠️ Model tidak mengembalikan jawaban (kemungkinan diblokir filter "
                            f"keamanan). finish_reason: {finish_reason}"
                        )
                else:
                    answer = response.text
            except Exception as e:
                answer = f"⚠️ Terjadi kesalahan saat memanggil Gemini API: {e}"
        st.markdown(answer)
        reply_time = datetime.now().strftime("%H:%M")
        st.caption(reply_time)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "time": reply_time}
    )