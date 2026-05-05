import streamlit as st
import numpy as np
from PIL import Image
import easyocr
import requests
import json

# ==================== SAYFA YAPILANDIRMASI ====================
st.set_page_config(
    page_title="Melih'in Sanal Tercümanı",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DOĞA RENKLERİ CSS ====================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f5f5dc 0%, #e8f5e9 50%, #d4edda 100%);
    }
    .nature-title {
        font-size: 44px;
        font-weight: 700;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Georgia', serif;
    }
    .nature-subtitle {
        font-size: 18px;
        color: #795548;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Georgia', serif;
    }
    .nature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 30px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.15);
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    .stButton>button {
        background: linear-gradient(45deg, #43a047 0%, #2e7d32 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 18px 50px;
        font-size: 20px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #2e7d32 0%, #1b5e20 100%);
        transform: translateY(-2px);
    }
    .stSelectbox>div>div {
        background: white;
        border-radius: 15px;
        border: 2px solid #81c784;
        box-shadow: 0 2px 10px rgba(129, 199, 132, 0.2);
    }
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
    .nature-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #81c784, #4caf50, #81c784, transparent);
        margin: 25px 0;
        border-radius: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== DİL VERİSİ ====================
DILLER = {
    'Türkçe': 'TR', 'İngilizce': 'EN', 'Almanca': 'DE',
    'Fransızca': 'FR', 'İspanyolca': 'ES', 'İtalyanca': 'IT',
    'Portekizce': 'PT', 'Rusça': 'RU', 'Arapça': 'AR',
    'Çince': 'ZH', 'Japonca': 'JA', 'Korece': 'KO',
    'Lehçe': 'PL', 'Hollandaca': 'NL', 'İsveççe': 'SV'
}

# DeepL dil kodları
DEEPL_DILLER = {
    'Türkçe': 'TR', 'İngilizce': 'EN-US', 'Almanca': 'DE',
    'Fransızca': 'FR', 'İspanyolca': 'ES', 'İtalyanca': 'IT',
    'Portekizce': 'PT-PT', 'Rusça': 'RU', 'Arapça': 'AR',
    'Çince': 'ZH', 'Japonca': 'JA', 'Korece': 'KO',
    'Lehçe': 'PL', 'Hollandaca': 'NL', 'İsveççe': 'SV'
}

# ==================== ÇEVİRİ FONKSİYONLARI ====================
def deepl_cevir(metin, kaynak, hedef, api_key):
    """DeepL API ile çeviri"""
    url = "https://api-free.deepl.com/v2/translate"
    
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": [metin],
        "target_lang": hedef
    }
    
    if kaynak != 'auto':
        data["source_lang"] = kaynak
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["translations"][0]["text"]
    except Exception as e:
        return f"DeepL Hatası: {str(e)}"

def google_cevir(metin, kaynak, hedef):
    """Google Translate (yedek)"""
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source=kaynak, target=hedef).translate(metin)
    except Exception as e:
        return f"Google Hatası: {str(e)}"

# ==================== SESSION STATE ====================
if 'sayfa' not in st.session_state:
    st.session_state.sayfa = 'ayarlar'
    st.session_state.source_lang = 'Otomatik'
    st.session_state.target_lang = 'İngilizce'

# ==================== SAYFA 1: AYARLAR ====================
if st.session_state.sayfa == 'ayarlar':
    
    st.markdown('<div class="nature-title">🌿 Melih\'in Sanal Tercümanı</div>', unsafe_allow_html=True)
    st.markdown('<div class="nature-subtitle">🍃 Sanal Dünyama Hoşgeldiniz</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="nature-card">', unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Tur Ayarlarınızı Seçin")
        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox("🌍 Kaynak Dil", ['Otomatik'] + list(DILLER.keys()))
        with col2:
            target = st.selectbox("🎯 Hedef Dil", list(DILLER.keys()), index=1)
        
        min_confidence = st.slider("🔍 Min. Güven Skoru", 0.0, 1.0, 0.3)
        
        # Çeviri motoru seçimi
        st.write("---")
        st.markdown("### 🤖 Çeviri Motoru")
        
        ceviri_motoru = st.radio(
            "Kalite seviyesi seçin:",
            ["DeepL (En Kaliteli - API Key Gerekli)", "Google (Otomatik - Ücretsiz)"]
        )
        
        api_key = ""
        if ceviri_motoru == "DeepL (En Kaliteli - API Key Gerekli)":
            api_key = st.text_input(
                "🔑 DeepL API Key'inizi girin:",
                type="password",
                help="deepl.com/pro-api adresinden ücretsiz alabilirsiniz"
            )
            st.info("💡 DeepL API key olmadan Google çevirisi kullanılır")
        
        st.write("---")
        
        if st.button("🚀 Tura Başla", use_container_width=True):
            st.session_state.source_lang = source
            st.session_state.target_lang = target
            st.session_state.min_confidence = min_confidence
            st.session_state.ceviri_motoru = ceviri_motoru
            st.session_state.api_key = api_key
            st.session_state.sayfa = 'kamera'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)
    st.caption("🌿 Turda Karşılaştıklarını Anlamak İçin Yazıyı Netleştir")

