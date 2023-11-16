import random as rd
import time 
import numpy as np

#Creating each component
class Component():
    
    def __init__(self,name) -> None:
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
        print(f"There are {self.attribute} atributes linked to {self.name}")
        return [attr.name for attr in self.attribute]


#Create each ATTRIBUTE linkin it with a COMPONENT
class Propriety():
        
    def __init__(self,name,component,risk) -> None:
        self.name= name
        self.component=component
        self.risk=risk
        self.state= True 
        self.component.addAttribute(self)
        self.link=[]
        print(f"Attribute created named {self.name} part of {self.component.name}")   
   

    def getComponent(self):
        print(f'{self.name} is part of {self.component}')    
              
    def addFailedTick(self,tick):
        self.FailedTick= tick
        
    def addLinkToAttribute(self, attr2, risk,time_to_infect,status):
        self.link.append([self, attr2,time_to_infect, risk,status])  

    def getLinks(self):
        for link in self.link:
            print(f"There is a link between {link[0].name} (FROM: {link[0].component.name}) and {link[1].name} (FROM: {link[1].component.name}) with risk {link[3]}") 
        return self.link
        
    def getInfected(self,t):
        self.state=False
        self.addFailedTick(tick=t)           
        
#NOTE: CREATING EACH LINK FOR EACH ATTRIBUTE      
class Link():
    
    def __init__(self,time,risk,attribute1, attribute2) -> None:  
        self.risk= risk
        self.time_to_infect=time
        self.stat= True
        self.status= True   
        
        self.attribute1= attribute1
        self.attribute2=attribute2
        attribute1.addLinkToAttribute(attr2=self.attribute2,risk=self.risk,time_to_infect= self.time_to_infect,status=self.stat)
        attribute2.addLinkToAttribute(attr2=self.attribute1, risk=self.risk,time_to_infect= self.time_to_infect,status=self.stat) 
                 
        print(f"{self.__class__.__name__} created between {attribute1.name} and {attribute2.name}")

    def infect(self):
        if self.attribute1.state== False:
            self.attribute2.state== False
            print(f"{self.attribute1.name} infected {self.attribute2.name}")
            
        if self.attribute2.state==False:
            self.attribute1.state== False
            print(f"{self.attribute2.name} infected {self.attribute1.name}")
            
#Perhaps adding as a metaAttribute might work!             
class Behaviour():
    
    def __init__(self,name) -> None:
        self.name=name
        print(f"{self.__class__.__name__} created named {self.name}")
