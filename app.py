import streamlit as st
from google import genai
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial Intelligence Dashboard", layout="wide", page_icon="📰")

# --- CSS UNTUK TAMPILAN DASHBOARD ---
st.markdown("""
    <style>
    .trend-card { 
        padding: 15px; border-radius: 10px; background-color: #ffffff; 
        border-left: 5px solid #FF4B4B; margin-bottom: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .result-box { padding: 25px; border-radius: 12px; background-color: #ffffff; border: 1px solid #ddd; line-height: 1.8; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📰 Editorial Intelligence Hub")
st.markdown(f"Pusat Riset Konten Viral - {datetime.now().strftime('%d %B %Y')}")

# --- SIDEBAR & API CONFIG ---
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Web ini menggunakan Gemini 3 Flash untuk memantau Google, TikTok, X, dan IG.")

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

# --- LAYOUT UTAMA: KOLOM KIRI (TREN HARI INI) & KOLOM KANAN (RISET) ---
col1, col2 = st.columns([1, 2.5])

with col1:
    st.subheader("🔥 Tren Naik Hari Ini")
    st.caption("Auto-scan: Google, X, & TikTok (Indonesia)")
    
    if st.button("🔄 Cek Tren Terbaru"):
        if not api_key_input:
            st.error("Input API Key dulu!")
        else:
            with st.spinner("Memindai radar..."):
                prompt_today = "Sebutkan 7 topik yang paling viral dan sedang naik daun di Indonesia hari ini (pencarian Google, trending X, dan viral TikTok). Berikan alasan singkat kenapa viral. Format dalam poin-poin singkat."
                trends_today = run_ai_task(prompt_today, api_key_input)
                st.markdown(f'<div class="trend-card">{trends_today}</div>', unsafe_allow_html=True)
    else:
        st.write("Klik tombol di atas untuk melihat apa yang sedang ramai hari ini.")

with col2:
    st.subheader("🔍 Riset Mendalam & Strategi Konten")
    tab1, tab2 = st.tabs(["📊 Deep Dive Research", "👤 Author Attribution"])
    
    with tab1:
        keyword = st.text_input("Ingin riset topik spesifik? Masukkan di sini:", placeholder="Contoh: Skandal Brand A, Larangan Ekspor B, Tren Outfit C")
        
        if st.button("Mulai Bedah Konten"):
            if not api_key_input:
                st.error("Input API Key di sidebar!")
            elif not keyword:
                st.warning("Masukkan topik untuk riset mendalam.")
            else:
                with st.spinner("Gemini sedang membedah data lintas platform..."):
                    prompt_deep = f"""
                    Bedah topik: "{keyword}" untuk tim redaksi berita.
                    
                    1. **Lanskap Media Sosial**: Apa yang dibahas netizen di TikTok (vibe/visual), X (debat/kontroversi), dan Instagram (gaya hidup/image)?
                    2. **Sisi Gelap & Kontroversi**: Berikan sisi buruk, kritik, atau hal yang memicu kemarahan/kekhawatiran netizen terkait topik ini.
                    3. **Pertanyaan Netizen**: 3 Pertanyaan yang paling banyak ditanyakan (People Also Ask).
                    4. **Strategi Judul**:
                       - 2 Judul Informatif (SEO).
                       - 3 Judul Sensasional/Provokatif (Sosmed).
                    5. **Rekomendasi Konten**: Apakah cocok dibuat video pendek, artikel listicle, atau investigasi?
                    """
                    deep_res = run_ai_task(prompt_deep, api_key_input)
                    st.markdown("### 📋 Hasil Riset Strategis")
                    st.markdown(f'<div class="result-box">{deep_res}</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("Pencari Profil Tokoh")
        name = st.text_input("Nama Penulis/Tokoh:")
        if st.button("Cari Profil"):
            res = run_ai_task(f"Buat bio singkat dan atribusi penulis profesional untuk: {name}", api_key_input)
            st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)
