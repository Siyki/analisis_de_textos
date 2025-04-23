import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator
from PIL import Image  # Importamos la librería para manejar imágenes

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
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

# Título y descripción
st.title(f"<span style='color:{azul};'>📝 Analizador de Texto con TextBlob</span>", unsafe_allow_html=True)
st.markdown(f"""
<p style='color:{azul};'>
Esta aplicación utiliza TextBlob para realizar un análisis básico de texto:
- Análisis de sentimiento y subjetividad
- Extracción de palabras clave
- Análisis de frecuencia de palabras
</p>
""", unsafe_allow_html=True)

# Barra lateral
st.sidebar.title(f"<span style='color:{azul};'>Opciones</span>", unsafe_allow_html=True)
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# Función para contar palabras sin depender de NLTK
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

# Inicializar el traductor
translator = Translator()

# Función para traducir texto del español al inglés
def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto  # Devolver el texto original si falla la traducción

# Función para procesar el texto con TextBlob (versión con traducción)
def procesar_texto(texto):
    # Guardar el texto original
    texto_original = texto

    # Traducir el texto al inglés para mejor análisis
    texto_ingles = traducir_texto(texto)

    # Analizar el texto traducido con TextBlob
    blob = TextBlob(texto_ingles)

    # Análisis de sentimiento (esto no requiere corpus adicionales)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity

    # Extraer frases de manera simplificada (del texto original)
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]

    # Extraer frases del texto traducido
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]

    # Combinar frases originales y traducidas
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })

    # Contar palabras con nuestra función simplificada (en el texto traducido)
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

# Función para crear visualizaciones usando componentes nativos de Streamlit
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    # Visualización de sentimiento y subjetividad con barras de progreso de Streamlit
    with col1:
        st.subheader(f"<span style='color:{azul};'>Análisis de Sentimiento y Subjetividad</span>", unsafe_allow_html=True)

        # Normalizar valores para mostrarlos en barras de progreso
        # Sentimiento va de -1 a 1, lo normalizamos a 0-1 para la barra
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2

        st.markdown(f"<p style='color:{azul};'>**Sentimiento:**</p>", unsafe_allow_html=True)
        st.progress(sentimiento_norm)

        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
            try:
                imagen_positiva = Image.open("happy.png")
                st.image(imagen_positiva, caption="¡Este texto irradia alegría!", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'happy.png' no encontrada.")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
            try:
                imagen_negativa = Image.open("sad.png")
                st.image(imagen_negativa, caption="Este texto tiene un tono más sombrío.", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'sad.png' no encontrada.")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
            try:
                imagen_neutral = Image.open("neutral.png")  # Asegúrate de tener esta imagen
                st.image(imagen_neutral, caption="Este texto se mantiene neutral.", width=150)
            except FileNotFoundError:
                st.warning("Imagen 'neutral.png' no encontrada.")

        # Subjetividad ya está en el rango 0-1
        st.markdown(f"<p style='color:{azul};'>**Subjetividad:**</p>", unsafe_allow_html=True)
        st.progress(resultados["subjetividad"])

        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")

    # Palabras más frecuentes usando chart de Streamlit
    with col2:
        st.subheader(f"<span style='color:{azul};'>Palabras más frecuentes</span>", unsafe_allow_html=True)
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)

    # Mostrar texto traducido
    st.subheader(f"<span style='color:{azul};'>Texto Traducido</span>", unsafe_allow_html=True)
    with st.expander("Ver traducción completa"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<span style='color:{azul};'>**Texto Original (Español):**</span>", unsafe_allow_html=True)
            st.text(resultados["texto_original"])
        with col2:
            st.markdown(f"<span style='color:{azul};'>**Texto Traducido (Inglés):**</span>", unsafe_allow_html=True)
            st.text(resultados["texto_traducido"])

    # Análisis de frases
    st.subheader(f"<span style='color:{azul};'>Frases detectadas</span>", unsafe_allow_html=True)
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]

            try:
                blob_frase = TextBlob(frase_traducida)
                sentimiento = blob_frase.sentiment.polarity

                emoji = "😐"
                if sentimiento > 0.05:
                    emoji = "😊"
                elif sentimiento < -0.05:
                    emoji = "😟"

                st.markdown(f"{i}. {emoji} **Original:** *\"{frase_original}\"*", unsafe_allow_html=True)
                st.markdown(f"   **Traducción:** *\"{frase_traducida}\"* (Sentimiento: {sentimiento:.2f})", unsafe_allow_html=True)
                st.markdown("---")
            except:
                st.markdown(f"{i}. **Original:** *\"{frase_original}\"*", unsafe_allow_html=True)
                st.markdown(f"   **Traducción:** *\"{frase_traducida}\"*", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.write("No se detectaron frases.")

# Lógica principal según el modo seleccionado
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

# Información adicional
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
    Pillow (para las imágenes)
    ```
    """, unsafe_allow_html=True)
