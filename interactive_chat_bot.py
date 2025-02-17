import os
import json
import pandas as pd
from api import *

def load_all_data(data_dir="data/"):
    """
    Loads all CSV files (articles, availability) as pandas DataFrames.
    Returns a dictionary containing the data.
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
    Retrieves a specific value from a dataset column for a given ID.

    Parameters:
        data (dict): Dictionary containing the DataFrames.
        dataset (str): Dataset name.
        component_id (int): Target component ID.
        column (str): Target column.

    Returns:
        The value in the specified column for the given ID.
    """
    return data[dataset].loc[data[dataset]["id"] == component_id, column].values[0]

def display_menu():
    """
    Displays an interactive menu for the user with clear descriptions.
    """
    print("\n-------------------------------------------")
    print("🤖 Hello, I am your intelligent AI assistant. Here is what I can do for you:")
    print("1. 📦 Submit a repair request")
    print("2. 💰 Submit a refund request")
    print("3. 🔍 Request information or advice")
    print("4. 📄 Request a document")
    print("5. 🚚 Track an order")
    print("6. ⚠️  Report a product issue")
    print("0. ❌ Exit")
    print("-------------------------------------------")

def user_choice():
    """
    Handles user choices and builds a scenario based on their responses.
    """
    data = load_all_data(data_dir="data/")
    scenario = []
    time_now = 20  # Example of current time

    while True:
        display_menu()
        try:
            number = int(input("👉 What would you like to do? Enter a number: "))
        except ValueError:
            print("⛔ Invalid input. Please enter a number.")
            continue

        if number == 0:
            print("👋 Thank you for using me. See you soon!")
            break

        match number:
            case 1:
                scenario.append("repair request")
                order_id = int(input("🔧 Enter your order ID: "))
                if not get_info(data, "articles", order_id, "repairable"):
                    scenario.append("non repairable product")
                if get_info(data, "articles", order_id, "under_warranty"):
                    scenario.append("product under warranty")
                return scenario

            case 2:
                scenario.append("refund request")
                order_id = int(input("💰 Enter your order ID: "))
                if get_info(data, "articles", order_id, "under_warranty"):
                    scenario.append("product under warranty")
                return scenario

            case 3:
                scenario.append("information request")
                info_choice = input("🔍 Do you want advice (A) or just information (I)? ").strip().upper()
                if info_choice == "A":
                    scenario.append("advice request on product")
                    if not int(get_info(data, "availability", 1, "horaire_start")) <= time_now <= int(get_info(data, "availability", 1, "horaire_end")):
                        scenario.append("human expert not available")
                return scenario

            case 4:
                scenario.append("document request")
                has_order_id = input("📄 Do you have an order ID? (Y/N): ").strip().upper()
                if has_order_id == "Y":
                    order_id = int(input("📄 Enter your order ID: "))
                    scenario.append("order id")
                return scenario

            case 5:
                scenario.append("tracking request")
                has_order_id = input("🚚 Do you have an order ID? (Y/N): ").strip().upper()
                if has_order_id == "Y":
                    order_id = int(input("🚚 Enter your order ID: "))
                    scenario.append("order id")
                return scenario

            case 6:
                scenario.append("report product issue")
                if not int(get_info(data, "availability", 1, "horaire_start")) <= time_now <= int(get_info(data, "availability", 1, "horaire_end")):
                    scenario.append("human expert not available")
                return scenario

            case _:
                print("⛔ Invalid choice. Please choose a valid number.")

def main():
    """
    Main function to run the interactive application.
    """
    scenario = user_choice()
    if scenario:
        print("\n✨ Here is your scenario:")
        print(json.dumps(scenario, indent=4, ensure_ascii=False))

        # Call the API with the scenario
        solutions = call_api(scenario)
        print("\n💡 Here are the proposed solutions:")
        print(json.dumps(solutions, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
