import json
import requests
from private_information import *

# Définir les en-têtes pour l'API
headers = {
    "x-api-key": api_key
}

def extract_elements_and_options(metadata):
    """
    Extrait les labels et IDs des éléments, ainsi que les IDs des options.

    Paramètres :
        metadata (dict) : Données contenant les sections 'elements' et 'options'.

    Retourne :
        tuple : 
            - Un dictionnaire {label: id} pour les éléments.
            - Une liste de dictionnaires [{"id": id}] pour les options.
    """
    elems = {}  # Stocke les labels et IDs des éléments
    opts = []   # Stocke les IDs des options

    # Récupère les éléments et options
    elem_items = metadata.get('elements', [])
    opts_items = metadata.get('options', [])

    # Traite les éléments et ajoute leurs labels et IDs dans le dictionnaire
    for item in elem_items:
        label = item.get("label")
        id_value = item.get("id")
        elems[label] = id_value

    # Traite les options et ajoute leurs IDs dans une liste
    for item in opts_items:
        id_value = item.get("id")
        opts.append({"id": id_value})

    return elems, opts


def check_solutions(options):
    """
    Vérifie les solutions valides parmi les options fournies.

    Paramètres :
        options (list) : Liste des options contenant la clé 'isSolution'.

    Retourne :
        list : Une liste des noms des options valides ou False si aucune.
    """
    # Liste pour stocker les noms des options valides
    true_options = []

    # Parcourir chaque option
    for option in options:
        if option['isSolution']:  # Vérifie si 'isSolution' est True
            true_options.append(option['option']['label'])  # Ajoute le label de l'option

    # Retourne les options valides ou False si aucune
    return true_options if true_options else None

def get_data_api(url, api_key):
    """
    Récupère les données de l'API et extrait les labels et IDs.

    Paramètres :
        url (str) : L'URL de l'API.
        api_key (str) : La clé API pour l'authentification.

    Retourne :
        metadata : Les metadata retournées
    """
    headers = {
        "x-api-key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            metadata = response.json()
        elif response.status_code == 400:
            print("Erreur 400 : Requête invalide.")
        else:
            print(f"Erreur {response.status_code} : {response.text}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    return metadata

def call_api(scenario):
    """
    Appelle l'API pour évaluer les scénarios et retourne les options valides.

    Paramètres :
        scenario (list) : Liste des labels des éléments à inclure dans le scénario.

    Retourne :
        list : Les solutions valides ou None si aucune.
    """

    metadata = get_data_api(url, api_key)
    elements, options = extract_elements_and_options(metadata)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    ids = []

    # Préparer les IDs des éléments du scénario
    for case in scenario:
        temp_dict = dict()
        temp_dict["id"] = elements[case]
        ids.append(temp_dict)

    payload = {
        "elements": ids,
        "options": options,
        "limit": len(options)
    }

    try:
        # Envoyer la requête POST avec la charge utile JSON
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            metadata = response.json()
        elif response.status_code == 400:
            print("Erreur 400 : Requête invalide.")
        else:
            print(f"Erreur {response.status_code} : {response.text}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

    # Retourner les solutions valides
    return check_solutions(metadata)

