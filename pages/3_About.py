import streamlit as st

st.title('À propos')
st.header('Qui sommes nous ?')
st.write("""
StarPC-Forest est une application développée avec Streamlit permettant de prédire la catégorie d'un brevet entré par l'utilisateur.
Le modèle est entraîné en utilisant FastText.
""")
st.write("""
### Notre équipe
""")
col1, col2, col3, col4, col5 = st.columns(5)
# Exemple d'image en ligne avec texte en dessous
with col1:
    st.image('./assets/edema.jpg')
    st.markdown("[Edem Adjovi](https://www.linkedin.com/in/edem-adjovi/)")

with col2:
    st.image('https://via.placeholder.com/150')
    st.markdown("[Hissein Doudou](https://www.linkedin.com/in/hisseindoudou/)")

with col3:
    st.image('./assets/olivierl.jpg')
    st.markdown("[Olivier Leroi--Morant](https://www.linkedin.com/in/olivier-leroi-morant-data-science/)")

with col4:
    st.image('./assets/kevm.jpg')
    st.markdown("[Kevin Munto](https://www.linkedin.com/in/muntokevin-s600e320/)")

with col5:
    st.image('./assets/oumart.jpg')
    st.markdown("[Oumar Traoré](https://www.linkedin.com/in/oumar-traoré-789245221/)")


# Vous pouvez ajouter autant d'images que nécessaire avec leurs descriptions

st.write('---')
st.write('Développé par les Seaborn Sailors.')


st.markdown(
    """
    <style>
    a {
        text-decoration: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


custom_css = f"""
    .stApp {{
        background-color: #f0f0f0;  /* Couleur de fond légère */
    }}
"""
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)