# ==================== SAYFA 2: KAMERA + ÇEVİRİ ====================
elif st.session_state.sayfa == 'kamera':
    
    @st.cache_resource
    def load_models():
        reader = easyocr.Reader(['en'], gpu=False, download_enabled=True)
        return reader
    
    reader = load_models()
    
    col_back, col_title, col_empty = st.columns([1, 3, 1])
    with col_back:
        if st.button("⬅️ Geri"):
            st.session_state.sayfa = 'ayarlar'
            st.rerun()
    with col_title:
        st.markdown('<div style="text-align:center; color:#2e7d32; font-size:20px; font-weight:600;">📷 TUR MODU</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)
    
    col_lang1, col_lang2, col_motor = st.columns(3)
    with col_lang1:
        st.info(f"🌍 Kaynak: {st.session_state.source_lang}")
    with col_lang2:
        st.info(f"🎯 Hedef: {st.session_state.target_lang}")
    with col_motor:
        motor = "DeepL" if "DeepL" in st.session_state.get('ceviri_motoru', '') else "Google"
        st.info(f"🤖 Motor: {motor}")
    
    st.write("---")
    
    st.markdown("### 🌱 Yazıyı Kameraya Tutun")
    
    camera_image = st.camera_input("📸 Fotoğraf Çek", key="camera_full")
    
    if camera_image is not None:
        with st.spinner("🍂 Metin okunuyor..."):
            image = Image.open(camera_image)
            img_array = np.array(image)
            results = reader.readtext(img_array, detail=1)
        
        if results:
            tum_metinler = []
            for bbox, text, prob in results:
                if prob >= st.session_state.get('min_confidence', 0.3):
                    tum_metinler.append(text)
            
            if tum_metinler:
                birlesik_metin = " ".join(tum_metinler)
                
                st.success(f"🌻 {len(tum_metinler)} metin bloğu bulundu!")
                
                with st.container():
                    st.markdown('<div class="nature-card" style="background:rgba(232,245,233,0.95); border:2px solid #81c784;">', unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.markdown("**📝 Orijinal Metin:**")
                        st.info(birlesik_metin)
                    
                    with c2:
                        st.markdown("**🔄 Çeviri:**")
                        
                        # ÇEVİRİ MOTORU SEÇİMİ
                        if "DeepL" in st.session_state.get('ceviri_motoru', '') and st.session_state.get('api_key'):
                            # DeepL kullan
                            src = 'auto' if st.session_state.source_lang == 'Otomatik' else DEEPL_DILLER.get(st.session_state.source_lang, 'EN')
                            dest = DEEPL_DILLER.get(st.session_state.target_lang, 'TR')
                            
                            translated = deepl_cevir(birlesik_metin, src, dest, st.session_state.api_key)
                            
                            if "Hatası" not in translated:
                                st.success(translated)
                                st.caption("✅ DeepL ile çevrildi")
                            else:
                                # DeepL hata verirse Google'a düş
                                st.warning("DeepL çalışmadı, Google kullanılıyor...")
                                src_g = 'auto' if st.session_state.source_lang == 'Otomatik' else DILLER.get(st.session_state.source_lang, 'auto')
                                dest_g = DILLER.get(st.session_state.target_lang, 'tr')
                                translated = google_cevir(birlesik_metin, src_g, dest_g)
                                st.success(translated)
                        else:
                            # Google kullan
                            src = 'auto' if st.session_state.source_lang == 'Otomatik' else DILLER.get(st.session_state.source_lang, 'auto')
                            dest = DILLER.get(st.session_state.target_lang, 'tr')
                            translated = google_cevir(birlesik_metin, src, dest)
                            st.success(translated)
                            st.caption("🔄 Google Translate ile çevrildi")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.write("---")
                if st.button("🔄 Yeni Fotoğraf Çek", use_container_width=True):
                    st.rerun()
            else:
                st.warning("🍂 Yeterince net metin bulunamadı.")
        else:
            st.warning("🍂 Hiç metin bulunamadı. Daha net tutun.")
    
    st.markdown('<div class="nature-line"></div>', unsafe_allow_html=True)
    st.caption("💡 Yazıyı net tutun ve yeterli ışık sağlayın")
