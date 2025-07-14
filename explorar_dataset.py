import pandas as pd 

df = pd.read_csv("data/Spotify-2000.csv")

print(df.columns)
print(df['Top Genre'].unique())
canciones_relajadas = df[(df['Valence'] > 0.7) & (df['Beats Per Minute (BPM)'] < 90)]
print(canciones_relajadas[['Title', 'Artist', 'Top Genre']].head())