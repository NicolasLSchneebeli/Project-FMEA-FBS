import random as rd
import time 
from objetos import *


def State_machine2(components, tick):
    while True:
        for component in components:
            for propriety in component.attribute: 
                risk= propriety.risk
                states = ["Working", "Failed"]
                weights = [100-risk,risk]
                result= rd.choices(states,weights,k=1)[0]
                print(f"STATE: {propriety.name} is {result}")
                
                
                
                if result == "Failed":
                    propriety.state=False
                    print(f"{propriety.name} from {propriety.component.name} just failed! TICK: {tick}")
                    time.sleep(3)
                    propriety.risk=100
                    propriety.addFailedTick(tick)
                    
                    
                elif propriety.state_change == True:
                    print(f"{propriety.name} from {propriety.component.name} failed! TICK: {tick}")
                    teste = propriety.getLinks()
                    for i in teste:

                        if propriety.FailedTick + tick == propriety.getLinks()[i][3]:
                            risk= Link.risk
                            states = ["Working", "Failed"]
                            weights = [100-risk,risk]
                            resultinf= rd.choices(states,weights,k=1)[0]

                            if resultinf == "Failed":
                                Link.infect()
                    time.sleep(3)        
                else:
                    print(f'{propriety.name} from {propriety.component.name} still working in tick {tick}!!')
                    time.sleep(3)
        tick +=1
    
