import streamlit as st
from google import genai
from datetime import datetime, timedelta

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial Intelligence 48h", layout="wide", page_icon="⚡")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .trend-card { 
        padding: 15px; border-radius: 10px; background-color: #ffffff; 
        border-left: 5px solid #FF4B4B; margin-bottom: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .result-box { padding: 25px; border-radius: 12px; background-color: #ffffff; border: 1px solid #ddd; line-height: 1.8; }
    .stButton>button { border-radius: 8px; font-weight: bold; background-color: #FF4B4B; color: white; }
    .time-badge { background-color: #ffeeee; color: #ff4b4b; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Editorial Radar: 48 Jam Terakhir")
st.markdown(f"Memantau tren viral Indonesia sejak: **{(datetime.now() - timedelta(days=2)).strftime('%d %B %Y')}**")

# --- SIDEBAR & API CONFIG ---
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.warning("Data dibatasi maksimal 2 hari terakhir untuk akurasi tren.")

def run_ai_task(prompt, api_key):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- LAYOUT UTAMA ---
col1, col2 = st.columns([1, 2.5])

with col1:
    st.subheader("🔥 Topik Naik (2 Hari Terakhir)")
    st.markdown('<span class="time-badge">REAL-TIME SCAN</span>', unsafe_allow_html=True)
    
    if st.button("🔄 Cek Tren 48 Jam Terakhir"):
        if not api_key_input:
            st.error("Input API Key dulu!")
        else:
            with st.spinner("Memindai berita & sosmed 48 jam terakhir..."):
                # PROMPT DIBATASI WAKTU
                prompt_today = f"""
                Identifikasi 7 topik yang paling viral di Indonesia HANYA dalam 2 hari terakhir (sejak {(datetime.now() - timedelta(days=2)).strftime('%d %B %Y')}).
                Sumber: Google Trends Indonesia, Trending X (Twitter), dan FYP TikTok Indonesia.
                
                Untuk setiap topik sertakan:
                1. Kenapa ini viral sekarang?
                2. Platform mana yang paling ramai membicarakannya?
                3. Apakah ini berita positif atau kontroversi/hujatan?
                """
                trends_today = run_ai_task(prompt_today, api_key_input)
                st.markdown(f'<div class="trend-card">{trends_today}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🔍 Bedah Konten & Sisi Gelap (Max 48 Jam)")
    tab1, tab2 = st.tabs(["📊 Deep Dive Research", "👤 Author Attribution"])
    
    with tab1:
        keyword = st.text_input("Topik spesifik:", placeholder="Contoh: Kasus Korupsi X, Viral TikTok Brand Y")
        
        if st.button("Analisis 48 Jam Terakhir"):
            if not api_key_input:
                st.error("Input API Key di sidebar!")
            elif not keyword:
                st.warning("Masukkan topik!")
            else:
                with st.spinner("Menganalisis percakapan netizen 2 hari terakhir..."):
                    # PROMPT KHUSUS SISI BURUK & SOSMED
                    prompt_deep = f"""
                    Bedah mendalam topik: "{keyword}" dengan data maksimal 2 hari terakhir.
                    
                    Tugas Anda:
                    1. **Update Sosmed (48 Jam)**: Apa drama/perdebatan terbaru di X dan TikTok terkait topik ini?
                    2. **Sisi Negatif & Kontroversi**: Apa keluhan netizen, sisi buruk, atau "aib" yang sedang dibongkar dalam 2 hari ini?
                    3. **People Also Ask**: Pertanyaan baru apa yang muncul di pikiran orang?
                    4. **Strategi Judul Viral**:
                       - 2 Judul Informatif (SEO).
                       - 3 Judul Sensasional/Provokatif (Gaya akun gosip/berita cepat).
                    5. **Status Tren**: Apakah tren ini masih akan naik besok atau sudah mulai turun?
                    """
                    deep_res = run_ai_task(prompt_deep, api_key_input)
                    st.markdown("### 📋 Strategi Redaksi (Data 48 Jam)")
                    st.markdown(f'<div class="result-box">{deep_res}</div>', unsafe_allow_html=True)

    with tab2:
        name = st.text_input("Nama Tokoh:")
        if st.button("Cari Profil"):
            res = run_ai_task(f"Buat bio singkat dan atribusi penulis untuk: {name}", api_key_input)
            st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)
