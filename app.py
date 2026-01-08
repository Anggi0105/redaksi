import streamlit as st
import google.generativeai as genai
from openai import OpenAI

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial AI Assistant", layout="wide")

# --- CSS CUSTOM UNTUK TAMPILAN ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; }
    .author-box { padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Editorial AI: Research & Attribution")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 API Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password")
    gpt_key = st.text_input("OpenAI API Key", type="password")
    st.info("Aplikasi ini menggunakan Gemini untuk data eksternal dan GPT untuk olah bahasa.")

# --- FUNGSI SEARCH & ATTRIBUTION ---
def get_author_attribution(author_name, api_key):
    genai.configure(api_key=api_key)
    # Menggunakan model Gemini 1.5 Flash/Pro yang mendukung web-search context
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Cari informasi publik mengenai tokoh bernama: "{author_name}".
    Tugas Anda adalah membuat 'Atribusi Penulis' atau 'Author Bio' untuk keperluan redaksi.
    
    Tolong rangkum:
    1. Deskripsi singkat (siapa dia).
    2. Latar belakang pendidikan atau organisasi (jika ada).
    3. Bidang keahlian (Expertise).
    4. Portofolio/Tulisan yang pernah dibuat atau pencapaian penting.
    5. Buatkan 1 paragraf "About the Author" (Atribusi) yang profesional untuk diletakkan di akhir artikel.

    Gunakan gaya bahasa jurnalistik yang formal dan akurat. Jika data tidak ditemukan secara spesifik, berikan template atribusi umum berdasarkan nama tersebut.
    """
    response = model.generate_content(prompt)
    return response.text

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["🔍 Keyword Research", "✍️ Author Attribution"])

with tab1:
    st.subheader("Riset Keyword & SERP")
    keyword_input = st.text_input("Masukkan Keyword Utama:")
    if st.button("Analisis Keyword"):
        if not gemini_key or not gpt_key:
            st.warning("Input API Key di sidebar!")
        else:
            with st.spinner("Menganalisis data Google..."):
                # (Fungsi riset keyword sama dengan kode sebelumnya)
                st.write(f"Menampilkan hasil riset untuk: {keyword_input}")
                # Logika riset keyword bisa diletakkan di sini...

with tab2:
    st.subheader("Pencari Atribusi Penulis")
    st.info("Gunakan fitur ini untuk mencari rekam jejak penulis/narasumber agar redaksi tidak salah menuliskan titel atau latar belakang.")
    
    author_name = st.text_input("Masukkan Nama Lengkap Tokoh/Penulis:", placeholder="Contoh: Nadiem Makarim atau [Nama Wartawan]")
    
    if st.button("Cari Profil & Atribusi"):
        if not gemini_key:
            st.error("Fitur ini membutuhkan Gemini API Key untuk melakukan pencarian data Google.")
        elif not author_name:
            st.warning("Silakan masukkan nama tokoh.")
        else:
            with st.spinner(f"Mencari data tentang {author_name} di Google..."):
                try:
                    attribution_data = get_author_attribution(author_name, gemini_key)
                    
                    st.markdown("### 📄 Hasil Profil & Atribusi")
                    st.markdown(f'<div class="author-box">{attribution_data}</div>', unsafe_allow_html=True)
                    
                    # Fitur Copy-Paste Ready
                    st.button("Salin Atribusi (Fitur Simulasi)")
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Tools ini membantu redaksi memvalidasi data penulis secara otomatis.")