import requests


def generate_plantuml_diagram(plantuml_code):

    response = requests.post(
        'https://www.bibcit.com/api/mdiag/svg',
        json={
            'diagType': 'plantuml',
            'diagcode': plantuml_code
        }
    )

    return response.json()

def generate_mermaid_diagram(mermaid_code):

    mermaid_code = '''%%{init: {"htmlLabels": false}}%%
''' + mermaid_code
    response = requests.post(
        'https://www.bibcit.com/api/mdiag/svg',
        json={
            'diagType': 'mermaid',
            'diagcode': mermaid_code
        }
    )

    return response.json()