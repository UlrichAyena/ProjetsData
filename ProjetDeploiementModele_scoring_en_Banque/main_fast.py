from fastapi import FastAPI
from pydantic import BaseModel
import joblib # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore

# Chargement du modèle et des colonnes de caractéristiques
model = joblib.load("model_regLogi.pkl")
feature_columns = joblib.load("feature_columns.pkl")  # Charger les colonnes sauvegardées

scaler = joblib.load('scaler.pkl') 

# Initialisation de l'application FastAPI
app = FastAPI()

# Définition du schéma de la requête
class ClientData(BaseModel):
    tranche_age: str
    statut_matrimonial: str
    anciennete: str
    tranche_epargne: str
    profession: str
    cumul_credit: str
    salaire: int
    credit_demande: int


# Endpoint d'accueil
@app.get("/")
def read_root():
    """
    Endpoint d'accueil de l'API.
    Retourne un message de bienvenue avec une indication sur l'utilisation de l'API.
    """
    return {"message": "Bienvenue à l'API de prédiction des clients. Utilisez l'endpoint /predict pour faire des prédictions."}

# Endpoint pour prédire le type de client
@app.post("/predict")
def predict(data: ClientData):
    # Conversion des données d'entrée en DataFrame
    df = pd.DataFrame([data.model_dump()])
    # Normalisation des variables numériques
    var = ['salaire', 'credit_demande']
    df[var] = scaler.transform(df[var])

    # Encodage des données d'entrée
    df_dummies = pd.get_dummies(df)
    df_dummies = df_dummies.reindex(columns=feature_columns, fill_value=0)
    
    # Faire une prédiction
    prediction = model.predict( df_dummies)
    prediction_proba = model.predict_proba(df_dummies)
    # Obtention de la probabilité associée à la classe prédite
    predicted_class = prediction[0]
    predicted_proba = prediction_proba[0][predicted_class]

    prediction_label = 'Bon client' if predicted_class == 1 else 'Mauvais client'
    
    # Retourne la prédiction et la probabilité associée
    return {
        "prediction": prediction_label,
        "probability": predicted_proba
    }
    
# Pour démarrer le serveur : uvicorn main_fast:app --reload
