import streamlit as st
import numpy as np
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator
import io

# ==================== DİL VERİSİ ====================
DILLER = {
    'Türkçe': 'tr', 'İngilizce': 'en', 'Almanca': 'de',
    'Fransızca': 'fr', 'İspanyolca': 'es', 'İtalyanca': 'it',
    'Portekizce': 'pt', 'Rusça': 'ru', 'Arapça': 'ar',
    'Çince': 'zh-CN', 'Japonca': 'ja', 'Korece': 'ko'
}

st.set_page_config(page_title="Melih'in Sanal Tercümanı", layout="wide")

# ==================== TEMİZ CSS - PC UYUMLU ====================
st.markdown("""
    <style>
    /* ARKA PLAN */
    .stApp {
        background: linear-gradient(180deg, #f5f5dc 0%, #e8f5e9 50%, #d4edda 100%);
    }
    
    /* TÜM YAZILAR SİYAH VE NET */
    body, .stApp, p, h1, h2, h3, h4, h5, h6, 
    label, .stMarkdown, .stText, div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* BAŞLIK */
    .baslik {
        font-size: 42px;
        font-weight: 700;
        color: #1b5e20 !important;
        text-align: center;
        margin-bottom: 5px;
        -webkit-text-fill-color: #1b5e20 !important;
    }
    
    .altbaslik {
        font-size: 18px;
        color: #5d4037 !important;
        text-align: center;
        margin-bottom: 20px;
        -webkit-text-fill-color: #5d4037 !important;
    }
    
    /* SEÇİM KUTULARI */
    .stSelectbox label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: bold;
        font-size: 16px;
    }
    
    .stSelectbox>div>div {
        background: #ffffff;
        border: 2px solid #4caf50;
        border-radius: 10px;
    }
    
    /* SLIDER */
    .stSlider label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: bold;
    }
    
    .stSlider div[data-testid="stThumbValue"] {
        color: #1b5e20 !important;
        -webkit-text-fill-color: #1b5e20 !important;
        font-weight: bold;
    }
    
    /* BUTON - SADE VE NET */
    .stButton>button {
        background: #2e7d32;
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        -webkit-text-fill-color: #ffffff !important;
        transition: none !important;
    }
    
    .stButton>button:hover {
        background: #1b5e20;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* TEXT AREA */
    .stTextArea label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: bold;
        font-size: 16px;
    }
    
    .stTextArea textarea {
        background: #ffffff;
        border: 2px solid #4caf50;
        border-radius: 10px;
        color: #000000 !important;
        font-size: 16px;
    }
    
    /* SONUÇ KUTULARI */
    .stInfo {
        background: #e8f5e9;
        border: 1px solid #4caf50;
        border-radius: 10px;
    }
    
    .stInfo p, .stInfo div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stSuccess {
        background: #c8e6c9;
        border: 1px solid #4caf50;
        border-radius: 10px;
    }
    
    .stSuccess p, .stSuccess div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stWarning {
        background: #fff9c4;
        border: 1px solid #fbc02d;
        border-radius: 10px;
    }
    
    .stWarning p, .stWarning div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* SEKMELER */
    .stTabs [data-baseweb="tab-list"] button {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: bold;
        font-size: 16px;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #1b5e20 !important;
        -webkit-text-fill-color: #1b5e20 !important;
        border-bottom: 3px solid #1b5e20 !important;
    }
    
    /* CAPTION */
    .stCaption {
        color: #5d4037 !important;
        -webkit-text-fill-color: #5d4037 !important;
    }
    
    /* KAMERA INPUT LABEL */
    .stCameraInput label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown('<div class="baslik">🌿 Melih\'in Sanal Tercümanı</div>', unsafe_allow_html=True)
st.markdown('<div class="altbaslik">🍃 Sanal Dünyama Hoşgeldiniz</div>', unsafe_allow_html=True)
st.markdown("---")

# ==================== DİL SEÇİMİ ====================
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("🌍 Kaynak Dil", ['Otomatik'] + list(DILLER.keys()), key="src")
with col2:
    target_lang = st.selectbox("🎯 Hedef Dil", list(DILLER.keys()), index=1, key="tgt")

min_confidence = st.slider("🔍 Min. Güven Skoru", 0.0, 1.0, 0.3)

st.markdown("---")

# ==================== YAZI ÇEVİRİ ====================
st.markdown("### ✍️ Yazı Çevir")

yazilacak_metin = st.text_area(
    "Metninizi yazın:",
    height=150,
    placeholder="Buraya yazın...",
    key="yazi_input"
)

# BUTON - ANLAMSIZ KUTU YOK, DOĞRUDAN BUTON
if st.button("🚀 Çevir", use_container_width=True, key="cevir_btn"):
    if yazilacak_metin.strip():
        try:
            src = 'auto' if source_lang == 'Otomatik' else DILLER.get(source_lang, 'auto')
            dest = DILLER.get(target_lang, 'tr')
            
            with st.spinner("Çevriliyor..."):
                translated = GoogleTranslator(source=src, target=dest).translate(yazilacak_metin)
            
            # SONUÇ - KUTUSUZ, DOĞRUDAN GÖSTER
            st.markdown("**📝 Orijinal:**")
            st.info(yazilacak_metin)
            
            st.markdown("**🔄 Çeviri:**")
            st.success(translated)
            
        except Exception as e:
            st.error(f"Çeviri hatası: {str(e)}")
    else:
        st.warning("Lütfen çevrilecek metin yazın.")

st.markdown("---")

# ==================== KAMERA ÇEVİRİ ====================
st.markdown("### 📷 Kamera Çevir")

# OCR modeli
try:
    @st.cache_resource
    def get_reader():
        return easyocr.Reader(['en'], gpu=False, download_enabled=True)
    
    reader = get_reader()
    ocr_hazir = True
except Exception as e:
    st.error(f"OCR yüklenemedi: {str(e)}")
    ocr_hazir = False

if ocr_hazir:
    camera_image = st.camera_input("Fotoğraf çekin", key="kamera")
    
    if camera_image is not None:
        try:
            with st.spinner("Metin okunuyor..."):
                image = Image.open(camera_image)
                img_array = np.array(image)
                results = reader.readtext(img_array, detail=1)
            
            if results:
                tum_metinler = []
                for bbox, text, prob in results:
                    if prob >= min_confidence:
                        tum_metinler.append(text)
                
                if tum_metinler:
                    birlesik_metin = " ".join(tum_metinler)
                    
                    st.success(f"✅ {len(tum_metinler)} metin bulundu")
                    
                    st.markdown("**📝 Orijinal:**")
                    st.info(birlesik_metin)
                    
                    st.markdown("**🔄 Çeviri:**")
                    try:
                        src = 'auto' if source_lang == 'Otomatik' else DILLER.get(source_lang, 'auto')
                        dest = DILLER.get(target_lang, 'tr')
                        translated = GoogleTranslator(source=src, target=dest).translate(birlesik_metin)
                        st.success(translated)
                    except Exception as e:
                        st.error(f"Çeviri hatası: {str(e)}")
                else:
                    st.warning("Yeterince net metin bulunamadı.")
            else:
                st.warning("Hiç metin bulunamadı. Daha net çekin.")
                
        except Exception as e:
            st.error(f"Kamera işleme hatası: {str(e)}")

st.markdown("---")
st.caption("🌿 Turda Karşılaştıklarını Anlamak İçin Yazıyı Netleştir")
