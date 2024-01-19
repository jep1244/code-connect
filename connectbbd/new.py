import streamlit as st
import re

# Création de l'interface
st.title("Création de Compte")

nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
email = st.text_input("Email")

# Validation de l'email
if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    st.error("Email invalide")

# Création de la connexion SQL
with st.connection('account_db', type='sql') as conn:
    # Vérification du bouton d'enregistrement
    if st.button("Enregistrer"):
        if nom and prenom and email:
            # Préparation de la requête SQL
            query = f"INSERT INTO users (nom, prenom, email) VALUES (?, ?, ?)"
            conn.execute(query, (nom, prenom, email))
            st.success("Compte créé avec succès!")
        else:
            st.error("Veuillez remplir tous les champs")

