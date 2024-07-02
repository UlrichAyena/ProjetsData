import streamlit as st
import pandas as pd
import requests
import json

##Titre de l'application  dans l'onglet
st.sidebar.title("Projet de scoring")


# Affichage dans la barre latérale avec l'étiquette "Auteur"
#st.sidebar.markdown("<p style='font-weight:bold; color:black;'>Auteur :</p> <p style='color:blue;'> AYENA Mahougnon</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-weight:bold; color:black;'>Auteur :</p> <p style='color:blue;'><a href='https://www.linkedin.com/in/mahougnon-ayena'\
                     target='_blank'>AYENA Mahougnon</a></p>", unsafe_allow_html=True)

#streamlit run app.py
# Grand Titre de l'application
st.title('Prédiction des types de Clients (bon ou mauvais client ) : scoring en Banque')
# URL de l'API FastAPI
api_url = 'http://127.0.0.1:8000/predict'

# Fonction pour prédire un seul client
def predict_single(data):
    """
    Envoie une requête POST à l'API pour obtenir la prédiction pour un seul client.
    
    Args:
        data (dict): Un dictionnaire contenant les caractéristiques du client.
        
    Returns:
        dict: La prédiction et la probabilité retournées par l'API.
    """
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Erreur lors de la prédiction')
        return None

# Entrées utilisateur pour les caractéristiques du client
tranche_age = st.selectbox('Tranche d\'âge', ['de 23 a 40 ans', 'de 40 a 60 ans', 'plus de 60 ans'])
statut_matrimonial = st.selectbox('Statut matrimonial', ['célibataire', 'marié', 'divorcé', 'veuf'])
anciennete = st.selectbox('Ancienneté', ['anc. de 0 a 6 ans', 'anc. de 6 a 12 ans', 'plus de 12 ans'])
tranche_epargne = st.selectbox('Tranche d\'épargne', ['pas d\'epargne', 'moins de 50K', '50K et plus'])
profession = st.selectbox('Profession', ['employé', 'cadre', 'ouvrier', 'indépendant'])
cumul_credit = st.selectbox('Cumul de crédits', ['aucun crédit', 'de 10 à 40 débits', 'de 40 à 100 débits', 'plus de 100 débits'])
salaire = st.number_input('Salaire', min_value=0, step=100)
credit_demande = st.number_input('Crédit demandé', min_value=0, step=100)

# Bouton pour faire la prédiction pour un seul client
if st.button('Prédire'):
    # Préparation des données pour l'API
    data = {
        'tranche_age': tranche_age,
        'statut_matrimonial': statut_matrimonial,
        'anciennete': anciennete,
        'tranche_epargne': tranche_epargne,
        'profession': profession,
        'cumul_credit': cumul_credit,
        'salaire': salaire,
        'credit_demande': credit_demande
    }
    # Appel à l'API pour obtenir la prédiction
    prediction_response = predict_single(data)
    # Affichage de la prédiction
    if prediction_response:
        st.success(f'Type de client prédit : {prediction_response["prediction"]}')
        st.info(f'Probabilité associée : {prediction_response["probability"]:.2f}')

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file)
    
    # Affichage des données du CSV
    st.write("Données du fichier CSV:")
    st.write(df)
    
    # Vérification que le CSV a les bonnes colonnes
    expected_columns = ['tranche_age', 'statut_matrimonial', 'anciennete', 'tranche_epargne', 'profession', 'cumul_credit', 'salaire', 'credit_demande']
    if all(col in df.columns for col in expected_columns):
        # Préparer les données pour l'API
        data = df[expected_columns].to_dict(orient='records')
        
        # Faire les prédictions pour chaque ligne du CSV
        predictions = [predict_single(d) for d in data]
        
        # Extraire les prédictions et les probabilités
        predictions_labels = [pred["prediction"] for pred in predictions]
        predictions_probas = [pred["probability"] for pred in predictions]
        
        # Ajouter les prédictions et les probabilités au DataFrame
        df['prediction'] = predictions_labels
        df['probability'] = predictions_probas
        
        # Afficher le DataFrame avec les prédictions
        st.write("Résultats avec les prédictions:")
        st.write(df)
    else:
        # Message d'erreur si les colonnes sont incorrectes
        st.error(f"Le fichier CSV doit contenir les colonnes suivantes: {expected_columns}")

