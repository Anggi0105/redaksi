import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial AI Assistant Pro", layout="wide", page_icon="🚀")

# --- CSS CUSTOM UNTUK TAMPILAN ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        background-color: #ffffff; 
        border-radius: 8px; 
        border: 1px solid #ddd;
        font-weight: bold;
    }
    .result-box { 
        padding: 25px; 
        border: 1px solid #e0e0e0; 
        border-radius: 12px; 
        background-color: #ffffff; 
        line-height: 1.8;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Editorial AI: Research & Attribution (Pro Version)")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # Cek apakah API Key sudah ada di Secrets, jika tidak pakai Text Input
    if "GEMINI_API_KEY" in st.secrets:
        gemini_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key terdeteksi otomatis dari Secrets!")
    else:
        gemini_key = st.text_input("Masukkan Gemini API Key:", type="password")
        st.info("Dapatkan API Key di [Google AI Studio](https://aistudio.google.com/)")
    
    st.divider()
    st.markdown("### Mode: **Gemini 1.5 Pro**")
    st.caption("Akurasi tinggi untuk riset mendalam.")

# --- FUNGSI AI (OPTIMAL UNTUK PRO) ---
def ask_gemini_pro(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        # Menggunakan model 1.5 Pro untuk hasil terbaik
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan teknis: {str(e)}"

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["🔍 Keyword Research", "✍️ Author Attribution"])

with tab1:
    st.subheader("Riset Keyword & Strategi Konten")
    keyword_input = st.text_input("Topik yang ingin diriset:", placeholder="Contoh: Manfaat AI untuk jurnalisme")
    
    if st.button("Jalankan Analisis Pro"):
        if not gemini_key:
            st.warning("Silakan masukkan API Key di sidebar!")
        elif not keyword_input:
            st.warning("Isi topiknya terlebih dahulu.")
        else:
            with st.spinner("Analisis mendalam sedang berlangsung..."):
                prompt_keyword = f"""
                Bertindaklah sebagai SEO Expert & Editor Senior. Analisis topik: "{keyword_input}".
                Berikan riset komprehensif:
                1. **Analisis Intent**: Mengapa orang mencari ini?
                2. **Kompetisi Konten**: Apa yang biasanya terlewatkan oleh kompetitor?
                3. **Struktur Konten (H1, H2, H3)**: Buat outline yang logis dan memikat.
                4. **Keyword LSI & Entitas**: Daftar kata yang harus ada agar relevansi SEO tinggi.
                5. **Unique Angle**: Satu sudut pandang berita agar viral.
                """
                hasil = ask_gemini_pro(prompt_keyword, gemini_key)
                st.markdown("### 📊 Hasil Riset Strategis")
                st.markdown(f'<div class="result-box">{hasil}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Pencari Atribusi Penulis & Tokoh")
    author_name = st.text_input("Nama Tokoh/Penulis yang dicari:")
    
    if st.button("Cari Profil Lengkap"):
        if not gemini_key:
            st.error("API Key dibutuhkan.")
        elif not author_name:
            st.warning("Masukkan nama tokoh.")
        else:
            with st.spinner(f"Menghimpun data publik tentang {author_name}..."):
                prompt_author = f"""
                Kumpulkan informasi kredibel tentang tokoh: "{author_name}".
                Format sebagai berikut:
                - **Profil Singkat**: Siapa tokoh ini?
                - **Keahlian Utama**: Spesialisasi dan latar belakang industri.
                - **Kredibilitas**: Organisasi, pendidikan, atau karya yang pernah dibuat.
                - **Atribusi (Siap Pakai)**: Tulis satu paragraf biografi singkat untuk bagian akhir artikel.
                """
                hasil_atribusi = ask_gemini_pro(prompt_author, gemini_key)
                st.markdown("### 📄 Profil & Atribusi Penulis")
                st.markdown(f'<div class="result-box">{hasil_atribusi}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Editorial AI Pro System | Google Gemini 1.5 Pro Engine")
