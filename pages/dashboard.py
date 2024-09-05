import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

@st.cache_data
def load_data(data_path):
    """Charge les données depuis un fichier CSV avec mise en cache."""
    df = pd.read_csv(data_path)
    return df

@st.cache_resource
def load_model(model_path):
    """Charge le modèle depuis un fichier avec mise en cache."""
    model = joblib.load(model_path)
    return model

def generate_recommendations(row):
    """Génère des recommandations et des conseils basés sur les seuils définis pour une seule ligne de données."""
    recs = []
    advice = []
    thresholds = {
        'Temperature (°C)': {
            'optimal': (18, 22),
            'good': (15, 25),
            'critical': (10, 30),
            'dangerous': (-float('inf'), 35),
            'advice': {
                'optimal': "La température est parfaite pour une croissance optimale des plantes.",
                'good': "La température est adéquate, mais vous pourriez surveiller de près pour éviter des fluctuations.",
                'critical': "La température devient critique. Ajustez l'irrigation ou l'ombrage pour éviter des dommages.",
                'dangerous': "Les températures sont dangereuses. Prenez immédiatement des mesures pour protéger vos cultures."
            }
        },
        'Humidity (%)': {
            'optimal': (40, 50),
            'good': (30, 60),
            'critical': (20, 70),
            'dangerous': (-float('inf'), 80),
            'advice': {
                'optimal': "L'humidité est parfaite pour une bonne absorption de l'eau par les plantes.",
                'good': "L'humidité est bonne, mais vérifiez l'irrigation pour maintenir ces niveaux.",
                'critical': "L'humidité est critique. Vous devriez ajuster l'irrigation pour éviter un stress hydrique.",
                'dangerous': "L'humidité est dangereusement élevée ou basse. Des actions immédiates sont nécessaires."
            }
        },
        'Nutrients (g/L)': {
            'optimal': (1.5, 2.5),
            'good': (1.0, 3.5),
            'critical': (0.5, 4.0),
            'dangerous': (-float('inf'), 5.0),
            'advice': {
                'optimal': "Les niveaux de nutriments sont parfaits, garantissant une croissance saine.",
                'good': "Les nutriments sont bons. Continuez à surveiller et ajuster si nécessaire.",
                'critical': "Les niveaux de nutriments sont critiques. Envisagez d'ajouter des engrais spécifiques.",
                'dangerous': "Les niveaux de nutriments sont trop bas ou trop élevés. Corrigez immédiatement pour éviter des pertes."
            }
        },
        'pH': {
            'optimal': (6.0, 6.5),
            'good': (5.5, 7.0),
            'critical': (5.0, 7.5),
            'dangerous': (-float('inf'), 8.0),
            'advice': {
                'optimal': "Le pH du sol est parfait pour une absorption optimale des nutriments.",
                'good': "Le pH est acceptable, mais surveillez-le pour maintenir cette bonne condition.",
                'critical': "Le pH est critique. Vous devriez envisager des amendements pour ajuster les niveaux.",
                'dangerous': "Le pH est dangereux. Corrigez immédiatement pour éviter des blocages de nutriments."
            }
        }
    }
    
    for param in ['Temperature (°C)', 'Humidity (%)', 'Nutrients (g/L)', 'pH']:
        value = row[param]
        thresh = thresholds[param]
        
        if thresh['optimal'][0] <= value <= thresh['optimal'][1]:
            status = "optimal"
        elif thresh['good'][0] <= value <= thresh['good'][1]:
            status = "good"
        elif thresh['critical'][0] <= value <= thresh['critical'][1]:
            status = "critical"
        else:
            status = "dangerous"
        
        # Ajouter les recommandations et conseils
        recs.append(f"{param} est dans la plage {status}.")
        advice.append(thresh['advice'][status])
    
    return " ".join(recs), " ".join(advice)

