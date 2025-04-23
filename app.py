import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator
from PIL import Image  # Para manejar imágenes

# Configuración de la página con colores personalizados
st.set_page_config(
    page_title="✨ Analizador de Texto Encantador ✨",
    page_icon="🔮",
    layout="wide"
)

# Define los colores pastel
fondo = "#E0F2F7"  # Un azul muy claro
azul = "#64B5F6"  # Un azul pastel más oscuro

# Aplica el estilo CSS personalizado
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

# Título y descripción con un toque mágico
st.title("✨ ¡Desentraña los Sentimientos de tus Palabras! ✨")
st.markdown(f"<p style='color:{azul};'>¡Sumérgete en el fascinante mundo del análisis de texto! Esta aplicación, impulsada por la magia de TextBlob, te permite:<br>- 💖 Descubrir el sentimiento oculto en tus textos (¿alegría, tristeza, neutralidad?)<br>- 💭 Medir la subjetividad de tus palabras (¿opinión o hecho?)<br>- 🗝️ Extraer las palabras clave que dan forma a tu mensaje<br>- 📊 Visualizar la frecuencia de tus vocablos más importantes</p>", unsafe_allow_html=True)

# Barra lateral con estilo
st.sidebar.title(f"⚙️ <span style='color:{azul};'>¡Ajusta tus Hechizos!</span>", unsafe_allow_html=True)
modo = st.sidebar.selectbox(
    "Elige tu portal de entrada:",
    ["Texto directo 📜", "Archivo de texto 📂"]
)

# Función para contar palabras (sin depender de NLTK) - ¡El conjuro de las palabras!
def contar_palabras(texto):
    stop_words = set([
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
        "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
        "ellas", "ellos", "en", "entre", "era", "eras", "es", "esa", "esas", "ese",
        "eso", "esos", "esta", "estas", "este", "esto", "estos", "ha", "había", "han",
        "has", "hasta", "he", "la", "las", "le", "les", "lo", "los", "me", "mi", "mía",
        "mías", "mío", "míos", "mis", "mucho", "muchos", "muy", "nada", "ni", "no", "nos",
        "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os",
        "otra", "otras", "otro", "otros", "para", "pero", "poco", "por", "porque", "que",
        "quien", "quienes", "qué", "se", "sea", "sean", "según", "si", "sido", "sin",
        "sobre", "sois", "somos", "son", "soy", "su", "sus", "suya", "suyas", "suyo",
        "suyos", "también", "tanto", "te", "tenéis", "tenemos", "tener", "tengo", "ti",
        "tiene", "tienen", "todo", "todos", "tu", "tus", "tuya", "tuyas", "tuyo", "tuyos",
        "tú", "un", "una", "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras",
        "vuestro", "vuestros", "y", "ya", "yo",
        # Inglés
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
        "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
        "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not",
        "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
        "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll",
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
        "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
        "we'd", "we'll", "we're", "we've", "were",         "weren't", "what", "what's", "when",
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])

    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [palabra for palabra in palabras
                         if palabra not in stop_words and len(palabra) > 2]

    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1

    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))

    return contador_ordenado, palabras_filtradas

# Inicializar el traductor - ¡El oráculo de los idiomas!
translator = Translator()

# Función para traducir texto - ¡El hechizo de la traducción!
def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"¡Oh no! El hechizo de traducción falló: {e}")
        return texto

