import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(df):
    # Exemple de traitement : gérer les valeurs manquantes
    df = df.dropna()
    return df
