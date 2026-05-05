import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator
import time

# ==================== TEMA AYARLARI ====================
st.set_page_config(
    page_title="Kamera Tercüman Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Karanlık mod desteği
dark_mode = st.sidebar.toggle("🌙 Karanlık Mod", value=False)

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
st.title("📱 Kamera Tercüman Pro")
st.caption("Kameranızı bir yazıya tutun, anında çeviri gelsin!")

# ==================== DİL SEÇİMİ ====================
st.sidebar.header("⚙️ Ayarlar")

# Tüm diller
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

col1, col2 = st.sidebar.columns(2)
with col1:
    source_lang = st.selectbox("Kaynak Dil", ['Otomatik'] + list(diller.keys()))
with col2:
    target_lang = st.selectbox("Hedef Dil", list(diller.keys()), index=1)

# Otomatik çeviri ayarı
auto_translate = st.sidebar.toggle("⚡ Otomatik Çeviri", value=True)
interval = st.sidebar.slider("Tarama Hızı (saniye)", 1, 5, 2)

# Güven skoru
min_confidence = st.sidebar.slider("Min. Güven Skoru", 0.0, 1.0, 0.3)

# ==================== OCR MODEL ====================
@st.cache_resource
def load_models():
    # İngilizce model (en hafif ve hızlı)
    reader = easyocr.Reader(['en'], gpu=False, download_enabled=True)
    return reader

reader = load_models()

# ==================== ANA EKRAN ====================
tab1, tab2 = st.tabs(["📷 Anlık Kamera", "🖼️ Fotoğraf Yükle"])

with tab1:
    st.write("Kamerayı açın, yazıyı tutun, otomatik çeviri gelsin!")
    
    camera_image = st.camera_input(
        "Kamerayı aç",
        key="camera",
        help="Yazıyı kameraya tutun, otomatik çevireceğim!"
    )
    
    if camera_image is not None:
        # Görüntüyü işle
        image = Image.open(camera_image)
        img_array = np.array(image)
        
        with st.spinner("🔍 Metin okunuyor..."):
            results = reader.readtext(img_array, detail=1)
        
        if results:
            st.success(f"✅ {len(results)} metin bloğu bulundu!")
            
            for bbox, text, prob in results:
                if prob >= min_confidence:
                    st.write("---")
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.markdown("**📝 Orijinal:**")
                        st.info(text)
                        st.caption(f"Güven: %{prob*100:.1f}")
                    
                    with c2:
                        st.markdown("**🔄 Çeviri:**")
                        try:
                            src = 'auto' if source_lang == 'Otomatik' else diller[source_lang]
                            dest = diller[target_lang]
                            
                            translated = GoogleTranslator(source=src, target=dest).translate(text)
                            st.success(translated)
                        except Exception as e:
                            st.error(f"Çeviri hatası: {str(e)}")
        else:
            st.warning("❌ Metin bulunamadı. Daha net tutun veya daha fazla ışık sağlayın.")

with tab2:
    st.write("Galeriden fotoğraf yükleyin:")
    uploaded_file = st.file_uploader("Fotoğraf seç", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        with st.spinner("🔍 Metin okunuyor..."):
            results = reader.readtext(img_array, detail=1)
        
        if results:
            st.success(f"✅ {len(results)} metin bloğu bulundu!")
            
            for bbox, text, prob in results:
                if prob >= min_confidence:
                    st.write("---")
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.markdown("**📝 Orijinal:**")
                        st.info(text)
                    
                    with c2:
                        st.markdown("**🔄 Çeviri:**")
                        try:
                            src = 'auto' if source_lang == 'Otomatik' else diller[source_lang]
                            dest = diller[target_lang]
                            
                            translated = GoogleTranslator(source=src, target=dest).translate(text)
                            st.success(translated)
                        except Exception as e:
                            st.error(f"Çeviri hatası: {str(e)}")
        else:
            st.warning("❌ Metin bulunamadı.")

# ==================== BİLGİ ====================
st.sidebar.write("---")
st.sidebar.caption("💡 İpucu: Daha iyi sonuç için yazıyı net tutun ve yeterli ışık sağlayın.")
st.sidebar.caption("🔄 Otomatik çeviri açıkken her fotoğraf otomatik işlenir.")
