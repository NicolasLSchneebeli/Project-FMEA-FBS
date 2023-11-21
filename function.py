
import random as rd
import time 
import numpy as np


#Funciton to run the simulation 
def State_machine(components, tick, behaviour):
    status,erro= check(component=components)
    if status == True:
        while behaviour.state==True:
            print(f'----------------------------TICK {tick}-------------------------------')
            for component in components:
                for propriety in component.attribute: 
                    #IF ATTRIBUTE HAS NOT FAILED YET CONTINUE WITHIN THE LOOP
                    if propriety.state == True:
                        risk= propriety.risk
                        states = ["Working", "Failed"]
                        weights = [100-risk,risk]
                        result= rd.choices(states,weights,k=1)[0]
                                    
                        if result == "Failed":
                            propriety.state=False
                            print(f"{propriety.name} from {propriety.component.name} *just* failed on tick: {tick}")
                            propriety.addFailedTick(tick)
                            
                        else:
                            print(f"{propriety.name} from {propriety.component.name} is {result}")

                            
                    #When the state of the attribute is false, meaning that it has failed.      
                    else:
                        print(f"{propriety.name} from {propriety.component.name} failed on tick {propriety.FailedTick}, which is {tick-propriety.FailedTick} ticks ago")
                        #Getting the links of the each attribute.
                        links_of_propriety = np.asarray(propriety.link)
                        for i in range(len(links_of_propriety)):
                            if links_of_propriety[i][4]==False:
                                pass
                            
                            '''Check if it is time yet for him to failed! (Right now just time, cause of implementation, 
                            perhaps it is a good alternative since is easy to determine unlike temperature for exemple, 
                            which I imagine taking a lot of the memory of the PC. )'''
                            
                            if tick - propriety.FailedTick  == links_of_propriety[i][2] and links_of_propriety[i][4]== False:
                                risk= links_of_propriety[i][3]
                                links_of_propriety[i][4]== False
                                weights = [100-risk,risk]
                                resultinf= rd.choices(states,weights,k=1)[0]
                                if resultinf == "Failed":
                                    links_of_propriety[i][1].getInfected(t=tick)
                                    print(f"{links_of_propriety[i][1].name} from {links_of_propriety[i][1].component.name} was infected by {propriety.name}")
                            else:
                                continue   
            behaviour.checkCondition()
            tick +=1
            time.sleep(3)
    else:
        print(erro)
#NOTE: Think about what to return here!!
#Perhaps a list of which component infected what, idk 
        
        
        
#Checking for name erros, attributes without links and component list empty! 
def check(component):
    component_name= set()
    if component== []:
        erro=('Component list is empty!')
        return False, erro
    for comp in component:
        if comp.name.lower() in component_name:
            erro= ('Two or more components with the same name! \n Try adding numbers. F.e. Motor1 and Motor2 or more specific names ')
            return False,erro
        component_name.add(comp.name.lower())
        
        if comp.attribute == []:
                erro=('There is a component(s) without attribute!')
                return False,erro
        # if comp.attribute.link == []:
        #         erro=('There is a attribute without link!')
        #         return False,erro
    else:
        erro= None
        return True,erro