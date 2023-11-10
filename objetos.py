import random as rd
import time 


def State_machine(propriety,tick):
    while True:
        risk= propriety.risk
        states = ["Working", "Failed"]
        weights = [100-risk,risk]
        result= rd.choices(states,weights,k=1)[0]
        print(f"STATE {result}")
        
        
        
        if result == "Failed" and propriety.state_change ==False:
            propriety.state=propriety.changeState()
            propriety.state_change= True
            
            
            print(f"{propriety.name} from {propriety.component.name} just failed! TICK: {tick}")
            time.sleep(1)
            propriety.risk=100
            tick +=1 
            
        elif propriety.state_change == True:
            print(f"{propriety.name} from {propriety.component.name} failed! TICK: {tick}")
            time.sleep(1)
            tick += 1
        else:
            print(f'{propriety.name} from {propriety.component.name} still working in tick {tick}!!')
            time.sleep(1)
            tick += 1
    
    

#Creating each component
class Component():
    
    def __init__(self,name) -> None:
        self.name= name
        self.atribute=[]
        print(f"{self.__class__.__name__} created named {self.name}")

    #Add atributes
    def addAtribute(self,atribute):
        #.NOTE to NEXT VERSION: add errors to help the user
        if any(attr.lower() == atribute.lower() for attr in self.atribute):
            print("Atribute already added!")
        else:
            self.atribute.append(atribute)
            # print(f"Atribute named {self.atribute[-1]} linked to {self.name}")
        
    #Give a list of all atributes given to the component
    def getAtribute(self):
        print(f"There are {self.atribute} atributes linked to {self.name}")
        return self.atribute
    

class Propriety():
        
    def __init__(self,name,component,risk) -> None:
        self.name= name
        self.component=component
        self.risk=risk
        self.state= True 
        self.state_change= False
        component.addAtribute(self.name)
        print(f"{self.__class__.__name__} created named {self.name} part of {self.component.name}")   
   
    def changeState(self):
        return not self.state

    def getComponent(self):
        print(f'{self.name} is part of {self.component}')          
    
    

class Behaviour():
    
    def __init__(self,name) -> None:
        self.name=name
        print(f"{self.__class__.__name__} created named {self.name}")



class Link():
    
    def __init__(self,type,value,attribute1, attribute2) -> None:
        
        
        
        print(f"{self.__class__.__name__} created named {self.name} with type ")

