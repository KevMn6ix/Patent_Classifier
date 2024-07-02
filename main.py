import streamlit as st
from utils import classify_text_hierarchically, format_classification_result, get_word_importance
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Titre de l'application
st.title('EXplain')

# Menu latéral pour la navigation
menu = st.sidebar.selectbox('Menu', options=['Page principale', 'Classification', 'Évolution des Scores'])

# Fonction pour surligner les mots dans le texte
def highlight_text(text, word_importance, highlight_color="yellow"):
    words = text.split()
    highlighted_text = ""

    important_words = {w.lower() for w, s in word_importance}  # Ensemble de mots importants pour recherche rapide

    for word in words:
        lower_word = word.lower()
        if lower_word in important_words:
            highlighted_text += f'<span style="background-color: {highlight_color}">{word}</span> '
        else:
            highlighted_text += word + ' '

    return highlighted_text

# Afficher le contenu basé sur le menu sélectionné
if menu == 'Page principale':
    st.header('Bienvenue sur notre application de classification de texte')
    st.write("Cette application vous permet de classifier des textes en différentes catégories grâce à un modèle d'intelligence artificielle.")
    st.image('https://via.placeholder.com/300x150', caption='Notre Logo')

    st.header('Fonctionnalités')
    st.write('Voici ce que notre application peut faire :')
    st.markdown("""
    - **Classifications précises** : Utilise un modèle d'intelligence artificielle avancé.
    - **Interface utilisateur conviviale** : Facile à utiliser et à naviguer.
    - **Rapidité** : Obtenez des résultats en temps réel.
    """)

elif menu == 'Classification':
    st.header('Classification de Texte')    
    # Zone de texte pour la description du brevet
    description = st.text_area('Description du Brevet')

    # Bouton pour soumettre
    if st.button('Classer'):
        words = description.split()
        if len(words) < 5:
            st.error("Le texte doit contenir au moins 5 mots pour effectuer la classification.")
        else:
            result = classify_text_hierarchically(description)
            formatted_result = format_classification_result(result)
        
            for key, value in formatted_result.items():
                st.write(f"{key} : {value}")

            # Calculer l'importance des mots par perturbation
            word_importance = get_word_importance(description, "fasttext_files/sections/section_model.bin")
            st.header("Mots influents dans la prédiction")

            # Surligner le texte
            highlighted_description = highlight_text(description, word_importance, highlight_color="yellow")
            st.markdown(highlighted_description, unsafe_allow_html=True)

elif menu == 'Évolution des Scores':
    st.header("Évolution des Scores F1")
    st.write("Voici l'évolution des scores F1 en fonction des niveaux (section, classe, etc.).")

    # Utilisation d'un iframe pour afficher le document HTML
    html_file = 'scores_evolution.html'
    with open(html_file, 'r') as f:
        html_content = f.read()
    
    st.components.v1.html(html_content, height=800, scrolling=True)
