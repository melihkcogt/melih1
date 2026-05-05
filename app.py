import streamlit as st
import numpy as np
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator

# ==================== NEON TEMA ====================
st.set_page_config(
    page_title="Melih'in Sanal Tercümanı",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Neon CSS
st.markdown("""
    <style>
    /* Siyah arka plan */
    .stApp {
        background-color: #0a0a0a;
    }
    
    /* Neon yazı efekti */
    .neon-title {
        font-size: 48px;
        font-weight: 900;
        color: #00ff88;
        text-align: center;
        text-shadow: 
            0 0 10px #00ff88,
            0 0 20px #00ff88,
            0 0 40px #00ff88,
            0 0 80px #00ff88;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
    }
    
    .neon-subtitle {
        font-size: 20px;
        color: #ff00ff;
        text-align: center;
        text-shadow: 
            0 0 10px #ff00ff,
            0 0 20px #ff00ff;
        margin-bottom: 40px;
        font-family: 'Courier New', monospace;
    }
    
    /* Neon kart */
    .neon-card {
        background: rgba(10, 10, 10, 0.9);
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 
            0 0 10px #00ff88,
            inset 0 0 10px rgba(0, 255, 136, 0.1);
    }
    
    .neon-card-pink {
        border: 2px solid #ff00ff;
        box-shadow: 
            0 0 10px #ff00ff,
            inset 0 0 10px rgba(255, 0, 255, 0.1);
    }
    
    /* Neon buton */
    .stButton>button {
        background: transparent;
        color: #00ff88;
        border: 2px solid #00ff88;
        border-radius: 10px;
        padding: 15px 40px;
        font-size: 18px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ff88;
        box-shadow: 0 0 15px #00ff88;
        width: 100%;
        font-family: 'Courier New', monospace;
    }
    
    .stButton>button:hover {
        background: #00ff88;
        color: #0a0a0a;
        box-shadow: 0 0 30px #00ff88;
    }
    
    /* Dil seçim */
    .stSelectbox>div>div {
        background: #0a0a0a;
        border: 2px solid #00ccff;
        border-radius: 10px;
        color: #00ccff;
        box-shadow: 0 0 10px #00ccff;
    }
    
    /* Sonuç kutuları */
    .stInfo {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #00ff88;
        border-radius: 10px;
        color: #00ff88;
    }
    
    .stSuccess {
        background: rgba(0, 255, 136, 0.2);
        border: 1px solid #00ff88;
        border-radius: 10px;
        color: #00ff88;
        text-shadow: 0 0 5px #00ff88;
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.1);
        border: 1px solid #ffa500;
        border-radius: 10px;
        color: #ffa500;
    }
    
    /* Işık çizgileri */
    .light-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        margin: 20px 0;
        box-shadow: 0 0 10px #00ff88;
    }
    </style>
""", unsafe_allow_html=True)

# Karanlık mod (neon'da her zaman karanlık)
dark_mode = st.toggle("🌙 Karanlık Mod", value=True, disabled=True)

# ==================== BAŞLIK ====================
st.markdown('<div class="neon-title">📱 MELIH\'IN SANAL TERCUMANİ</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">🌍 SANAL DUNYAMA HOSGELDINIZ</div>', unsafe_allow_html=True)

st.markdown('<div class="light-line"></div>', unsafe_allow_html=True)

# ==================== DİL KARTI ====================
with st.container():
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    
    diller = {
        'Turkce': 'tr', 'Ingilizce': 'en', 'Almanca': 'de',
        'Fransizca': 'fr', 'Ispanyolca': 'es', 'Italyanca': 'it',
        'Portekizce': 'pt', 'Rusca': 'ru', 'Arapca': 'ar',
        'Cince': 'zh-CN', 'Japonca': 'ja', 'Korece': 'ko'
    }
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("🌍 KAYNAK DIL", ['Otomatik'] + list(diller.keys()))
    with col2:
        target_lang = st.selectbox("🎯 HEDEF DIL", list(diller.keys()), index=1)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== OCR MODEL ====================
@st.cache_resource
def load_models():
    reader = easyocr.Reader(['en'], gpu=False, download_enabled=True)
    return reader

reader = load_models()

# ==================== KAMERA KARTI ====================
with st.container():
    st.markdown('<div class="neon-card neon-card-pink">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 SANAL DUNYA TURUNA HAZIR MISIN?")
    
    camera_image = st.camera_input(
        "TURA BASLA",
        key="camera"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="light-line"></div>', unsafe_allow_html=True)

# ==================== SONUÇ KARTI ====================
if camera_image is not None:
    with st.container():
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        
        image = Image.open(camera_image)
        img_array = np.array(image)
        
        with st.spinner("🔍 METIN OKUNUYOR..."):
            results = reader.readtext(img_array, detail=1)
        
        if results:
            tum_metinler = []
            for bbox, text, prob in results:
                if prob >= 0.3:
                    tum_metinler.append(text)
            
            if tum_metinler:
                birlesik_metin = " ".join(tum_metinler)
                
                st.success(f"✅ {len(tum_metinler)} METIN BLOKU BULUNDU!")
                
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("**📝 ORIJINAL METIN:**")
                    st.info(birlesik_metin)
                
                with c2:
                    st.markdown("**🔄 CEVIRI:**")
                    try:
                        src = 'auto' if source_lang == 'Otomatik' else diller[source_lang]
                        dest = diller[target_lang]
                        
                        translated = GoogleTranslator(source=src, target=dest).translate(birlesik_metin)
                        st.success(translated)
                    except Exception as e:
                        st.error(f"CEVIRI HATASI: {str(e)}")
            else:
                st.warning("❌ YETERINCE NET METIN BULUNAMADI.")
        else:
            st.warning("❌ HIC METIN BULUNAMADI. DAHA NET TUTUN.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown('<div class="light-line"></div>', unsafe_allow_html=True)
st.caption("💡 TURDA KARSILASTIKLARINI ANLAMAK ICIN YAZIYI NETLESTIR")
