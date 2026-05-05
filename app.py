import streamlit as st
import numpy as np
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator

# ==================== DOĞA TEMASI ====================
st.set_page_config(
    page_title="Melih'in Sanal Tercümanı",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Doğa renkleri CSS
st.markdown("""
    <style>
    /* Yumuşak yeşil-bej arka plan */
    .stApp {
        background: linear-gradient(180deg, #f5f5dc 0%, #e8f5e9 50%, #d4edda 100%);
    }
    
    /* Başlık - Orman yeşili */
    .nature-title {
        font-size: 44px;
        font-weight: 700;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Georgia', serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Alt başlık - Toprak rengi */
    .nature-subtitle {
        font-size: 18px;
        color: #795548;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Georgia', serif;
    }
    
    /* Doğa kartı - Beyaz, yumuşak gölge */
    .nature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.15);
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    
    /* Kamera kartı - Açık yeşil ton */
    .camera-card {
        background: rgba(232, 245, 233, 0.9);
        border: 2px solid #81c784;
        box-shadow: 0 4px 20px rgba(129, 199, 132, 0.3);
    }
    
    /* Sonuç kartı */
    .result-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #a5d6a7;
    }
    
    /* Buton - Orman yeşili */
    .stButton>button {
        background: linear-gradient(45deg, #43a047 0%, #2e7d32 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 40px;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #2e7d32 0%, #1b5e20 100%);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
        transform: translateY(-2px);
    }
    
    /* Dil seçim - Yaprak yeşili */
    .stSelectbox>div>div {
        background: white;
        border-radius: 15px;
        border: 2px solid #81c784;
        box-shadow: 0 2px 10px rgba(129, 199, 132, 0.2);
    }
    
    /* Sonuç kutuları */
    .stInfo {
        background: rgba(232, 245, 233, 0.8);
        border: 1px solid #81c784;
        border-radius: 15px;
        color: #2e7d32;
    }
    
    .stSuccess {
        background: rgba(200, 230, 201, 0.9);
        border: 1px solid #66bb6a;
        border-radius: 15px;
        color: #1b5e20;
    }
    
    .stWarning {
        background: rgba(255, 249, 196, 0.8);
        border: 1px solid #ffd54f;
        border-radius: 15px;
        color: #f57f17;
    }
    
    /* Ayırıcı çizgi - Doğal */
    .nature-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #81c784, #4caf50, #81c784, transparent);
        margin: 25px 0;
        border-radius: 2px;
    }
    
    /* Emoji stil */
    .nature-emoji {
        font-size: 24px;
        margin-right: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown('<div class="nature-title">🌿 Melih\'in Sanal Tercümanı</div>', unsafe_allow_html=True)
st.markdown('<div class="nature-subtitle">🍃 Sanal Dünyama Hoşgeldiniz</div>', unsafe_allow_html=True)

st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)

# ==================== DİL KARTI ====================
with st.container():
    st.markdown('<div class="nature-card">', unsafe_allow_html=True)
    
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
    st.markdown('<div class="nature-card camera-card">', unsafe_allow_html=True)
    
    st.markdown("### 🌱 Sanal Dünya Turuna Hazır Mısın?")
    
    camera_image = st.camera_input(
        "🌸 Tura Başla",
        key="camera"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)

# ==================== SONUÇ KARTI ====================
if camera_image is not None:
    with st.container():
        st.markdown('<div class="nature-card result-card">', unsafe_allow_html=True)
        
        image = Image.open(camera_image)
        img_array = np.array(image)
        
        with st.spinner("🍂 Metin okunuyor..."):
            results = reader.readtext(img_array, detail=1)
        
        if results:
            tum_metinler = []
            for bbox, text, prob in results:
                if prob >= 0.3:
                    tum_metinler.append(text)
            
            if tum_metinler:
                birlesik_metin = " ".join(tum_metinler)
                
                st.success(f"🌻 {len(tum_metinler)} metin bloğu bulundu!")
                
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
                        st.error(f"🥀 Çeviri hatası: {str(e)}")
            else:
                st.warning("🍂 Yeterince net metin bulunamadı.")
        else:
            st.warning("🍂 Hiç metin bulunamadı. Daha net tutun.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)
st.caption("🌿 Turda Karşılaştıklarını Anlamak İçin Yazıyı Netleştir")
