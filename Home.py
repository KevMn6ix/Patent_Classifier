import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Titre de l'application
st.title('StarPC-Forest')

st.header('Bienvenue sur notre application de classification de texte')
st.write("Cette application vous permet de classifier des textes en différentes catégories grâce à un modèle d'intelligence artificielle.")
st.image('https://via.placeholder.com/600x300', caption='Notre Logo')

st.header('Fonctionnalités')
st.write('Voici ce que notre application peut faire :')
st.markdown("""
- **Classifications précises** : Utilise un modèle d'intelligence artificielle avancé.
- **Interface utilisateur conviviale** : Facile à utiliser et à naviguer.
- **Rapidité** : Obtenez des résultats en temps réel.
""")

# Call to Action
st.markdown("---")
st.header("Prêt à essayer notre produit ?")
st.write("Rendez-vous dans la page classification ou vous pourrez classifier tout les textes que vous voulez !")
    
# Footer
st.markdown("---")
st.write("© 2024. Seaborn Sailors. Tous droits réservés.")

# Personnalisation du thème pour une apparence colorée et agréable
# Couleurs personnalisées
primary_color = "#FF5733"  # Orange vif
secondary_color = "#FFCBA4"  

# Appliquer le thème personnalisé
custom_css = f"""
    .stApp {{
        background-color: #f0f0f0;  /* Couleur de fond légère */
    }}
    .stButton button {{
        background-color: {primary_color};  /* Couleur de fond du bouton */
        color: white;  /* Couleur du texte du bouton */
    }}
    .stButton button:hover {{
        background-color: {secondary_color};  /* Couleur de fond au survol */
    }}
    .stMarkdown, .stText, .stTextInput {{
        color: #333;  /* Couleur du texte principal */
    }}
"""
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)




