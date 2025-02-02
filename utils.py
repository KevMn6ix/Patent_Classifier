# utils.py
import fasttext
import os
from nltk.corpus import stopwords


# Répertoire où sont stockés les modèles FastText
base_dir = "fasttext_files/sections"

# Liste des stop words
stop_words = set(stopwords.words('english'))

# Dictionnaire des codes CPC pour les descriptions
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

# Fonction pour obtenir la description du code CPC
def get_cpc_description(cpc_section):
    return cpc_codes.get(cpc_section, "Unknown CPC section")

# Fonction pour enlever les stop words du texte
def remove_stopwords(text):
    words = text.split()
    filtered_text = ' '.join(word for word in words if word.lower() not in stop_words)
    return filtered_text

# Fonction pour classifier le texte à chaque niveau hiérarchique
def classify_text_hierarchically(text):
    text = remove_stopwords(text)  # Enlever les stop words ici
    def load_and_predict(model_path, text):
        if not os.path.exists(model_path):
            return None, None
        model = fasttext.load_model(model_path)
        predicted_class, probability = model.predict(text)
        return predicted_class[0].split("__label__")[-1], probability[0]

    result = {}

    # Niveau 1 : Section CPC
    section_model_path = os.path.join(base_dir, "section_model.bin")
    cpc_section, section_prob = load_and_predict(section_model_path, text)
    if cpc_section is None:
        result['section'] = "Model not found"
        return result

    """result['section'] = {
        'code': cpc_section,
        'description': get_cpc_description(cpc_section),
        'probability': section_prob
    }"""
    
    result['section'] = {
        'code': cpc_section,
        'probability': section_prob
    }

    # Niveau 2 : Classe CPC
    class_model_path = os.path.join(base_dir, f"section_{cpc_section}", "class_model.bin")
    cpc_class, class_prob = load_and_predict(class_model_path, text)
    if cpc_class is None:
        result['class'] = "Model not found"
        return result

    result['class'] = {'code': cpc_class, 'probability': class_prob}

    # Niveau 3 : Sous-classe CPC
    subclass_model_path = os.path.join(base_dir, f"section_{cpc_section}", f"class_{cpc_class}", "subclass_model.bin")
    cpc_subclass, subclass_prob = load_and_predict(subclass_model_path, text)
    if cpc_subclass is None:
        result['subclass'] = "Model not found"
        return result

    result['subclass'] = {'code': cpc_subclass, 'probability': subclass_prob}

    # Niveau 4 : Groupe CPC
    group_model_path = os.path.join(base_dir, f"section_{cpc_section}", f"class_{cpc_class}", f"subclass_{cpc_subclass}", "group_model.bin")
    cpc_group, group_prob = load_and_predict(group_model_path, text)
    if cpc_group is None:
        result['group'] = "Model not found"
        return result

    result['group'] = {'code': cpc_group, 'probability': group_prob}

    # Niveau 5 : Sous-groupe CPC
    subgroup_model_path = os.path.join(base_dir, f"section_{cpc_section}", f"class_{cpc_class}", f"subclass_{cpc_subclass}", f"group_{cpc_group}", "subgroup_model.bin")
    cpc_subgroup, subgroup_prob = load_and_predict(subgroup_model_path, text)
    if cpc_subgroup is None:
        result['subgroup'] = "Model not found"
        return result

    result['subgroup'] = {'code': cpc_subgroup, 'probability': subgroup_prob}

    # Combiner le code CPC complet
    result['full_cpc_code'] = f"{cpc_section}{cpc_class}{cpc_subclass}{cpc_group}/{cpc_subgroup}"

    return result

# Fonction pour formater le résultat de la classification
def format_classification_result(result):
    if 'section' in result and isinstance(result['section'], dict):
        #section_desc = f"{result['section']['code']} - {result['section']['description']} (Probability: {result['section']['probability']:.2f})"
        section_desc = f"{result['section']['code']} (Probability: {result['section']['probability']:.2f})"
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
        'Section': section_desc,
        'Class': class_desc,
        'Subclass': subclass_desc,
        'Group': group_desc,
        'Subgroup': subgroup_desc,
        'Full CPC Code': full_cpc_code
    }

    return formatted_result

# Fonction pour calculer l'importance des mots par perturbation
def get_word_importance(text, model_path):
    model = fasttext.load_model(model_path)
    
    # Prédiction originale
    original_label, original_prob = model.predict(text)
    original_prob = original_prob[0]
    
    words = text.split()
    importance_scores = []
    seen_words = set()
    
    for i, word in enumerate(words):
        if word in seen_words or word.lower() in stop_words:  # Ignorer les stop words et les doublons
            continue
        seen_words.add(word)
        perturbed_text = ' '.join(words[:i] + words[i+1:])
        perturbed_label, perturbed_prob = model.predict(perturbed_text)
        perturbed_prob = perturbed_prob[0]
        
        importance_score = original_prob - perturbed_prob
        if importance_score > 0:  
            importance_scores.append((word, importance_score))
    
    # Trier les mots par importance
    importance_scores.sort(key=lambda x: x[1], reverse=True)
    
    return importance_scores
