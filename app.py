import streamlit as st
import numpy as np
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator

# ==================== MODERN TEMA ====================
st.set_page_config(
    page_title="Melih'in Sanal Tercümanı",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS
st.markdown("""
    <style>
    /* Gradient arka plan */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Karanlık mod için */
    .dark .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Kart stili */
    .modern-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Başlık stili */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-size: 18px;
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Buton stili */
    .stButton>button {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100%;
    }
    
    /* Dil seçim kutusu */
    .stSelectbox>div>div {
        background: white;
        border-radius: 15px;
        border: 2px solid rgba(255,255,255,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Karanlık mod
dark_mode = st.toggle("🌙 Karanlık Mod", value=False)

# ==================== BAŞLIK ====================
st.markdown('<div class="main-title">📱 Melih\'in Sanal Tercümanı</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🌍 Sanal Dünyama Hoşgeldiniz</div>', unsafe_allow_html=True)

# ==================== DİL KARTI ====================
with st.container():
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    
    diller = {
        'Türkçe': 'tr', 'İngilizce': 'en', 'Almanca': 'de',
        'Fransızca': 'fr', 'İspanyolca': 'es', 'İtalyanca': 'it',
        'Portekizce': 'pt', 'Rusça': 'ru', 'Arapça': 'ar',
        'Çince': 'zh-CN', 'Japonca': 'ja', 'Korece': 'ko'
    }
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("🌍 Kaynak Dil", ['Otomatik'] + list(diller.keys()))
    with col2:
        target_lang = st.selectbox("🎯 Hedef Dil", list(diller.keys()), index=1)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== OCR MODEL ====================
@st.cache_resource
def load_models():
    reader = easyocr.Reader(['en'], gpu=False, download_enabled=True)
    return reader

reader = load_models()

# ==================== KAMERA KARTI ====================
with st.container():
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Sanal Dünya Turuna Hazır Mısın?")
    
    camera_image = st.camera_input(
        "Tura Başla",
        key="camera"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== SONUÇ KARTI ====================
if camera_image is not None:
    with st.container():
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.write("---")
st.caption("💡 Turda Karşılaştıklarını Anlamak İçin Yazıyı Netleştir")
