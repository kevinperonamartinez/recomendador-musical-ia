# utils.py
import pandas as pd
import random
from transformers import pipeline

# Cargar géneros del dataset
df = pd.read_csv("data/Spotify-2000.csv")
GENRES_IN_DATASET = set(df['Top Genre'].unique())

# Cargar modelo Hugging Face
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analizar_estado_animo(texto_usuario):
    # Analizar sentimiento con Hugging Face
    resultado = classifier(texto_usuario)[0]
    sentiment = resultado['label']  # POSITIVE o NEGATIVE
    confidence = resultado['score']

    # Mapear sentimiento a valence y energy
    if sentiment == "POSITIVE":
        valence = round(random.uniform(0.7, 1.0), 2)
        energy = round(random.uniform(0.6, 1.0), 2)
        generos = ["pop", "dance", "electronic", "indie pop"]
    elif sentiment == "NEGATIVE":
        valence = round(random.uniform(0.0, 0.3), 2)
        energy = round(random.uniform(0.2, 0.5), 2)
        generos = ["acoustic", "sad pop", "soft rock", "blues"]
    else:  # Neutral (por si acaso)
        valence = round(random.uniform(0.3, 0.7), 2)
        energy = round(random.uniform(0.3, 0.7), 2)
        generos = ["alternative", "folk", "chillout", "lofi"]

    return {
        "generos": generos,
        "valence": valence,
        "energy": energy,
        "sentiment": sentiment,
        "sentiment_score": round(confidence, 4)
    }