# Función para procesar el texto con TextBlob - ¡La alquimia del análisis!
def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })
    contador_palabras, palabras = contar_palabras(texto_ingles)
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# Función para crear visualizaciones mágicas
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    # Visualización de sentimiento y subjetividad con barras de progreso y emojis
    with col1:
        st.subheader(f"<span style='color:{azul};'>💖 Análisis de Sentimiento y Subjetividad 💭</span>", unsafe_allow_html=True)

        st.markdown(f"<p style='color:{azul};'>**Sentimiento:**</p>", unsafe_allow_html=True)
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)

        if resultados["sentimiento"] > 0.2:
            st.success(f"😊 ¡Vibras positivas! ({resultados['sentimiento']:.2f})")
            try:
                imagen_positiva = Image.open("happy.png")
                st.image(imagen_positiva, caption="¡Este texto irradia alegría!", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'happy.png' no encontrada.")
        elif resultados["sentimiento"] < -0.2:
            st.error(f"😟 ¡Un toque de melancolía! ({resultados['sentimiento']:.2f})")
            try:
                imagen_negativa = Image.open("sad.png")
                st.image(imagen_negativa, caption="Este texto tiene un tono más sombrío.", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'sad.png' no encontrada.")
        else:
            st.info(f"😐 Neutralidad en el aire ({resultados['sentimiento']:.2f})")
            try:
                imagen_neutral = Image.open("neutral.png")  # Reemplaza "neutral.png" con tu imagen neutral
                st.image(imagen_neutral, caption="Este texto se mantiene en un punto medio.", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'neutral.png' no encontrada.")

        st.markdown(f"<p style='color:{azul};'>**Subjetividad:**</p>", unsafe_allow_html=True)
        st.progress(resultados["subjetividad"])
        if resultados["subjetividad"] > 0.6:
            st.warning(f"🗣️ ¡Mucha opinión aquí! ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 ¡Predominan los hechos! ({resultados['subjetividad']:.2f})")

    # Palabras más frecuentes con un gráfico de barras encantador
    with col2:
        st.subheader(f"<span style='color:{azul};'>✨ Las Palabras con más Poder ✨</span>", unsafe_allow_html=True)
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)
        else:
            st.info("El conjuro de las palabras no encontró nada relevante.")

    # Mostrar texto traducido en un pergamino expandible
    st.subheader(f"<span style='color:{azul};'>📜 El Pergamino de la Traducción 📜</span>", unsafe_allow_html=True)
    with st.expander("Desenrollar el pergamino completo"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<p style='color:{azul};'>**Texto Original (Español):**</p>", unsafe_allow_html=True)
            st.text_area("", resultados["texto_original"], height=150)
        with col2:
            st.markdown(f"<p style='color:{azul};'>**Texto Traducido (Inglés):**</p>", unsafe_allow_html=True)
            st.text_area("", resultados["texto_traducido"], height=150)

    # Análisis de frases con un toque de sentimiento
    st.subheader(f"<span style='color:{azul};'>💬 Fragmentos de Sentimiento 💬</span>", unsafe_allow_html=True)
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]

            try:
                blob_frase = TextBlob(frase_traducida)
                sentimiento_frase = blob_frase.sentiment.polarity

                emoji_frase = "😐"  # Emoji neutral por defecto
                if sentimiento_frase > 0.2:
                    emoji_frase = "😊"
                elif sentimiento_frase < -0.2:
                    emoji_frase = "😟"

                st.markdown(f"{i}. {emoji_frase} **Original:** *\"{frase_original}\"*", unsafe_allow_html=True)
                st.markdown(f"   **Traducción:** *\"{frase_traducida}\"* (Sentimiento: {sentimiento_frase:.2f})", unsafe_allow_html=True)
                st.markdown("---")
            except:
                st.markdown(f"{i}. **Original:** *\"{frase_original}\"*", unsafe_allow_html=True)
                st.markdown(f"   **Traducción:** *\"{frase_traducida}\"*", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("El oráculo de las frases no reveló nada.")

# Lógica principal según el modo seleccionado - ¡El corazón de la magia!
if modo == "Texto directo 📜":
    st.subheader(f"<span style='color:{azul};'>🔮 ¡Escribe tus palabras mágicas aquí! 🔮</span>", unsafe_allow_html=True)
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar...")

    if st.button("✨ ¡Invocar el Análisis! ✨"):
        if texto.strip():
            with st.spinner("¡Los duendes del análisis están trabajando...!"):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("¡El pergamino está vacío! Por favor, ingresa algún texto.")

elif modo == "Archivo de texto 📂":
    st.subheader(f"<span style='color:{azul};'>📤 ¡Ofrece tu archivo al analizador! 📤</span>", unsafe_allow_html=True)
    archivo = st.file_uploader("", type=["txt", "csv", "md"])

    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander(f"<span style='color:{azul};'>👁️‍🗨️ ¡Echar un vistazo al contenido del archivo! (Primeros 1000 caracteres)</span>", unsafe_allow_html=True):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))

            if st.button("✨ ¡Desatar el Análisis del Archivo! ✨"):
                with st.spinner("¡Los escribas del análisis están descifrando tu archivo...!"):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"¡Un error arcano ocurrió al procesar el archivo: {e}")

# Información adicional en un cofre del tesoro expandible
with st.expander(f"<span style='color:{azul};'>📜 ¡Secretos del Análisis Revelados! 📜</span>", unsafe_allow_html=True):
    st.markdown(
    )
