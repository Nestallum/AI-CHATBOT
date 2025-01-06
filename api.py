
import json
import requests
from private_information import *

headers = {
    "x-api-key": api_key
}

def extract_labels_and_ids(data):
    """
    Extracts a dictionary where the keys are labels and the values are their corresponding IDs.

    Parameters:
        data (dict): The input dictionary containing 'elements' and 'options' lists.

    Returns:
        dict: A dictionary with labels as keys and IDs as values.
    """
    result = {}

    # Combine elements and options into one list to process them together
    items = data.get('elements', []) + data.get('options', [])

    # Loop through the items and populate the result dictionary
    for item in items:
        label = item.get('label')
        id_value = item.get('id')
        if label and id_value:  # Ensure both label and id exist
            result[label] = id_value

    return result

def check_solutions(options):
    # Liste pour stocker les noms des options vraies
    true_options = []
    
    # Boucle à travers chaque option
    for option in options:
        if option['isSolution']:  # Vérifie si 'isSolution' est True
            true_options.append(option['option']['label'])  # Ajoute le nom de l'option vraie
            
    # Si des options vraies sont trouvées, retourne leurs noms
    if true_options:
        return true_options
    else:
        return False

def getDataApi(url,api_key):
    
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
        
    return extract_labels_and_ids(metadata)


def callApi(scenario):
      # Remplacez par votre clé API
    ids_scenario = getDataApi(url,api_key)
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    ids = []
    
    for case in scenario :
        temps_dict = dict()
        temps_dict["id"]=ids_scenario[case]
        ids.append(temps_dict)
    print(ids)
    payload = {
        "elements": ids,
        "options": options,
        "limit": len(options)
    }
    
    try:
        # Utilisation correcte du mot-clé `json` pour envoyer la charge utile JSON
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            metadata = response.json()
            
            
              # Retourne les données si succès
        elif response.status_code == 400:
            print("Erreur 400 : Requête invalide.")
        else:
            print(f"Erreur {response.status_code} : {response.text}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    # Initialiser `metadata` par défaut en cas d'erreur
    print(check_solutions(metadata))
    return check_solutions(metadata)


ids = getDataApi(url,api_key)


    
    
    
    

