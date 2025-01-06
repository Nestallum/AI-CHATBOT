import os
import pandas as pd 
from api import *

def load_all_data(data_dir="data/"):
    """
    Loads all CSV files (CPUs, motherboards, RAM) as pandas DataFrames.
    Returns a dictionary with the data.
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


def getInfo(data,key,id,info):
    return data[key].loc[data[key]["id"]==id,info].values[0]

data = load_all_data(data_dir="data/")


def userChoice():
    time_now = 12
    data = load_all_data(data_dir="data/")
    number=int(input("WHAT DO YOU WANT : "))
    scenario = []
    while(number!=0):
        match number:
            case 1 :
                scenario.append("repair request")
                bool=int(input("order Id ?")) 
                if not(getInfo(data,"articles",bool,"repairable")) :
                    scenario.append("non repairable product")
                if getInfo(data,"articles",bool,"under_warranty") :
                    scenario.append("product under warranty") 
                
                return scenario 
            case 2 :
                scenario.append("information request")
                bool=input("Do you want advice or just information ? A or I") 
                if(bool=="A"):
                    scenario.append("advice request on product")
                    if not int(getInfo(data,"availability",1,"horaire_start")) <= time_now <= int(getInfo(data,"availability",1,"horaire_end")):
                        scenario.append("human expert not available")         
                return scenario
            case 3 :
                scenario.append("document request")
                bool=input("Do you have a order Id ? N or Y")
                if(bool=="Y"):
                    number=int(input("Give your order Id")) 
                    #checkez si id existe
                    scenario.append("order id")
                return scenario
            case 4 :
                scenario.append("tracking request")
                bool=input("Do you have order id ? Y or N") 
                if(bool=="Y"):
                    number=int(input("Give your order Id")) 
                    #checkez si id existe
                    scenario.append("order id")
                
                return scenario
            case 5 :
                scenario.append("report product issue")
                if not int(getInfo(data,"availability",1,"horaire_start")) <= time_now <= int(getInfo(data,"availability",1,"horaire_end")):
                        scenario.append("human expert not available")
                return scenario
                
            case 6 :
                scenario.append("refund request")
                bool=int(input("order Id ?")) 
                if getInfo(data,"articles",bool,"under_warranty") :
                    scenario.append("product under warranty") 
                return scenario

scenario = userChoice() 
print()
print(scenario)        
callApi(scenario)  
                                                                   
        
              

   
            