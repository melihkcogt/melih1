pimport streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
from googletrans import Translator

st.set_page_config(page_title="Kamera Tercüman", layout="wide")
st.title("📱 Kamera Tercüman")
st.write("Kameranızı bir yazıya tutun, anında çeviri gelsin!")

@st.cache_resource
def load_models():
    reader = easyocr.Reader(['tr','en'], gpu=False)
    translator = Translator()
    return reader, translator

reader, translator = load_models()

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Kaynak Dil", ['Auto','Türkçe','İngilizce'])
with col2:
    target_lang = st.selectbox("Hedef Dil", ['İngilizce','Türkçe'])

lang_map = {'Türkçe':'tr','İngilizce':'en','Auto':'auto'}

st.write("---")
camera_image = st.camera_input("Kameranızı açın ve bir yazı tutun")

if camera_image is not None:
    image = Image.open(camera_image)
    img_array = np.array(image)
    
    with st.spinner("Metin okunuyor..."):
        results = reader.readtext(img_array, detail=1)
    
    if results:
        st.success(f"{len(results)} metin bulundu!")
        for bbox, text, prob in results:
            if prob > 0.3:
                st.write("---")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**📝 Orijinal:**")
                    st.info(text)
                with c2:
                    st.markdown("**🔄 Çeviri:**")
                    try:
                        src = lang_map[source_lang] if source_lang != 'Auto' else 'auto'
                        dest = 'en' if target_lang == 'İngilizce' else 'tr'
                        if src == dest and src != 'auto':
                            dest = 'tr' if dest == 'en' else 'en'
                        translated = translator.translate(text, src=src, dest=dest)
                        st.success(translated.text)
                    except Exception as e:
                        st.error(f"Hata: {str(e)}")
    else:
        st.warning("Metin bulunamadı. Daha net tutun.")

st.write("---")
st.caption("💡 İpucu: Daha iyi sonuç için yazıyı net tutun ve yeterli ışık sağlayın.")
