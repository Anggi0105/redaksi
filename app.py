import streamlit as st
from google import genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial AI Pro (Gemini 3)", layout="wide")

st.markdown("""
    <style>
    .result-box { padding: 25px; border: 1px solid #ddd; border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Editorial AI: Gemini 3 Trends & SEO Edition")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Menggunakan SDK Google GenAI Terbaru & Model Gemini 3 Flash Preview.")

# --- FUNGSI AI (SDK BARU) ---
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

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["🔥 Google Trends & Keyword", "✍️ Author Attribution"])

with tab1:
    st.subheader("Riset Tren & Rekomendasi Judul")
    keyword = st.text_input("Apa topik atau keyword yang ingin diriset?", placeholder="Contoh: Mobil Listrik, Investasi, Kuliner")
    
    if st.button("Analisis Tren & Buat Judul Viral"):
        if not api_key_input:
            st.error("Silakan isi API Key di sidebar terlebih dahulu!")
        elif not keyword:
            st.warning("Masukkan kata kunci pencarian.")
        else:
            with st.spinner("Sedang memproses tren terbaru dari Google..."):
                prompt_trends = f"""
                Bertindaklah sebagai Editor SEO Senior dan Analis Tren.
                Topik: "{keyword}"
                
                Tugas Anda:
                1. **Analisis Tren Terkini**: Berdasarkan data Google Trends terbaru di Indonesia, apa yang sedang ramai dibahas terkait topik ini?
                2. **Rekomendasi 5 Judul Viral**: Buatkan 5 pilihan judul artikel yang "Click-worthy" (memancing klik) tapi tetap SEO-friendly (mengandung keyword).
                3. **Sudut Pandang (Angle)**: Berikan satu sudut pandang unik yang belum banyak dibahas kompetitor agar artikel ini masuk ke Google Discover.
                4. **Outline Singkat**: Berikan poin-poin H2 dan H3 yang harus ada dalam artikel.
                
                Gunakan gaya bahasa profesional dan berikan insight yang tajam.
                """
                res = run_ai_task(prompt_trends, api_key_input)
                st.markdown("### 📊 Hasil Riset Tren & SEO")
                st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Pencari Profil & Atribusi")
    name = st.text_input("Nama Penulis/Tokoh untuk Atribusi:")
    if st.button("Cari Data Tokoh"):
        if not api_key_input:
            st.error("Isi API Key dulu!")
        else:
            with st.spinner("Mencari data valid di Google..."):
                res = run_ai_task(f"Cari bio lengkap, latar belakang, dan buatkan 1 paragraf atribusi penulis untuk: {name}", api_key_input)
                st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Editorial Intelligence Hub | Powered by Gemini 3 Flash Preview SDK 1.0")
