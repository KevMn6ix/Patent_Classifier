from flask import Flask, request, render_template
import fasttext
import os

app = Flask(__name__)

classification_log = []

# Directory where FastText models are stored
base_dir = "fasttext_files/sections"

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
    
    # Level 1: CPC Sections
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

# format classification to display the result
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

    formatted_result = (
        f"Section: {section_desc}\n"
        f"Class: {class_desc}\n"
        f"Subclass: {subclass_desc}\n"
        f"Group: {group_desc}\n"
        f"Subgroup: {subgroup_desc}\n"
        f"Full CPC Code: {full_cpc_code}"
    )
    return formatted_result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['text']
        result = classify_text_hierarchically(user_input)
        formatted_result = format_classification_result(result)
        # Append the new classification attempt to the log
        classification_log.append({'text': user_input, 'result': formatted_result})
    return render_template('index.html', classification_log=classification_log)

if __name__ == '__main__':
    app.run(debug=True)
