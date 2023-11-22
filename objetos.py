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
        print(f"There are {self.attribute.name} atributes linked to {self.name}")
        return [attr.name for attr in self.attribute]


#Create each ATTRIBUTE linkin it with a COMPONENT
class Propriety():
    #Constructor
    def __init__(self,name,component,risk) -> None:
        self.name= name
        self.component=component
        self.risk=risk
        self.state= True 
        self.component.addAttribute(self)
        self.link=[]
        # print(f"Attribute created named {self.name} part of {self.component.name}")   
   
    #Just to confirm if is ok
    def getComponent(self):
        print(f'{self.name} is part of {self.component}')    
      
    #Add time when this component failed!      
    def addFailedTick(self,tick,data,origin):
        self.FailedTick= tick
        data.loc[len(data)]=(self.FailedTick,self.name,self.component.name,origin)

    
    #Create via ENTITIY NAMED LINK!!
    def addLinkToAttribute(self, attr2, risk,time_to_infect,status):
        self.link.append([self, attr2,time_to_infect, risk,status])  
    
    #LIST OF LINKS COMPOSED OF ATT1, ATT2, RISK, COOLDOWN TIME, STATUS
    def getLinks(self):
        for link in self.link:
            print(f"There is a link between {link[0].name} (FROM: {link[0].component.name}) and {link[1].name} (FROM: {link[1].component.name}) with risk {link[3]}") 
        return self.link
    
    #Change our entity state to FAILEd
    def getInfected(self,t,origin,df):
        self.state=False
        self.addFailedTick(tick=t,data=df,origin=origin)           
        
#NOTE: CREATING EACH LINK FOR EACH ATTRIBUTE
'''How to create other kinds of links such as Temperatures/Distance etc. Don't see how this would impact the simul in general...?'''      
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
            
#Perhaps adding as a Bigger Attribute/Component might work! 
''' How to implement their links?'''             
class Behaviour():
    
    def __init__(self,name) -> None:
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


        
