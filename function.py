import pandas as pd
import datetime as dt
import numpy as np
import random as rd
import time
import os 
import glob 
from objetos import *
 

#Funciton to run the simulation 
def State_machine(components: list[Component], behaviour: list[Behaviour],link_matrix: np.array ,attrs: list[Propriety],number_of_interaction: int=1 ):
    k=0
    status,erro= check(component=components)
    if status == True:
        while k<number_of_interaction:
            print(f'==============================ITERACTION {k} =========================')
            tick=0
            matrix=np.copy(link_matrix)
            for beh in behaviour:
                beh.state= True
            for component in components:
                        for propriety in component.attribute: 
                            propriety.state=True
                        
            df= pd.DataFrame(columns= ['Tick','Attribute.Component','Origin'])
        
        
            stt=time.time()
            while all(behavior.state==True for behavior in behaviour):
                print(f'============================CURRENTLY ON TICK {tick}===============================')
                print(f'----------------------------Proprieties-------------------------------')
                for component in components:
                    for propriety in component.attribute: 
                        #IF ATTRIBUTE HAS NOT FAILED YET CONTINUE WITHIN THE LOOP
                        if propriety.state == True:
                            risk= propriety.risk
                            states = ["Working", "Failed"]
                            weights = [100-risk,risk]
                            result= rd.choices(states,weights,k=1)[0]
                                        
                            if result == "Failed":
                                print(f"{propriety.name} from {propriety.component.name} *just* failed on tick: {tick}")
                                failures=list(propriety.FailureMode.keys())
                                chances=[propriety.FailureMode[i] for i in failures]
                                # if chances == []:
                                propriety.addFailedTick(tick=tick,data=df,origin=propriety)
                                # else:
                                #     result=rd.choices(failures,chances,k=1)[0]
                                #     propriety.addFailedTick(tick=tick,data=df,origin=f'self ({result})')

                                
                            else:
                                print(f"{propriety.name} from {propriety.component.name} is {result}")

                                
                            """When the state of the attribute is false,
                            meaning that it has failed."""      
                        else:
                            '''Check if it is time yet for him to failed! (Right now just time, cause of implementation, 
                                perhaps it is a good alternative since is easy to determine unlike temperature for exemple, 
                                which I imagine taking a lot of the memory of the PC. )'''
                            print(f"{propriety.name} from {propriety.component.name} failed on tick {propriety.FailedTick}, which is {tick-propriety.FailedTick} ticks ago")
                            
                            """Getting the links of the each attribute."""
                            i = attrs.index(propriety)
                            for j in range(matrix.shape[1]):
                                '''Relating the columns and getting the links active for this attribute'''
                                if sum(matrix[i,j]) > 0:
                                    if tick -propriety.FailedTick >= matrix[i, j, 1]:
                                        risk= matrix[i, j, 0]
                                        states_ = ["Working", "Failed"]
                                        weights = [100-risk,risk]
                                        resultinf= rd.choices(states_,weights,k=1)[0]
                                        if resultinf == "Failed":
                                            attrs[j].addFailedTick(tick=tick,data=df,origin=propriety)
                                            matrix[i,j]=[0,0]
                                            matrix[j,i]=[0,0]
                                            print(f"{attrs[j].name} from {attrs[j].component.name} was infected by {propriety.name}")
                                    else:
                                        pass
                                else:
                                    pass
                                
                print(f'----------------------------Behaviour-------------------------------')
                for beh in behaviour:
                    beh.checkCondition()
                tick +=1
            else:
                principal= f'Simulations/Simulation_{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}'
                sec_=principal+'\Analysis'
                sec__=principal+'\CauseOfFailure'
                os.makedirs(principal, exist_ok=True)
                os.makedirs(f'{sec_}',exist_ok=True)
                os.makedirs(f'{sec__}',exist_ok=True)
                toSave(df=df,behaviour=behaviour,start_time=stt,tick=tick,k=k,path=principal)
                k+=1
        else:
            print('Number of iteractions achieved!')
    
    else:
        print(erro)
        
    
#NOTE: Remove the error for append method is a good way to improve the quality of the display and the results
        
