
def userChoice():
    number=int(input("WHAT DO YOU WANT : "))
    scenario = []
    while(number!=0):
        match number:
            case 1 :
                scenario.append("repair request")
                bool=int(input("order Id ?")) 
                #verifier dans bdd si piece dispo
                #verifier dans bdd si article sous garantie
                return scenario 
            case 2 :
                scenario.append("information request")
                bool=input("Do you want advice or just information ? A or I") 
                #verifier dans bdd si article sous garantie
                if(bool=="A"):
                    scenario.append("advice request on product")
                    #verifier bdd si personne dispo a cette heure 
                    
                return scenario
            case 3 :
                scenario.append("document request")
                bool=int(input("Do you have a order Id ? N or Y"))
                if(bool=="Y"):
                    number=int(input("Give your order Id")) #verifier bdd si existe si oui alors
                    scenario.append("order id")
                return scenario
            case 4 :
                scenario.append("tracking request")
                bool=input("Do you have order id ? Y or N") 
                if(bool=="Y"):
                    number=int(input("Give your order Id")) 
                    #verifier bdd si existe si oui alors
                    scenario.append("order id")
                    return scenario
            case 5 :
                scenario.append("report product issue")
                #verifier bdd si personne dispo a cette heure
            case 6 :
                scenario.append("refund request")
                bool=int(input("order Id ?")) 
                #verifier dans bdd si article sous garantie
                
                                                                   
def callApi(scenario):
    action =""
    return action 

def respond(action):
    return 0
                       
              

   
            