import streamlit as st
from pathlib import Path
import sys

# Ajoutez le dossier des pages au chemin d'importation
sys.path.append(str(Path(__file__).parent / 'pages'))

from login import show_login
from dashboard import show_dashboard

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Login", "Dashboard"])
    
    if selection == "Login":
        show_login()
    elif selection == "Dashboard":
        if st.session_state.get('logged_in'):
            show_dashboard()  # Affiche le tableau de bord si connecté
        else:
            st.warning("Veuillez vous connecter pour accéder au tableau de bord.")

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    main()