def readFile(excel_file: str):     
    df= pd.read_excel(excel_file,header=0)
    components_unique= df['Component'].unique()
    
    list_comp = [Component(name=component_name) for component_name in components_unique]
    
    relacoes={}
    for index, line in df.iterrows():
        component = line['Component']
        attribute = line['Attribute']
        prob_failure = line['Prob_of_Failure']
    
        if component not in relacoes:
            relacoes[component] = {}
        relacoes[component][attribute] = prob_failure
            
    attributos_= []
    for comp in list_comp:
        for attr in relacoes[comp.name]:
            attributos_.append(Propriety(component=comp, name=attr, risk=relacoes[comp.name][attr]))
    return list_comp,attributos_
    

#Checking for name erros, attributes without links and component list empty! 
def check(component: list[Component]):
    component_name= set()
    if component== []:
        erro=('Component list is empty!')
        return False, erro
    for comp in component:
        if comp.name.lower() in component_name:
            erro= ('Two or more components with the same name! \n Try adding numbers. F.e. Component1 and Component2 instead of Component and Component')
            return False,erro
        component_name.add(comp.name.lower())
        if comp.attribute == []:
                erro=('There is a component(s) without attribute. Please add an attribute')
                return False,erro
    else:
        erro= None
        return True,erro
    
    
def toSave(df: pd.DataFrame,behaviour: list[Behaviour],start_time,tick,k,path):

    Beh_Failure = [beh for beh in behaviour if not beh.state]
    df.to_csv(f'{path}/Analysis/DF_{k}{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.csv',index=False)

    for beh in Beh_Failure:
        mensagem_erro = f'`{beh.name} failed cause conditions where achivied: {[i.name for i in beh.condition]} FAILED'
        df = df.append({'Failed Behaviour': mensagem_erro}, ignore_index=True)
    df.to_csv(f'{path}\CauseOfFailure\Simulation{k}__{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.csv',index=False)
    print('===================================DONE================================================')
    print(f'CSV saved in: Simulation/Simulation{k}__{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.csv')
    print(f'Time to complete {time.time()- start_time} seconds')
    print(f'Time to complete each tick {(time.time()- start_time)/tick} seconds')



''''RIGHT NOW I HAVE TO DO IT MANUALLY'''
def createMatrix(attributes_list: list[Propriety]):
    attrs= attributes_list
    return np.zeros((len(attrs),len(attrs),2),dtype=int)

def createLink(matrix,attribute_list: list[Propriety],attribute1: Propriety,attribute2: Propriety,risk,time: float):
    """Finding the index related to the attributes"""   
    i = attribute_list.index(attribute1)
    j = attribute_list.index(attribute2)
    
    '''Adding/Updating the matrix for the values for the link with RISK, TIME'''
    matrix[i, j] = [risk,time] 
    matrix[j, i] = [risk,time]
    
# def nameMatrix(attrs,):
    



'''
YET TO BE IMPLEMENTED PROPERLY
'''  
def analysis(path):
    path=os.path.join(path)
    csv_files = glob.glob(os.path.join(path, "*.csv")) 
    dfs=[]
    for f in csv_files:
        df_ = pd.read_csv(f)
        dfs.append(df_)
    df = pd.concat(dfs, ignore_index=True)
    
    return df


'''Function to list unique values and count their frequency'''
def count_and_list(series):
    unique_values = list(set(series))
    count_dict = {value: series[series == value].count() for value in unique_values}
    return unique_values, count_dict

'''Groupby Attribute.Component given a mean tick to fail and the unique listing to Origin '''
def Count_FailureModes(df):
    result = df.groupby('Attribute.Component').agg({
    'Tick': 'mean',
    'Origin': count_and_list
    }).reset_index()
    '''Creating new columns to add Unique Origin and their counts'''
    for value in result['Origin'].iloc[0][0]:
        result[value + '_Count'] = result['Origin'].apply(lambda x: x[1].get(value, 0))
    result = result.drop(columns=['Origin'])
    result.columns = ['Attribute.Component', 'Mean Tick to Fail'] + [f'{value}' for value in result.columns[2:]]
    return result