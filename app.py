import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
    layout="wide"
)

# Colores pastel
fondo = "#E0F2F7"
azul = "#64B5F6"

# Estilo CSS
st.markdown(
    f"""
    <style>
        body {{
            background-color: {fondo};
            color: {azul};
        }}
        .st-title {{
            color: {azul} !important;
        }}
        .st-subheader {{
            color: {azul} !important;
        }}
        .streamlit-expanderHeader {{
            color: {azul} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Título y descripción
st.markdown(f"<h1 style='color:{azul};'>📝 Analizador de Texto con TextBlob</h1>", unsafe_allow_html=True)
st.markdown(f"""
<p style='color:{azul};'>
Esta aplicación utiliza TextBlob para realizar un análisis básico de texto:
- Análisis de sentimiento y subjetividad
- Extracción de palabras clave
- Análisis de frecuencia de palabras
</p>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title(f"<span style='color:{azul};'>Opciones</span>", unsafe_allow_html=True)
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# Función para contar palabras
def contar_palabras(texto):
    stop_words = set([
        # español e inglés...
        "a", "al", "como", "de", "el", "en", "la", "los", "y", "the", "and", "is", "to", "with", "for", "on", "you", "this",
        "that", "are", "was", "have", "has", "it", "he", "she", "we", "they", "not", "but", "if", "or", "by", "an", "be"
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True)), palabras_filtradas

# Traductor
translator = Translator()

def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

def procesar_texto(texto):
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    frases_originales = [f.strip() for f in re.split(r'[.!?]+', texto) if f.strip()]
    frases_traducidas = [f.strip() for f in re.split(r'[.!?]+', texto_ingles) if f.strip()]
    frases = [{"original": o, "traducido": t} for o, t in zip(frases_originales, frases_traducidas)]
    contador_palabras, palabras = contar_palabras(texto_ingles)
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto,
        "texto_traducido": texto_ingles
    }

def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"<span style='color:{azul};'>Análisis de Sentimiento y Subjetividad</span>", unsafe_allow_html=True)
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.markdown(f"<p style='color:{azul};'>**Sentimiento:**</p>", unsafe_allow_html=True)
        st.progress(sentimiento_norm)

        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
            try:
                st.image("happy.png", caption="¡Este texto irradia alegría!", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'happy.png' no encontrada.")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
            try:
                st.image("sad.png", caption="Este texto tiene un tono más sombrío.", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'sad.png' no encontrada.")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
            try:
                st.image("neutral.png", caption="Este texto se mantiene neutral.", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'neutral.png' no encontrada.")

        st.markdown(f"<p style='color:{azul};'>**Subjetividad:**</p>", unsafe_allow_html=True)
        st.progress(resultados["subjetividad"])
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")

    with col2:
        st.subheader(f"<span style='color:{azul};'>Palabras más frecuentes</span>", unsafe_allow_html=True)
        top = dict(list(resultados["contador_palabras"].items())[:10])
        st.bar_chart(top)

    st.subheader(f"<span style='color:{azul};'>Texto Traducido</span>", unsafe_allow_html=True)
    with st.expander("Ver traducción completa"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Texto Original (Español):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown(f"**Texto Traducido (Inglés):**")
            st.text(resultados["texto_traducido"])

    st.subheader(f"<span style='color:{azul};'>Frases detectadas</span>", unsafe_allow_html=True)
    for i, frase in enumerate(resultados["frases"][:10], 1):
        try:
            blob_frase = TextBlob(frase["traducido"])
            s = blob_frase.sentiment.polarity
            emoji = "😐"
            if s > 0.05:
                emoji = "😊"
            elif s < -0.05:
                emoji = "😟"
            st.markdown(f"{i}. {emoji} **Original:** *\"{frase['original']}\"*", unsafe_allow_html=True)
            st.markdown(f"   **Traducción:** *\"{frase['traducido']}\"* (Sentimiento: {s:.2f})", unsafe_allow_html=True)
        except:
            st.markdown(f"{i}. **Original:** *\"{frase['original']}\"*", unsafe_allow_html=True)
            st.markdown(f"   **Traducción:** *\"{frase['traducido']}\"*", unsafe_allow_html=True)

# Lógica principal
if modo == "Texto directo":
    st.subheader(f"<span style='color:{azul};'>Ingresa tu texto para analizar</span>", unsafe_allow_html=True)
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar...")

    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando texto..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Por favor, ingresa algún texto para analizar.")

elif modo == "Archivo de texto":
    st.subheader(f"<span style='color:{azul};'>Carga un archivo de texto</span>", unsafe_allow_html=True)
    archivo = st.file_uploader("", type=["txt", "csv", "md"])

    if archivo is not None:
        try:
            contenido = archivo.getvalue()
            if isinstance(contenido, bytes):
                contenido = contenido.decode("utf-8")
            with st.expander("Ver contenido del archivo"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            if st.button("Analizar archivo"):
                with st.spinner("Analizando archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

# Info adicional
with st.expander(f"<span style='color:{azul};'>📚 Información sobre el análisis</span>", unsafe_allow_html=True):
    st.markdown(f"""
    ### <span style='color:{azul};'>Sobre el análisis de texto</span>

    - **Sentimiento**: Varía de -1 (muy negativo) a 1 (muy positivo)
    - **Subjetividad**: Varía de 0 (muy objetivo) a 1 (muy subjetivo)

    ### <span style='color:{azul};'>Requisitos mínimos</span>

    Esta aplicación utiliza únicamente:
    ```
    streamlit
    textblob
    pandas
    googletrans
    Pillow
    ```
    """, unsafe_allow_html=True)
