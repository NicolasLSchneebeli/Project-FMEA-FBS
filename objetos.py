import random as rd
import time 
import numpy as np

def State_machine(components, tick):
    while True:
        for component in components:
            for propriety in component.attribute: 
                risk= propriety.risk
                states = ["Working", "Failed"]
                weights = [100-risk,risk]
                result= rd.choices(states,weights,k=1)[0]
                             
                if result == "Failed" and propriety.state_change ==False:
                    propriety.state=propriety.changeState()
                    propriety.state_change= True
                    print(f"{propriety.name} from {propriety.component.name} just failed! TICK: {tick}")
                    
                    propriety.risk=100
                    propriety.addFailedTick(tick)
                    
                    
                elif propriety.state_change == True:
                    print(f"{propriety.name} from {propriety.component.name} failed! TICK: {tick}")
                    vector_link = np.asarray(propriety.getLinks())
                    if vector_link.size > 0:
                        for i in range(len(vector_link)):
                            if propriety.FailedTick + tick == vector_link[i][3]:
                                risk= vector_link[i][1]
                                states = ["Working", "Failed"]
                                weights = [100-risk,risk]
                                resultinf= rd.choices(states,weights,k=1)[0]

                                if resultinf == "Failed":
                                    vector_link[i][2].state= False
                                    vector_link[i][2].change_State= True
                                    vector_link[i][2].risk=100
                                    print(f"{vector_link[i][2].name} was infected")
                                else:
                                    pass
                            else:
                                pass
                            
                    else:
                        pass
                else:
                    print(f'{propriety.name} from {propriety.component.name} still working in tick {tick}!!')
                    
        tick +=1
    

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

class Propriety():
        
    def __init__(self,name,component,risk) -> None:
        self.name= name
        self.component=component
        self.risk=risk
        self.state= True 
        self.state_change= False
        self.component.addAttribute(self)
        self.link=[]
        print(f"Attribute created named {self.name} part of {self.component.name}")   
   
    def changeState(self):
        return not self.state

    def getComponent(self):
        print(f'{self.name} is part of {self.component}')    
              
    def addFailedTick(self,tick):
        self.FailedTick= tick
        
    def addLinkToAttribute(self, attr2, risk,time_to_infect):
        self.link.append([self, risk, attr2,time_to_infect])  

    def getLinks(self):
        for link in self.link:
            # print(f"There is a link between {link[0].name} and {link[2].name} with risk {link[1]}")
            return self.link
                        
class Link():
    
    def __init__(self,time,risk,attribute1, attribute2) -> None:  
        self.risk= risk
        self.time_to_infect=time
        self.attribute1= attribute1
        self.attribute2=attribute2
        attribute1.addLinkToAttribute(attr2=self.attribute2,risk=self.risk,time_to_infect= self.time_to_infect)
        attribute2.addLinkToAttribute(attr2=self.attribute1, risk=self.risk,time_to_infect= self.time_to_infect)    
        print(f"{self.__class__.__name__} created between {attribute1.name} and {attribute2.name}")

    def infect(self):
        if self.attribute1.state== False:
            self.attribute2.state== False
            print(f"{self.attribute1.name} infected {self.attribute2.name}")
            
        if self.attribute2.state==False:
            self.attribute1.state== False
            print(f"{self.attribute2.name} infected {self.attribute1.name}")
            
            
class Behaviour():
    
    def __init__(self,name) -> None:
        self.name=name
        print(f"{self.__class__.__name__} created named {self.name}")
