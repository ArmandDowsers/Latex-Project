import os
import json
from pylatex import Document, Command
from pylatex.utils import NoEscape

# json -> commandes LaTeX
latex_commands = {
    'language': r'\languageChange',
    'blockchain': r'\blockchain',
    'name': r'\name',
    'criticity': r'\criticity',
    'patern': r'\pattern',
    'conditionalPattern': r'\conditionalPattern',
    'description': r'\descriptionChange',
    'recommendation': r'\recommendation',
    'gasSaving': r'\gasSaving',
    'impact': r'\impact',
    'startLineModifier': r'\startLineModifierChange',
    'endLineModifier': r'\endLineModifierChange',
    'category': r'\category',
    'specificationEN': r'\specificationEN',
    'specificationMATH': r'\specificationMATH',
    'contractType': r'\contractType',
    'risk': r'\risk',
    'scenario': r'\scenario',
    'subScenario': r'\subScenario',
    'property': r'\property'
}

# clés spéciales
special_cases = {
    'specification_DID': 'specificationDID',
    'version': 'version'
}

def verifyKeys(key):
    """
    Cette fonction permet de vérifier les clés du JSON par rapport aux
    commandes LaTeX définies dans 'latex_commands' ou 'special_cases'.
    """
    if key in special_cases:
        return special_cases[key]  # 'specification_DID' -> 'specificationDID'
    elif key in latex_commands:
        # '\languageChange')
        return latex_commands[key].lstrip('\\')
    else:
        # clé classique
        return key

def load_json_data(json_file):
    """Charge les données du fichier JSON"""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("*****************************")
    print(data)
    print("*****************************")
    return data

def define_latex_commands(doc, data):
    """
    Ajoute les commandes LaTeX dans la préambule du document,
    en fonction des paires (clé, valeur) du JSON.
    """
    for key, value in data.items():
        # on converti la clé json -> commande latex
        latex_command_name = verifyKeys(key)

        # si la valeur est une liste on l'a convert to string
        if isinstance(value, list):
            value = ", ".join(value)

        if value is None:
            value = ""

        # \newcommand{\commande}{valeur}
        command = Command('newcommand', [NoEscape(f'\\{latex_command_name}'), value])
        print(command)
        doc.preamble.append(command)

def add_template_content(doc, template_file):
    """Ajoute le contenu du template LaTeX au document."""
    with open(template_file, 'r', encoding='utf-8') as file:
        template_content = file.read()
    doc.append(NoEscape(template_content))

def create_dynamic_report(json_file, template_file, output_filename):
    """
    Crée un rapport dynamique en injectant les données JSON
    dans un template LaTeX & ensuite génère le PDF.
    """
    # on charge les données JSON
    data = load_json_data(json_file)

    # on créer un document pylatex
    doc = Document(documentclass='article', lmodern=False)

    # 3) on défini les commandes LaTeX basées sur clé et valeur du JSON
    define_latex_commands(doc, data)

    # on ajoute le contenu du template LaTeX
    add_template_content(doc, template_file)

    # on génère le pdf dans le répertoire 
    doc.generate_pdf(output_filename, clean_tex=False)

if __name__ == '__main__':
    json_file = './Specifications/arbitraryJump.json'
    template_file = './Specifications/template.tex'
    output_filename = 'specification'

    create_dynamic_report(json_file, template_file, output_filename)
