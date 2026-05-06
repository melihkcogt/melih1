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

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #f5f5dc 0%, #e8f5e9 50%, #d4edda 100%); }
    .stApp, p, h1, h2, h3, label { color: #1a1a1a !important; -webkit-text-fill-color: #1a1a1a !important; }
    .baslik { font-size: 42px; font-weight: 700; color: #2e7d32 !important; text-align: center; -webkit-text-fill-color: #2e7d32 !important; }
    .altbaslik { font-size: 18px; color: #5d4037 !important; text-align: center; -webkit-text-fill-color: #5d4037 !important; }
    .stButton>button { 
        background: #2e7d32; color: white !important; border-radius: 20px; 
        padding: 12px 30px; font-size: 16px; width: 100%;
        -webkit-text-fill-color: white !important;
    }
    .stButton>button:hover { background: #1b5e20; }
    .stTextArea textarea { 
        background: white; border: 2px solid #81c784; border-radius: 15px; 
        color: #1a1a1a !important; font-size: 16px;
    }
    .stSelectbox>div>div { background: white; border-radius: 10px; border: 2px solid #81c784; }
    .kutu { background: white; border-radius: 15px; padding: 20px; margin: 10px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .sonuc-kutu { background: #e8f5e9; border-radius: 10px; padding: 15px; border-left: 4px solid #2e7d32; }
    .hata-kutu { background: #ffebee; border-radius: 10px; padding: 15px; border-left: 4px solid #c62828; }
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

with st.container():
    yazilacak_metin = st.text_area(
        "Metninizi yazın:",
        height=150,
        placeholder="Buraya yazın...",
        key="yazi_input"
    )
    
    # ENTER ile çalışan buton (form kullanarak)
    with st.form(key="yazi_form", clear_on_submit=False):
        st.text("")  # boşluk
        gonder_btn = st.form_submit_button("🚀 Çevir", use_container_width=True)
    
    if gonder_btn and yazilacak_metin.strip():
        try:
            src = 'auto' if source_lang == 'Otomatik' else DILLER.get(source_lang, 'auto')
            dest = DILLER.get(target_lang, 'tr')
            
            with st.spinner("Çevriliyor..."):
                translated = GoogleTranslator(source=src, target=dest).translate(yazilacak_metin)
            
            st.markdown('<div class="sonuc-kutu">', unsafe_allow_html=True)
            st.markdown(f"**🔄 Çeviri:**\n\n{translated}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown('<div class="hata-kutu">', unsafe_allow_html=True)
            st.error(f"Çeviri hatası: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==================== KAMERA ÇEVİRİ ====================
st.markdown("### 📷 Kamera Çevir")

# OCR modeli - hata kontrolü ile
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
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**📝 Orijinal:**")
                        st.info(birlesik_metin)
                    
                    with col_b:
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
