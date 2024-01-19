import streamlit as st
from sqlalchemy.sql import text

# Connexion à la base de données
conn = st.connection('account_db', type='sql')

# Onglets pour Création de Compte et Paramètres
tab1, tab2 = st.tabs(["Création de Compte", "Paramètres"])

# Onglet pour la création de compte
with tab1:
    st.title("Création de compte utilisateur")

    # Champs de saisie pour les informations de l'utilisateur
    first_name = st.text_input("Prénom", key="first_name")
    last_name = st.text_input("Nom de famille", key="last_name")
    email = st.text_input("Email", key="email")

    # Bouton pour enregistrer les informations
    if st.button("Enregistrer", key="create"):
        if not first_name or not last_name or not email:
            st.error("Le prénom, le nom de famille et l'email sont obligatoires.")
        else:
            # Vérification de l'unicité de l'email
            with conn.session as s:
                existing_email = s.execute(text("SELECT email FROM account WHERE email = :email"), {'email': email}).fetchone()
                if existing_email is not None:
                    st.error("Un compte avec cet email existe déjà.")
                else:
                    # Insertion des informations dans la table 'account'
                    create_account_sql = text('''
                        INSERT INTO account (first_name, last_name, email) 
                        VALUES (:first_name, :last_name, :email);
                    ''')
                    s.execute(
                        create_account_sql,
                        params=dict(
                            first_name=first_name,
                            last_name=last_name,
                            email=email
                        )
                    )
                    s.commit()
                    st.success("Les informations du compte utilisateur ont été enregistrées avec succès.")

# Onglet Paramètres pour la suppression de compte
with tab2:
    st.title("Paramètres")

    # Suppression de compte utilisateur
    st.subheader("Supprimer un compte utilisateur")
    delete_email = st.text_input("Entrez l'email du compte à supprimer", key="delete_email")

    if st.button("Supprimer le compte", key="delete"):
        if delete_email:
            with conn.session as s:
                delete_query = text("DELETE FROM account WHERE email = :email")
                s.execute(delete_query, {'email': delete_email})
                s.commit()
            st.success(f"Le compte avec l'email {delete_email} a été supprimé.")
        else:
            st.error("Veuillez entrer un email valide.")

# Affichage des comptes enregistrés
with conn.session as s:
    accounts = s.execute(text('SELECT * FROM account')).fetchall()
    st.subheader("Liste des comptes utilisateurs enregistrés :")
    st.dataframe(accounts)
