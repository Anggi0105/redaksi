import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial AI Assistant (Gemini Only)", layout="wide")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .result-box { padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Editorial AI: Research & Attribution")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 API Configuration")
    # Masukkan API Key Gemini di sini saat web sudah jalan
    gemini_key = st.text_input("Masukkan APi Di sini:, type="password")
    st.info("Website ini sekarang 100% menggunakan Google Gemini (Gratis).")
    st.markdown("[Dapatkan API Key Gratis di Sini](https://aistudio.google.com/)")

# --- FUNGSI AI (GEMINI) ---
def ask_gemini(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["🔍 Keyword Research", "✍️ Author Attribution"])

with tab1:
    st.subheader("Riset Keyword & Strategi Konten")
    keyword_input = st.text_input("Masukkan Keyword Utama (Contoh: cara memelihara kucing):")
    
    if st.button("Analisis Keyword"):
        if not gemini_key:
            st.warning("Masukkan Gemini API Key di sidebar!")
        elif not keyword_input:
            st.warning("Masukkan keyword dulu!")
        else:
            with st.spinner("Gemini sedang menganalisis tren & membuat strategi..."):
                prompt_keyword = f"""
                Analisis keyword: "{keyword_input}" untuk audience Indonesia.
                Tolong berikan:
                1. Search Intent (Kenapa orang mencari ini?).
                2. 5 Pertanyaan populer (People Also Ask).
                3. Struktur artikel (H1, H2, H3) yang SEO-friendly.
                4. Sudut pandang unik (Unique Angle) agar tulisan redaksi menonjol.
                """
                hasil_riset = ask_gemini(prompt_keyword, gemini_key)
                st.markdown("### 📊 Strategi Konten")
                st.markdown(f'<div class="result-box">{hasil_riset}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Pencari Atribusi Penulis")
    author_name = st.text_input("Masukkan Nama Lengkap Tokoh/Penulis:")
    
    if st.button("Cari Profil & Atribusi"):
        if not gemini_key:
            st.error("Masukkan Gemini API Key di sidebar!")
        elif not author_name:
            st.warning("Silakan masukkan nama tokoh.")
        else:
            with st.spinner(f"Mencari data tentang {author_name}..."):
                prompt_author = f"""
                Cari informasi publik mengenai tokoh bernama: "{author_name}".
                Buatkan ringkasan profesional untuk redaksi:
                1. Siapa dia (Bio singkat).
                2. Bidang keahlian & Latar belakang.
                3. Contoh karya atau pencapaian.
                4. Buatkan 1 paragraf 'About the Author' untuk diletakkan di akhir artikel.
                """
                hasil_atribusi = ask_gemini(prompt_author, gemini_key)
                st.markdown("### 📄 Hasil Profil & Atribusi")
                st.markdown(f'<div class="result-box">{hasil_atribusi}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 Flash")
