import streamlit as st

def show_login():
    st.title("Agrisense - Login")
    
    # Entrée de l'utilisateur
    username = st.text_input("Nom d'utilisateur", key="username")
    password = st.text_input("Mot de passe", type="password", key="password")
    
    # Bouton de connexion
    if st.button("Login"):
        if check_login(username, password):
            st.session_state['logged_in'] = True
            st.success("Connexion réussie! Redirection vers le tableau de bord...")
            # Redirection vers le tableau de bord après connexion
            st.experimental_set_query_params(page="dashboard")
        else:
            st.error("Identifiants incorrects. Réessayez.")

def check_login(username, password):
    valid_username = "admin"
    valid_password = "1234"
    return username == valid_username and password == valid_password

def main():
    # Gestion de la redirection
    page = st.experimental_get_query_params().get('page', [''])[0]
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.write("Tableau de bord")
    else:
        show_login()

if __name__ == "__main__":
    main()
