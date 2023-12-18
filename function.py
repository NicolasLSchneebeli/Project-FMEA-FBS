import pandas as pd
import datetime as dt
import numpy as np
import random as rd
import time
import os 
import glob 
from objetos import *
import seaborn as sns
import matplotlib.pyplot as plt



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
                                propriety.addFailedTick(tick=tick,data=df,origin=propriety)
                               
                                
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
                                        if resultinf == "Failed" and attrs[j].state ==True:
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
                principal= f'PROJETO_FRANÇA/Simulations/Simulation_{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}'
                sec_=principal+'\Analysis'
                sec__=principal+'\CauseOfFailure'
                os.makedirs(principal, exist_ok=True)
                os.makedirs(f'{sec_}',exist_ok=True)
                os.makedirs(f'{sec__}',exist_ok=True)
                toSave(df=df,behaviour=behaviour,start_time=stt,tick=tick,k=k,path=principal)
                k+=1
        else:
            print('Number of iteractions achieved!')
            return f'{principal}/Analysis/'
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
    print('======= SAVING ========')
    Beh_Failure = [beh for beh in behaviour if not beh.state]
    df.to_csv(f'{path}/Analysis/DF_{k}{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.csv',index=False)

    for beh in Beh_Failure:
        mensagem_erro = f'`{beh.name} failed cause conditions where achivied: {[i.name for i in beh.condition]} FAILED'
        df = df.append({'Failed Behaviour': mensagem_erro}, ignore_index=True)
    df.to_csv(f'{path}\CauseOfFailure\Simulation{k}__{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.csv',index=False)
    print('===================================DONE================================================')
    print(f'CSV saved in: Simulations/Simulation{k}__{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.csv')
    print(f'Time to complete {time.time()- start_time} seconds')
    print(f'Time to complete each tick {(time.time()- start_time)/tick} seconds')
    

    
    
def createMatrix(attributes_list: list[Propriety], random: bool = False, save_excel: bool = False):
    attrs= attributes_list
    matrix= np.zeros((len(attrs),len(attrs),2),dtype=int)
    if random==True:
        createLinksRandom(matrix=matrix,attributes_list=attrs)
        return matrix
    if save_excel == True:
        matrix = np.zeros((len(attrs), len(attrs)), dtype=int)
        df=pd.DataFrame(matrix, columns=[f'{i.name}.{i.component.name}' for i in attrs], index=[f'{i.name}.{i.component.name}' for i in attrs])
        df_time=df.copy()
        df_risk=df.copy()
        file_name=f'Projeto_FRANÇA/Links_{dt.datetime.now().day}_{dt.datetime.now().month}_{dt.datetime.now().year}_{dt.datetime.now().hour}_{dt.datetime.now().minute}.xlsx'
        with pd.ExcelWriter(f'{file_name}', engine='xlsxwriter') as writer:
            df_risk.to_excel(writer, sheet_name='Risk')
            df_time.to_excel(writer, sheet_name='Time')
        return  file_name ,print(f'Save as {file_name}')

    else:
        return matrix


    
def readMatrix(path: str):
    df_time=pd.read_excel(path,sheet_name='Time')
    df_risk=pd.read_excel(path,sheet_name='Risk')
    df_risk=df_risk.drop(columns='Unnamed: 0')
    df_time=df_time.drop(columns='Unnamed: 0')                
    array_time = df_time.to_numpy()
    array_risk = df_risk.to_numpy()
    array_combined = np.concatenate([array_risk[:, :, np.newaxis], array_time[:, :, np.newaxis]], axis=2)
    return array_combined
    

def createLink(matrix,attribute_list: list[Propriety],attribute1: Propriety,attribute2: Propriety,risk,time: float):
    """Finding the index related to the attributes"""   
    i = attribute_list.index(attribute1)
    j = attribute_list.index(attribute2)
    
    '''Adding/Updating the matrix for the values for the link with RISK, TIME'''
    matrix[i, j] = [risk,time] 
    matrix[j, i] = [risk,time]

'''Create links randomly'''
def createLinksRandom(matrix, attributes_list, numb_of_links:int=5, time_max:int=5, risk_max:int=100):
    for i in range(len(attributes_list)):
        rand_int_number_of_connections = rd.randint(0, numb_of_links)
        for j in range (0,rand_int_number_of_connections):
            other_attr = rd.randint(0, len(attributes_list) - 1)
            while other_attr == i:
                other_attr = rd.randint(0, len(attributes_list) - 1)

            createLink(matrix=matrix, attribute_list=attributes_list, attribute1=attributes_list[i], attribute2=attributes_list[other_attr], risk=rd.randint(0,risk_max), time=rd.randint(1, time_max))
    return matrix


def analysis(path: str):
    path=os.path.join(path)
    csv_files = glob.glob(os.path.join(path, "*.csv")) 
    dfs=[]
    for f in csv_files:
        df_ = pd.read_csv(f)
        dfs.append(df_)
    df = pd.concat(dfs, ignore_index=True)
    
    return df

'''Function to find all Attributes with components that present, so the user can choose 1'''
def list_repeat(list_attr: list[str], attr: str):
    repated_index=[index for index, name in enumerate(list_attr) if name == attr]
    return repated_index

'''Function to list unique values and count their frequency'''
def count_and_list(series):
    unique_values = list(set(series))
    count_dict = {value: series[series == value].count() for value in unique_values}
    return unique_values, count_dict


'''Groupby Attribute.Component given a mean tick to fail and the unique listing to Origin '''
def countFailureMode(df=None, **path):
    if df is None:
        # If df is not provided, check if a file path is provided
        if 'path' in path:
            df = analysis(path['path'])
    
    result = df.groupby('Attribute.Component').agg({
        'Tick': 'mean',
        'Origin': count_and_list
    }).reset_index()

    # Extract unique values from 'Origin' dynamically
    unique_origins = set()
    for origin_list, _ in result['Origin']:
        unique_origins.update(origin_list)

    # Creating new columns for Unique Origin and their counts
    for value in unique_origins:
        result[value] = result['Origin'].apply(lambda x: x[1].get(value, 0))

    result = result.drop(columns=['Origin'])
    result.columns = ['Attribute.Component', 'Mean Tick to Fail'] + [f'{value}' for value in result.columns[2:]]
    
    return result


'''Heatmap plot'''
def plot_heatmap(count_values:list =None, origin_columns:list =None, normalize:bool=False,path:str=None):
    '''If a path is given, it also works'''
    if path is not None:  
        count_values=countFailureMode(path=path)
    '''Eliminate the reading of the 2 first columns ATTRIBUTE.COMPONENT and MEAN TICK TO FAIL'''
    if origin_columns is None:
        origin_columns = count_values.columns[2:]
        
    heatmap_data = count_values.set_index('Attribute.Component')[origin_columns]
    
    '''Don't know how to normalize it yet. Ideas?'''
    if normalize== True: 
        '''Yet to be implemented'''
        
        print('Not yet implemented')


    ''' To guarantee the same order '''
    order = [component.replace('_Count', '') for component in heatmap_data.index.tolist()]

    '''Plot of the map'''
    plt.figure(figsize=(10, 8))
    ax=sns.heatmap(heatmap_data.loc[order, :], annot=True, fmt='g', cmap='copper', linewidths=.5, square=True, cbar_kws={"orientation": "vertical"})
    plt.gca().invert_yaxis()

    plt.title('Count of failures: Origin to Destiny', pad=20)
    plt.xlabel('Attribute(Origin)')
    plt.ylabel('Attribute (Destiny)')
    plt.show()