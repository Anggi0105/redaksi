import streamlit as st
from google import genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Editorial AI: Social Media & Trends", layout="wide")

st.markdown("""
    <style>
    .result-box { padding: 25px; border: 1px solid #ddd; border-radius: 12px; background-color: #ffffff; line-height: 1.8; }
    .negative-box { background-color: #fff5f5; border-left: 5px solid #ff4b4b; padding: 15px; margin-top: 10px; border-radius: 5px; }
    .stButton>button { border-radius: 8px; font-weight: bold; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Editorial Viral Intelligence")
st.markdown("Analisis Tren Google, TikTok, X, dan Instagram menggunakan **Gemini 3 Flash**")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Pastikan API Key Anda aktif di Google AI Studio.")

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

# --- INTERFACE ---
tab1, tab2 = st.tabs(["📊 Trend & Social Media Radar", "👤 Author Attribution"])

with tab1:
    keyword = st.text_input("Topik yang ingin dibedah:", placeholder="Contoh: Brand Skincare X, Kebijakan Pemerintah, Tren Diet")
    
    if st.button("Bedah Tren Viral"):
        if not api_key_input:
            st.error("Input API Key di sidebar!")
        elif not keyword:
            st.warning("Masukkan topik!")
        else:
            with st.spinner("Sedang memindai tren di Google, TikTok, X, dan IG..."):
                prompt_viral = f"""
                Analisis mendalam topik: "{keyword}" untuk audiens Indonesia.
                
                1. **Google Trends & Questions**: Apa pertanyaan spesifik (People Also Ask) yang paling banyak dicari orang?
                2. **Social Media Radar (TikTok, X, Instagram)**: 
                   - Apa yang sedang dibahas di TikTok (misal: challenge, sound, atau review jujur)?
                   - Apa sentimen di X/Twitter (misal: perdebatan atau drama)?
                   - Gaya visual apa yang sedang tren di Instagram terkait ini?
                3. **Sisi Negatif & Kontroversi**: Jangan hanya berikan yang baik. Apa keluhan, kritik, atau potensi masalah (sisi buruk) terkait topik ini yang bisa dijadikan bahan berita?
                4. **Rekomendasi 5 Judul**: 
                   - 2 Judul Informatif (SEO).
                   - 3 Judul Sensasional/Clickbait (untuk Sosmed).
                5. **Daftar Hashtag**: Berikan hashtag paling relevan untuk X dan Instagram.
                """
                res = run_ai_task(prompt_viral, api_key_input)
                st.markdown("### 📋 Hasil Analisis Viral")
                st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Pencari Profil & Atribusi")
    name = st.text_input("Nama Penulis/Tokoh:")
    if st.button("Cari Data"):
        res = run_ai_task(f"Cari bio lengkap dan buatkan atribusi penulis profesional untuk: {name}", api_key_input)
        st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)
