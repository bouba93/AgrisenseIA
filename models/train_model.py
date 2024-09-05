import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Définir les seuils
THRESHOLDS = {
    'Temperature (°C)': {
        'optimal': (18, 22),
        'good': (15, 25),
        'critical': (10, 30),
        'dangerous': (-float('inf'), 35)
    },
    'Humidity (%)': {
        'optimal': (40, 50),
        'good': (30, 60),
        'critical': (20, 70),
        'dangerous': (-float('inf'), 80)
    },
    'Nutrients (g/L)': {
        'optimal': (1.5, 2.5),
        'good': (1.0, 3.5),
        'critical': (0.5, 4.0),
        'dangerous': (-float('inf'), 5.0)
    },
    'pH': {
        'optimal': (6.0, 6.5),
        'good': (5.5, 7.0),
        'critical': (5.0, 7.5),
        'dangerous': (-float('inf'), 8.0)
    }
}

def load_data(file_path):
    """Charge les données depuis un fichier CSV."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Les données ont été chargées depuis {file_path}.")
        return df
    except FileNotFoundError:
        logging.error(f"Erreur : le fichier {file_path} est introuvable.")
        raise
    except Exception as e:
        logging.error(f"Erreur lors du chargement des données : {e}")
        raise

def prepare_data(df):
    """Prépare les données pour l'entraînement du modèle."""
    required_columns = ['Temperature (°C)', 'Humidity (%)', 'Nutrients (g/L)', 'pH', 'Recommendations']
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        logging.error(f"Erreur : colonnes manquantes dans les données - {', '.join(missing_cols)}")
        raise KeyError(f"Colonnes manquantes : {', '.join(missing_cols)}")

    X = df[['Temperature (°C)', 'Humidity (%)', 'Nutrients (g/L)', 'pH']]
    y = df['Recommendations']
    logging.info("Les données ont été préparées pour l'entraînement.")
    return X, y

def train_model(X, y):
    """Entraîne un modèle de classification RandomForest."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    logging.info("Le modèle a été entraîné.")
    return model

def save_model(model, file_path):
    """Sauvegarde le modèle entraîné dans un fichier."""
    try:
        joblib.dump(model, file_path)
        logging.info(f"Le modèle a été sauvegardé dans {file_path}.")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde du modèle : {e}")
        raise

def generate_recommendations(row):
    """Génère des recommandations pour une seule ligne de données."""
    recs = []

    for param in ['Temperature (°C)', 'Humidity (%)', 'Nutrients (g/L)', 'pH']:
        value = row[param]
        thresholds = THRESHOLDS[param]
        
        if thresholds['optimal'][0] <= value <= thresholds['optimal'][1]:
            status = "optimal"
        elif thresholds['good'][0] <= value <= thresholds['good'][1]:
            status = "good"
        elif thresholds['critical'][0] <= value <= thresholds['critical'][1]:
            status = "critical"
        else:
            status = "dangerous"
        
        if status == "optimal":
            recs.append(f"{param} est dans la plage optimale.")
        elif status == "good":
            recs.append(f"{param} est dans la plage bonne, mais pourrait être amélioré.")
        elif status == "critical":
            recs.append(f"{param} est critique. Des ajustements sont nécessaires.")
        else:
            recs.append(f"{param} est dangereux. Des mesures immédiates sont requises.")
    
    return " ".join(recs) if recs else "Aucune recommandation spécifique."

def make_recommendations(df):
    """Fait des recommandations basées sur les valeurs des caractéristiques."""
    df['Recommendations'] = df.apply(generate_recommendations, axis=1)
    return df['Recommendations']

if __name__ == "__main__":
    # Définir les chemins relatifs
    base_path = 'C:/Users/ODC/OneDrive/Desktop/Agri_Predictor/data'
    data_path = os.path.join(base_path, 'agriculture_data.csv')
    model_path = os.path.join(base_path, 'model.pkl')
    output_data_path = os.path.join(base_path, 'agriculture_data_with_recommendations.csv')

    # Chargement des données
    df = load_data(data_path)
    
    # Préparation des données
    X, y = prepare_data(df)
    
    # Entraînement du modèle
    model = train_model(X, y)
    
    # Sauvegarde du modèle
    save_model(model, model_path)
    
    # Faire des prédictions et obtenir des recommandations
    predictions = model.predict(X)
    df['Model Predictions'] = predictions
    recommendations = make_recommendations(df)
    
    # Ajouter les recommandations au DataFrame
    df['Recommendations'] = recommendations
    
    # Sauvegarder le DataFrame avec les recommandations ajoutées
    df.to_csv(output_data_path, index=False)
    logging.info("Les recommandations ont été ajoutées aux données et sauvegardées.")
