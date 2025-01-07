import json
from pylatex import Document, Command
from pylatex.utils import NoEscape

def load_json_data(json_file):
    """Charge les données du fichier JSON"""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def define_latex_commands(doc, data):
    """Ca rajoute les commandes sur le fichier latex qui provienne du json (clé et valeur)"""
    for key, value in data.items():
        # \newcommand{\key}{value} c'est ce que ça va rendre dans le doc .tex
        command = Command('newcommand', [NoEscape(f'\\{key}'), value])
        doc.preamble.append(command)

def add_template_content(doc, template_file):
    """Ajoute le contenu du template LaTeX au document"""
    with open(template_file, 'r', encoding='utf-8') as file:
        template_content = file.read()
    doc.append(NoEscape(template_content))

def create_dynamic_report(json_file, template_file, output_filename):
    """Ca créer un rapport dynamique qui injecte les données JSON dans un template LaTeX"""
    # Charger les données JSON
    data = load_json_data(json_file)

    # Créer un document
    doc = Document(documentclass='article', lmodern=False)

    # Définir les commandes LaTeX basées sur le JSON On définit ls commandes LaTeX basées sur le json
    define_latex_commands(doc, data)

    # Ajout du contenu du template
    add_template_content(doc, template_file)

    # On génère le pdf
    doc.generate_pdf(output_filename, clean_tex=False)


if __name__ == '__main__':
    json_file = 'arbitraryJump.json'
    template_file = 'template.tex'
    output_filename = 'specification'

    create_dynamic_report(json_file, template_file, output_filename)
