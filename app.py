import streamlit as st
from google import genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial AI Pro (Gemini 3)", layout="wide")

st.markdown("""
    <style>
    .result-box { padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Editorial AI: Gemini 3 Flash Edition")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Menggunakan SDK Google GenAI Terbaru")

# --- FUNGSI AI (SDK BARU) ---
def run_ai_task(prompt, api_key):
    try:
        # Inisialisasi client sesuai kode baru kamu
        client = genai.Client(api_key=api_key)
        
        # Menggunakan model Gemini 3 Flash Preview sesuai permintaanmu
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["🔍 Keyword Research", "✍️ Author Attribution"])

with tab1:
    st.subheader("Riset Keyword")
    keyword = st.text_input("Apa topik artikelnya?")
    if st.button("Analisis"):
        if not api_key_input:
            st.error("Isi API Key dulu!")
        else:
            with st.spinner("Gemini 3 sedang bekerja..."):
                res = run_ai_task(f"Buatkan SEO plan dan outline artikel untuk: {keyword}", api_key_input)
                st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Atribusi Penulis")
    name = st.text_input("Nama Penulis/Tokoh:")
    if st.button("Cari Profil"):
        if not api_key_input:
            st.error("Isi API Key dulu!")
        else:
            with st.spinner("Mencari data tokoh..."):
                res = run_ai_task(f"Cari bio singkat dan buatkan atribusi penulis untuk: {name}", api_key_input)
                st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)
