import streamlit as st
import fasttext
import os

st.title('EXplain')

menu = st.sidebar.selectbox('Menu', options=['Page principale', 'Classification', 'About Us'])

# Directory where FastText models are stored
base_dir = "fasttext_files/sections"

if menu == 'Page principale':
    st.header('Bienvenue sur notre application de classification de texte')
    st.write("Cette application vous permet de classifier des textes en différentes catégories grâce à un modèle d'intelligence artificielle.")
    st.image('https://via.placeholder.com/300x150', caption='Notre Logo')

    st.header('Fonctionnalités')
    st.write('Voici ce que notre application peut faire :')
    st.markdown("""
    - **Classifications précises** : Utilise un modèle d'intelligence artificielle' avancé.
    - **Interface utilisateur conviviale** : Facile à utiliser et à naviguer.
    - **Rapidité** : Obtenez des résultats en temps réel.
    """)
    
    #st.header('Commencez maintenant')
    #st.write('Prêt à essayer notre application de classification de texte ?')
    #if st.button('Cliquez ici pour classifier un texte'):
        #st.session_state.page = 'Classification'
        
elif menu == 'Classification':
    st.header('Classification de Texte')    
    # CPC codes dictionary for descriptions
    cpc_codes = {
        "A": "Human necessities",
        "B": "Performing operations; transporting",
        "C": "Chemistry; metallurgy",
        "D": "Textiles; paper",
        "E": "Fixed constructions",
        "F": "Mechanical engineering; lighting; heating; weapons; blasting engines or pumps",
        "G": "Physics",
        "H": "Electricity",
        "Y": "General tagging of new technological developments; general tagging of cross-sectional technologies spanning over several sections of the IPC; technical subjects covered by former USPC cross-reference art collections [XRACs] and digests"
    }

    def get_cpc_description(cpc_section):
        return cpc_codes.get(cpc_section, "Unknown CPC section")

    def classify_text_hierarchically(text):
        # Function to classify text at each hierarchical level

        def load_and_predict(model_path, text):
            if not os.path.exists(model_path):
                return None, None
            model = fasttext.load_model(model_path)
            predicted_class, probability = model.predict(text)
            return predicted_class[0].split("__label__")[-1], probability[0]

        result = {}
        
        # Level 1: CPC Section
        section_model_path = os.path.join(base_dir, "section_model.bin")
        cpc_section, section_prob = load_and_predict(section_model_path, text)
        if cpc_section is None:
            result['section'] = "Model not found"
            return result

        result['section'] = {
            'code': cpc_section,
            'description': get_cpc_description(cpc_section),
            'probability': section_prob
        }
        
        # Level 2: CPC Class
        class_model_path = os.path.join(base_dir, f"section_{cpc_section}", "class_model.bin")
        cpc_class, class_prob = load_and_predict(class_model_path, text)
        if cpc_class is None:
            result['class'] = "Model not found"
            return result

        result['class'] = {'code': cpc_class, 'probability': class_prob}

        # Level 3: CPC Subclass
        subclass_model_path = os.path.join(base_dir, f"section_{cpc_section}", f"class_{cpc_class}", "subclass_model.bin")
        cpc_subclass, subclass_prob = load_and_predict(subclass_model_path, text)
        if cpc_subclass is None:
            result['subclass'] = "Model not found"
            return result

        result['subclass'] = {'code': cpc_subclass, 'probability': subclass_prob}

        # Level 4: CPC Group
        group_model_path = os.path.join(base_dir, f"section_{cpc_section}", f"class_{cpc_class}", f"subclass_{cpc_subclass}", "group_model.bin")
        cpc_group, group_prob = load_and_predict(group_model_path, text)
        if cpc_group is None:
            result['group'] = "Model not found"
            return result

        result['group'] = {'code': cpc_group, 'probability': group_prob}

        # Level 5: CPC Subgroup
        subgroup_model_path = os.path.join(base_dir, f"section_{cpc_section}", f"class_{cpc_class}", f"subclass_{cpc_subclass}", f"group_{cpc_group}", "subgroup_model.bin")
        cpc_subgroup, subgroup_prob = load_and_predict(subgroup_model_path, text)
        if cpc_subgroup is None:
            result['subgroup'] = "Model not found"
            return result

        result['subgroup'] = {'code': cpc_subgroup, 'probability': subgroup_prob}

        # Combine the full CPC code
        result['full_cpc_code'] = f"{cpc_section}{cpc_class}{cpc_subclass}{cpc_group}/{cpc_subgroup}"

        return result


    def format_classification_result(result):
        if 'section' in result and isinstance(result['section'], dict):
            section_desc = f"{result['section']['code']} - {result['section']['description']} (Probability: {result['section']['probability']:.2f})"
        else:
            section_desc = "Section model not found"
        
        cpc_class = result.get('class', "Class model not found")
        if isinstance(cpc_class, dict):
            class_desc = f"{cpc_class['code']} (Probability: {cpc_class['probability']:.2f})"
        else:
            class_desc = cpc_class
        
        cpc_subclass = result.get('subclass', "Subclass model not found")
        if isinstance(cpc_subclass, dict):
            subclass_desc = f"{cpc_subclass['code']} (Probability: {cpc_subclass['probability']:.2f})"
        else:
            subclass_desc = cpc_subclass
        
        cpc_group = result.get('group', "Group model not found")
        if isinstance(cpc_group, dict):
            group_desc = f"{cpc_group['code']} (Probability: {cpc_group['probability']:.2f})"
        else:
            group_desc = cpc_group
        
        cpc_subgroup = result.get('subgroup', "Subgroup model not found")
        if isinstance(cpc_subgroup, dict):
            subgroup_desc = f"{cpc_subgroup['code']} (Probability: {cpc_subgroup['probability']:.2f})"
        else:
            subgroup_desc = cpc_subgroup
        
        full_cpc_code = result.get('full_cpc_code', "Full CPC code not found")

        formatted_result = {
            'Section' : section_desc,
            'Class' : class_desc,
            'Subclass' : subclass_desc,
            'Subgroup' : subgroup_desc,
            'Full CPC Code' : full_cpc_code
        }

        return formatted_result

    # Zone de texte pour la description du brevet
    description = st.text_area('Description du Brevet')

    # Bouton pour soumettre
    classification_log = []
    if st.button('Classer'):
        
        result = classify_text_hierarchically(description)
        formatted_result = format_classification_result(result)
    
        for key, value in formatted_result.items():
            st.write(f"{key} : {value}")
            
else:
    st.header('À propos')
    st.write("""
    Cette application est développée avec Streamlit pour prédire la classe d'un texte entré par l'utilisateur.
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