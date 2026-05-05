import streamlit as st
import numpy as np
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator

# ==================== TEMA AYARLARI ====================
st.set_page_config(
    page_title="Melih'in Sanal Tercümanı",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Karanlık mod
dark_mode = st.toggle("🌙 Karanlık Mod", value=False)

if dark_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #1a1a2e; color: #eee; }
        .stButton>button { background-color: #16213e; color: white; }
        .stInfo { background-color: #0f3460; }
        .stSuccess { background-color: #1a5f3f; }
        </style>
    """, unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.title("📱 Melih'in Sanal Tercümanı")
st.caption("🌍 Sanal Dünyama Hoşgeldiniz")

# ==================== DİL SEÇİMİ ====================
diller = {
    'Türkçe': 'tr',
    'İngilizce': 'en',
    'Almanca': 'de',
    'Fransızca': 'fr',
    'İspanyolca': 'es',
    'İtalyanca': 'it',
    'Portekizce': 'pt',
    'Rusça': 'ru',
    'Arapça': 'ar',
    'Çince': 'zh-CN',
    'Japonca': 'ja',
    'Korece': 'ko'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("🌍 Kaynak Dil", ['Otomatik'] + list(diller.keys()))
with col2:
    target_lang = st.selectbox("🎯 Hedef Dil", list(diller.keys()), index=1)

# ==================== OCR MODEL ====================
@st.cache_resource
def load_models():
    reader = easyocr.Reader(['en'], gpu=False, download_enabled=True)
    return reader

reader = load_models()

# ==================== KAMERA ====================
st.write("---")

st.markdown("### 🚀 Sanal Dünya Turuna Hazır Mısın?")

camera_image = st.camera_input(
    "Tura Başla",
    key="camera"
)

if camera_image is not None:
    image = Image.open(camera_image)
    img_array = np.array(image)
    
    with st.spinner("🔍 Metin okunuyor..."):
        results = reader.readtext(img_array, detail=1)
    
    if results:
        tum_metinler = []
        for bbox, text, prob in results:
            if prob >= 0.3:
                tum_metinler.append(text)
        
        if tum_metinler:
            birlesik_metin = " ".join(tum_metinler)
            
            st.success(f"✅ {len(tum_metinler)} metin bloğu bulundu!")
            
            st.write("---")
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("**📝 Orijinal Metin:**")
                st.info(birlesik_metin)
            
            with c2:
                st.markdown("**🔄 Çeviri:**")
                try:
                    src = 'auto' if source_lang == 'Otomatik' else diller[source_lang]
                    dest = diller[target_lang]
                    
                    translated = GoogleTranslator(source=src, target=dest).translate(birlesik_metin)
                    st.success(translated)
                except Exception as e:
                    st.error(f"Çeviri hatası: {str(e)}")
        else:
            st.warning("❌ Yeterince net metin bulunamadı.")
    else:
        st.warning("❌ Hiç metin bulunamadı. Daha net tutun.")

st.write("---")
st.caption("💡 Turda Karşılaştıklarını Anlamak İçin Yazıyı Netleştir")
