import streamlit as st
from utils import classify_text_hierarchically, format_classification_result, get_word_importance
from scrapping import find_description


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

st.title("Classification")

st.header('Transformez vos mots en informations précieuses!')   
st.write("Utilisez notre outil de classification avancé pour analyser et catégoriser vos textes.")
 
# Zone de texte pour la description du brevet
description = st.text_area('Description du Brevet')
description = description.strip()
# Bouton pour soumettre
if st.button('Classer'):
    words = description.split()
    if len(words) < 5:
        st.error("Le texte doit contenir au moins 5 mots pour effectuer la classification.")
    else:
        result = classify_text_hierarchically(description)
        formatted_result = format_classification_result(result)
        
        code_description = find_description(
                                            result['section']['code'], 
                                            result['class']['code'], 
                                            result['subclass']['code'], 
                                            result['group']['code'], 
                                            result['subgroup']['code']
                                        )            
        #for key, value in formatted_result.items():
        #    st.write(f"{key} : {value}")
        
        for (key1, value1), (key2, value2) in zip(formatted_result.items(), code_description.items()):
            st.write(f"{key1} : {value1}, {value2}")

        # Calculer l'importance des mots par perturbation
        word_importance = get_word_importance(description, "fasttext_files/sections/section_model.bin")
        st.header("Mots influents dans la prédiction")

        # Surligner le texte
        highlighted_description = highlight_text(description, word_importance, highlight_color="yellow")
        st.markdown(highlighted_description, unsafe_allow_html=True)
        
        
custom_css = f"""
    .stApp {{
        background-color: #f0f0f0;  /* Couleur de fond légère */
    }}
"""
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)