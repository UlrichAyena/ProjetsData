## Déploiement d'un Modèle de Machine Learning avec FastAPI sur le cloud Render dashboard et intégration avec Streamlit

  Ce projet vise à déployer un modèle de machine learning destiné au scoring bancaire, permettant de distinguer les bons des mauvais clients. Le modèle est initialement déployé via une application FastAPI sur render dashboard, puis intégré à une interface utilisateur interactive avec Streamlit.

 ##### FastAPI
  - uvicorn main_fast:app --reload 
 ##### Render dashboard
   services:
  - type: web
    name: my-fastapi-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port 10000
 ##### Streamlit 
  - streamlit run app_streamlit.py 

  Voici le lien final de l'application : 


  FastAPI
  Render
  Deploy
  API
  Python
  Stremlit
