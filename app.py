# app.py
import streamlit as st
import pandas as pd
from utils import analizar_estado_animo
from difflib import get_close_matches
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="🎧 Recomendador Musical IA", page_icon="🎵", layout="centered")
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://i.pinimg.com/originals/4a/65/ab/4a65abeead3a8d113bccfee5d5d239f4.gif') no-repeat center center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título estilizado
st.markdown(
    """
    <h1 style="
        text-align: center;
        color: white;
        font-size: 3rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        margin-bottom: 30px;
    ">
    🎧 Recomendador Musical con IA
    </h1>
    """,
    unsafe_allow_html=True
)

# Cargar dataset
df = pd.read_csv("data/Spotify-2000.csv")

# Input del usuario
estado = st.text_input("¿Cómo te sientes o qué estás haciendo ahora mismo?")

if st.button("🎶 Recomendar canciones"):
    if not estado.strip():
        st.warning("❗ Por favor ingresa cómo te sientes o en qué estás.")
        st.stop()

    st.write("🧠 Analizando tu estado de ánimo con IA...")
    resultado = analizar_estado_animo(estado)

    if resultado is None:
        st.error("😢 No se pudo generar recomendación. Intenta de nuevo.")
        st.stop()

    st.markdown(
    """
    <p style="
        text-align: center;
        color: white;
        font-size: 3rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        margin-bottom: 30px;
    ">
    Resultado de la IA:
    </p>
    """,
    unsafe_allow_html=True
)

    generos = resultado.get("generos", [])
    valence = float(resultado.get("valence", 0))
    energy = float(resultado.get("energy", 0))

   

    # Función para coincidencia aproximada de géneros
    def match_genero(genre, target_genres):
        genre_lower = genre.lower()
        for target in target_genres:
            if target in genre_lower:
                return True
            if get_close_matches(target, [genre_lower], n=1, cutoff=0.6):  # subido de 0.4 a 0.6
                return True
        return False

    # Filtrado inicial
    df_filtrado = df[
        (df['Valence'] >= valence - 0.15) &
        (df['Valence'] <= valence + 0.15) &
        (df['Energy'] >= energy - 0.15) &
        (df['Energy'] <= energy + 0.15) &
        (df['Top Genre'].apply(lambda x: match_genero(x, generos)))
    ].copy()

    # Ampliar rangos si no hay resultados
    if df_filtrado.empty:
        df_filtrado = df[
            (df['Valence'] >= valence - 0.3) &
            (df['Valence'] <= valence + 0.3) &
            (df['Energy'] >= energy - 0.3) &
            (df['Energy'] <= energy + 0.3) &
            (df['Top Genre'].apply(lambda x: match_genero(x, generos)))
        ].copy()

    # Si sigue vacío, buscar solo por género
    if df_filtrado.empty:
        df_filtrado = df[
            df['Top Genre'].apply(lambda x: match_genero(x, generos))
        ].copy()

    # Si aún no hay resultados, muestra 5 aleatorias
    if df_filtrado.empty:
        df_filtrado = df.sample(5).copy()
    else:
        st.success(f"✅ Se encontraron {len(df_filtrado)} canciones relacionadas, ¡aquí tienes unas cuantas!")

    canciones = df_filtrado[['Title', 'Artist', 'Top Genre']].sample(min(len(df_filtrado), 5))

    # Función para degradado dinámico según valence
    def obtener_degradado(valence: float) -> str:
        if 0.8 <= valence <= 1.0:
            color1, color2 = "#00FF7F", "#ADFF2F"  # Muy feliz
        elif 0.6 <= valence < 0.8:
            color1, color2 = "#FFD700", "#FFA500"  # Feliz
        elif 0.45 <= valence < 0.6:
            color1, color2 = "#FFD700", "#FFA500"  # Neutro-positivo
        elif 0.3 <= valence < 0.45:
            color1, color2 = "#FFD700", "#FFA500"  # Neutro-negativo
        else:  # valence < 0.3
            color1, color2 = "#0000FF", "#483D8B"  # Triste

        return f"linear-gradient(135deg, {color1}, {color2})"

    degradado = obtener_degradado(valence)

    # Mostrar barra de valence para feedback
    st.markdown(
        f"""
        <div style="margin: 10px 0; height: 20px; background: linear-gradient(to right, #0000FF, #FF69B4, #FFD700, #1DB954, #00FF7F); border-radius: 10px;">
            <div style="width: {valence*100}%; height: 100%; background-color: rgba(255, 255, 255, 0.5); border-radius: 10px;"></div>
        </div>
        <p style="text-align: center; color: white; font-weight: bold;">Valence: {valence:.2f}</p>
        """,
        unsafe_allow_html=True
    )

    # Mostrar canciones con tarjetas estilizadas
    for _, row in canciones.iterrows():
        title = row['Title']
        artist = row['Artist']
        genre = row['Top Genre'].title()
        query = urllib.parse.quote(f"{title} {artist}")
        spotify_url = f"https://open.spotify.com/search/{query}"

        with st.container():
            st.markdown(
                f"""
                <div style="
                    background: {degradado};
                    background-size: 200% 200%;
                    animation: gradientShift 5s ease infinite;
                    padding: 15px;
                    border-radius: 15px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    margin-bottom: 10px;
                    color: black;
                ">
                    <h4 style="margin: 0;">🎵 {title}</h4>
                    <p style="margin: 0;">👤 <b>{artist}</b></p>
                    <p style="margin: 0; font-style: italic;">🎼 {genre}</p>
                    <a href="{spotify_url}" target="_blank" style="
                        display: inline-block;
                        margin-top: 8px;
                        padding: 8px 12px;
                        background-color: #1DB954;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                    ">▶️ Escuchar en Spotify</a>
                </div>
                """,
                unsafe_allow_html=True
            )
