import streamlit as st

st.title("Evaluation des Performances")

st.header("Évaluation des Scores")
st.write("Analysez les performances de votre modèle avec différentes métriques d'évaluation.")

# Utilisation d'un iframe pour afficher le document HTML
html_file = 'f1_score_evolution.html'
with open(html_file, 'r') as f:
    html_content = f.read()

st.components.v1.html(html_content, height=800, scrolling=True)

custom_css = f"""
    .stApp {{
        background-color: #f0f0f0;  /* Couleur de fond légère */
    }}
"""
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)