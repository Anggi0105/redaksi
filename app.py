import streamlit as st
from google import genai
from datetime import datetime, timedelta

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial Intelligence v3", layout="wide", page_icon="🔥")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .trend-card { padding: 15px; border-radius: 10px; background-color: #ffffff; border-left: 5px solid #007BFF; margin-bottom: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .result-box { padding: 25px; border-radius: 12px; background-color: #ffffff; border: 1px solid #ddd; line-height: 1.8; color: #333; }
    .stButton>button { border-radius: 8px; font-weight: bold; background-color: #007BFF; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Editorial Hub: Gemini 3 Flash Edition")
st.markdown(f"Status Data: **48 Jam Terakhir** (Sejak {(datetime.now() - timedelta(days=2)).strftime('%d %B %Y')})")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 API v3 Configuration")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.markdown("---")
    st.info("Sistem ini menggunakan **Google GenAI SDK 1.0** untuk akses langsung ke Gemini 3 Flash Preview.")

# --- FUNGSI CORE GEMINI 3 ---
def call_gemini_3(prompt, api_key):
    try:
        # Menggunakan Client baru khusus SDK v1.0
        client = genai.Client(api_key=api_key)
        
        # MEMAKSA PENGGUNAAN GEMINI 3
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gagal memanggil Gemini 3: {str(e)}"

# --- LAYOUT DASHBOARD ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📡 Radar Tren 48 Jam")
    if st.button("Pindai Tren Terbaru"):
        if not api_key_input:
            st.error("Input API Key dulu!")
        else:
            with st.spinner("Gemini 3 sedang menyisir internet..."):
                prompt_radar = f"Berikan 5 topik yang paling meledak/viral di Indonesia dalam 48 jam terakhir. Fokus pada drama X, FYP TikTok, dan Google Trends. Jelaskan sisi buruk/kontroversinya secara singkat."
                res_radar = call_gemini_3(prompt_radar, api_key_input)
                st.markdown(f'<div class="trend-card">{res_radar}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🔍 Riset Mendalam & Sisi Gelap")
    topic_input = st.text_input("Masukkan Topik Spesifik:", placeholder="Misal: Isu Kenaikan Pajak, Viral Artis X")
    
    if st.button("Bedah Strategi Redaksi"):
        if not api_key_input:
            st.error("Input API Key di sidebar!")
        elif not topic_input:
            st.warning("Masukkan topik!")
        else:
            with st.spinner("Menganalisis sisi negatif & potensi viral..."):
                prompt_deep = f"""
                Gunakan data terbaru (48 jam terakhir) untuk membedah: "{topic_input}".
                1. **Apa Sisi Buruk/Masalahnya?**: Jelaskan kritik atau kemarahan netizen saat ini.
                2. **Sentimen Sosmed**: Apa kata orang di TikTok dan X dalam 2 hari ini?
                3. **Rekomendasi Judul**: Berikan 3 judul berita yang berani/provokatif.
                4. **Celah Konten**: Apa yang belum dibahas media besar lain?
                """
                res_deep = call_gemini_3(prompt_deep, api_key_input)
                st.markdown(f'<div class="result-box">{res_deep}</div>', unsafe_allow_html=True)
