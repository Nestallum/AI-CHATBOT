import os
import pandas as pd
from api import *

def load_all_data(data_dir="data/"):
    """
    Charge tous les fichiers CSV (articles, disponibilité) en tant que DataFrames pandas.
    Retourne un dictionnaire contenant les données.
    """
    files = {
        "articles": "articles.csv",
        "availability": "availability.csv",
    }
    data = {}
    for key, file_name in files.items():
        file_path = os.path.join(data_dir, file_name)
        data[key] = pd.read_csv(file_path)

    return data

def get_info(data, dataset, component_id, column):
    """
    Récupère une valeur spécifique d'une colonne d'un dataset pour un ID donné.

    Paramètres :
        data (dict) : Dictionnaire contenant les DataFrames.
        dataset (str) : Nom du dataset
        component_id (int) : ID du composant cible.
        column (str) : Colonne cible.

    Retourne :
        La valeur dans la colonne spécifiée pour l'ID donné.
    """
    return data[dataset].loc[data[dataset]["id"] == component_id, column].values[0]

def display_menu():
    """
    Affiche un menu interactif pour l'utilisateur avec des descriptions claires.
    """
    print("\n-------------------------------------------")
    print("🤖 Bonjour, je suis votre assistant AI intelligent. Voici ce que je peux faire pour vous :")
    print("1. 📦 Faire une demande de réparation")
    print("2. 💰 Faire une demande de remboursement")
    print("3. 🔍 Demander des informations ou des conseils")
    print("4. 📄 Demander un document")
    print("5. 🚚 Suivre une commande")
    print("6. ⚠️  Signaler un problème produit")
    print("0. ❌ Quitter")
    print("-------------------------------------------")

def user_choice():
    """
    Gère les choix de l'utilisateur et construit un scénario basé sur ses réponses.
    """
    data = load_all_data(data_dir="data/")
    scenario = []
    time_now = 12  # Exemple d'heure actuelle

    while True:
        display_menu()
        try:
            number = int(input("👉 Que souhaitez-vous faire ? Entrez un numéro : "))
        except ValueError:
            print("⛔ Entrée invalide. Veuillez entrer un numéro.")
            continue

        if number == 0:
            print("👋 Merci de m'avoir utilisé. À bientôt !")
            break

        match number:
            case 1:
                scenario.append("repair request")
                order_id = int(input("🔧 Entrez votre numéro de commande : "))
                if not get_info(data, "articles", order_id, "repairable"):
                    scenario.append("non repairable product")
                if get_info(data, "articles", order_id, "under_warranty"):
                    scenario.append("product under warranty")
                return scenario

            case 2:
                scenario.append("refund request")
                order_id = int(input("💰 Entrez votre numéro de commande : "))
                if get_info(data, "articles", order_id, "under_warranty"):
                    scenario.append("product under warranty")
                return scenario

            case 3:
                scenario.append("information request")
                info_choice = input("🔍 Voulez-vous des conseils (A) ou juste des informations (I) ? ").strip().upper()
                if info_choice == "A":
                    scenario.append("advice request on product")
                    if not int(get_info(data, "availability", 1, "horaire_start")) <= time_now <= int(get_info(data, "availability", 1, "horaire_end")):
                        scenario.append("human expert not available")
                return scenario

            case 4:
                scenario.append("document request")
                has_order_id = input("📄 Avez-vous un numéro de commande ? (Y/N) : ").strip().upper()
                if has_order_id == "Y":
                    order_id = int(input("📄 Entrez votre numéro de commande : "))
                    scenario.append("order id")
                return scenario

            case 5:
                scenario.append("tracking request")
                has_order_id = input("🚚 Avez-vous un numéro de commande ? (Y/N) : ").strip().upper()
                if has_order_id == "Y":
                    order_id = int(input("🚚 Entrez votre numéro de commande : "))
                    scenario.append("order id")
                return scenario

            case 6:
                scenario.append("report product issue")
                if not int(get_info(data, "availability", 1, "horaire_start")) <= time_now <= int(get_info(data, "availability", 1, "horaire_end")):
                    scenario.append("human expert not available")
                return scenario

            case _:
                print("⛔ Choix invalide. Veuillez choisir un numéro valide.")


def main():
    """
    Fonction principale pour exécuter l'application interactive.
    """
    scenario = user_choice()
    if scenario:
        print("\n✨ Voici votre scénario :")
        print(json.dumps(scenario, indent=4, ensure_ascii=False))

        # Appeler l'API avec le scénario
        solutions = call_api(scenario)
        print("\n💡 Voici les solutions proposées :")
        print(json.dumps(solutions, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()