def show_dashboard():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("Veuillez vous connecter pour accéder au tableau de bord.")
        return

    st.title("Bienvenue à Agrisense")

    # Définir les chemins des fichiers
    data_path = 'data/agriculture_data.csv'
    model_path = 'models/model.pkl'

    # Vérification de l'existence des fichiers
    if not os.path.exists(data_path):
        st.error(f"Le fichier de données {data_path} est introuvable.")
        return

    if not os.path.exists(model_path):
        st.error(f"Le fichier du modèle {model_path} est introuvable.")
        return

    # Chargement des données et du modèle avec mise en cache
    df = load_data(data_path)
    model = load_model(model_path)
    
    # Vérifiez si la colonne 'Date' existe
    if 'Date' not in df.columns:
        st.error("La colonne 'Date' est manquante dans le fichier CSV.")
        return
    
    # Ajout d'une sélection de plage de dates
    st.subheader("Sélectionnez une période pour analyser les données")
    st.info("Utilisez les sélecteurs de date pour choisir la période d'analyse des données.")
    try:
        start_date = st.date_input("Date de début", value=pd.to_datetime(df['Date']).min())
        end_date = st.date_input("Date de fin", value=pd.to_datetime(df['Date']).max())
    except Exception as e:
        st.error(f"Erreur lors de la sélection des dates : {e}")
        return

    # Filtrer les données en fonction de la plage de dates
    try:
        filtered_df = df[(pd.to_datetime(df['Date']) >= pd.to_datetime(start_date)) & 
                         (pd.to_datetime(df['Date']) <= pd.to_datetime(end_date))]
    except Exception as e:
        st.error(f"Erreur lors du filtrage des données : {e}")
        return

    # Visualisation des données
    st.subheader("Évolution de la température")
    st.info("Visualisez l'évolution de la température sur la période sélectionnée.")
    fig = px.line(filtered_df, x='Date', y="Temperature (°C)", title="Température au fil du temps")
    st.plotly_chart(fig)
    
    st.subheader("Évolution de l'humidité")
    st.info("Visualisez l'évolution de l'humidité sur la période sélectionnée.")
    fig2 = px.line(filtered_df, x='Date', y="Humidity (%)", title="Humidité au fil du temps")
    st.plotly_chart(fig2)
    
    st.subheader("Évolution des nutriments")
    st.info("Visualisez l'évolution des niveaux de nutriments sur la période sélectionnée.")
    fig3 = px.line(filtered_df, x='Date', y="Nutrients (g/L)", title="Nutriments au fil du temps")
    st.plotly_chart(fig3)
    
    st.subheader("Évolution du pH")
    st.info("Visualisez l'évolution du pH sur la période sélectionnée.")
    fig4 = px.line(filtered_df, x='Date', y="pH", title="pH au fil du temps")
    st.plotly_chart(fig4)
    
    # Entrée des données de capteurs pour la prédiction
    st.subheader("Entrée des données des capteurs pour la prédiction")
    st.info("Saisissez les valeurs des capteurs pour obtenir une prédiction et des recommandations.")
    temp = st.number_input("Température (°C)", min_value=10.0, max_value=40.0, step=0.5, help="Entrez la température actuelle mesurée en degrés Celsius.")
    humidity = st.number_input("Humidité (%)", min_value=10.0, max_value=100.0, step=1.0, help="Entrez l'humidité actuelle mesurée en pourcentage.")
    nutrients = st.number_input("Nutriments (g/L)", min_value=0.0, max_value=20.0, step=0.1, help="Entrez le niveau actuel des nutriments mesuré en grammes par litre.")
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1, help="Entrez le niveau actuel du pH du sol.")

    if st.button("Prédire et Recommander"):
        new_data = pd.DataFrame([[temp, humidity, nutrients, ph]], columns=['Temperature (°C)', 'Humidity (%)', 'Nutrients (g/L)', 'pH'])
        
        # Prédiction
        try:
            prediction = model.predict(new_data)[0]
            st.success(f"Recommandation : {prediction}")
            
            # Suggestions basées sur les seuils et conseils
            recommendations, advice = generate_recommendations({
                'Temperature (°C)': temp,
                'Humidity (%)': humidity,
                'Nutrients (g/L)': nutrients,
                'pH': ph
            })
            
            st.info(recommendations)
            st.info(f"Conseils : {advice}")
            
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")

