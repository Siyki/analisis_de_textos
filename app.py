import streamlit as st
from textblob import TextBlob

# Colores personalizados
azul = "#1f77b4"

# Título principal
st.markdown(f"<h1 style='color:{azul};'>📝 Analizador de Texto con TextBlob</h1>", unsafe_allow_html=True)

# Título del sidebar
st.sidebar.markdown(f"<h2 style='color:{azul};'>⚙️ Opciones</h2>", unsafe_allow_html=True)

# Resto de tu código...
texto_usuario = st.text_area("Introduce el texto que deseas analizar:")

if st.button("Analizar"):
    blob = TextBlob(texto_usuario)
    polaridad = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity

    st.subheader("Resultado del Análisis")
    st.write(f"**Polaridad:** {polaridad}")
    st.write(f"**Subjetividad:** {subjetividad}")
