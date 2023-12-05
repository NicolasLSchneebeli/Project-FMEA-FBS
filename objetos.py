import random as rd
import numpy as np

#Creating each component
class Component():
    
    def __init__(self,name: str) -> None:
        self.name= name
        self.attribute=[]
        print(f"{self.__class__.__name__} created named {self.name}")

    #Add atributes
    def addAttribute(self,attribute):
        #.NOTE to NEXT VERSION: add errors to help the user
        if any(attr.name.lower() == attribute.name.lower() for attr in self.attribute):
            print("Atribute already added!")
        else:
            self.attribute.append(attribute)
            print(f"Atribute named {self.attribute[-1].name} linked to {self.name}")
        
    #Give a list of all atributes given to the component
    def getAttribute(self):
        print(f"There are {self.attribute.name} atributes linked to {self.name}")
        return [attr.name for attr in self.attribute]


#Create each ATTRIBUTE linkin it with a COMPONENT
class Propriety():
    #Constructor
    def __init__(self,name: str,component: Component,risk: float) -> None:
        self.name= name
        self.component=component
        self.risk=risk
        self.state= True 
        self.source=[]
        self.component.addAttribute(self)
        self.FailureMode={}
   
    #Just to confirm if is ok
    def getComponent(self):
        print(f'{self.name} is part of {self.component}')    
      
    #Add time when this component failed!      
    def addFailedTick(self,tick,data,origin):
        self.FailedTick= tick
        self.state=False
        self.source=origin
        
        if origin.name.lower() == self.name.lower() and origin.component.name == self.component.name:
            data.loc[len(data)]=(self.FailedTick,f'{self.name}.{self.component.name}',f'{self.name}.{self.component.name}')
        else:
            data.loc[len(data)]=(self.FailedTick,f'{self.name}.{self.component.name}',f"{origin.name}.{origin.component.name}")
            
        
    '''For FMEA Table. Perhaps adding a dictionary
    like linking to EXCESS or LOSS, idk yet.
    '''     
    def addFailureMode(self,Names: list[str] ,Risks):
        if sum(Risks)!=100:
            print("Failure mode sum of probabilities diferent that 100%")
        for i in range(len(Names)):
            self.FailureMode[Names[i]]= Risks[i]

class Behaviour():
    
    def __init__(self,name: str) -> None:
        self.name=name
        self.condition= []
        self.c_state= True
        self.state= True  
        print(f"{self.__class__.__name__} created named {self.name}")

    def checkCondition(self):
        c_state=[comp.state for comp in self.condition]
        if c_state==[]:
            c_state=[True]
        if all(state == False for state in c_state):
            self.state= False
            print(f'{self.name} has failed!')
        else: 
            self.state= True    
            print(f"{self.name} working")
            
    def addCondition(self, conditions):
        self.condition.append(conditions)
        print(f"Created a condtion that {conditions.name} has to work for  {self.name} to continue working")


        
