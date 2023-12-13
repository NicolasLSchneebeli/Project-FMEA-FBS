from objetos import *
from function import *
try:
    import openpyxl
except ImportError:
    print("Error: Required module 'openpyxl' not found.")
    print("Please create and activate a virtual environment, then run: pip install -r requirements.txt")
    exit(1)
possible_inputs= ['Y', 'N']


print("=============== Start Program ================")
print('========= Please read the HELPME for info about input and commands. The excel file should have columns in this order: =========')
print('Component, Attribute, Prob_of_Failure')
print('They are case-sensitive and in this order! Attention for the underline (_) as well!')

print('Name of the excel:' )
input_file=input()
list_comp,attributes=readFile(excel_file=f'Projeto_FRANÇA/{input_file}.xlsx')

print(f'Using file named as {input_file}')
names=[attr.name for attr in attributes ]

inp=input('Do you want random links? Y/N: ').upper()
while inp not in possible_inputs:
    inp=input('Do you want random links? Y/N: ').upper()

'''Creating LINKS'''
if inp =='Y':
    print('================= Random Links ================= ')
    inp_ = 'Y'
    while inp_ == 'Y':
        links=createMatrix(attributes_list=attributes,random=True)
        print(links)
        inp_=input('Want to renegenarate? Y/N ').upper()
        while inp_ not in possible_inputs:
            inp_=input('Want to renegenarate? Y/N ').upper()

else:
    links=createMatrix(attributes_list=attributes)
    print('==================Proceed to create links ==================')
    opt= 'Y'
    while opt== 'Y':
        print(names)
        attr1=input(f'Choose the first attribute name: ').lower()
        while attr1 not in names:
            print(f'Attribute "{attr1}" not found. Careful with spelling/ spacing.')
            attr1=input(f'Choose the first attribute name: ').lower()
        repetetions_comp1= list_repeat(names,attr=attr1)
        if len(repetetions_comp1) >1:
            print('Please select from which component and attribute do you wish to create a link:')
            comp_names =[attributes[index].component.name for index in repetetions_comp1]
            print(f'For {attr1} there are:{comp_names} ')
            inp_comp1= input('Select which component name do you wish: ').lower()
            while inp_comp1 not in comp_names:
                print("Component not found")
                inp_comp1= input('Select which component name do you wish: ').lower()
            attr1_index = repetetions_comp1[comp_names.index(inp_comp1)]
            
        else:
            attr1_index=names.index(attr1)
            
            
        attr2=input(f'Choose the second attribute name: ').lower()
        while attr2 not in names:
            print(f'Attribute "{attr2}" not found. Careful with spelling/ spacing.')
            attr2=input(f'Choose the second attribute name: ').lower()
            
        repetetions_comp2= list_repeat(names, attr=attr2)

        if len(repetetions_comp2) >1:
            print('Please select from which component and attribute do you wish to create a link:')
            comp_names =[attributes[index].component.name for index in repetetions_comp2]
            print(f'For {attr2} there are:{comp_names} ')
            inp_comp2= input('Select which component name do you wish: ').lower()
            while inp_comp2 not in comp_names:
                print("Component not found")
                inp_comp2= input('Select which component name do you wish: ').lower()
            attr2_index = repetetions_comp2[comp_names.index(inp_comp2)]

        else:
            attr2_index=names.index(attr2)
                    
        risk= int(input('Choose risk: '))
        time= int(input('Choose time condition to infection: '))
        
        if risk <=0 or risk >100:
            print('Invalid risk value')
            risk= input('Choose risk: ')
            continue
        if time <0:
            print('Invalid time value')
            time= input('Choose time condition to infection: ')
            continue

        else:
            createLink(matrix=links,attribute_list=attributes,attribute1=attributes[attr1_index], attribute2=attributes[attr2_index], risk=risk, time=time)
            print(f'Created a link between {attr1} and {attr2} with risk {risk} and time condition {time}')
            opt=input('Do you wish to create more links? Y/N ').upper()
            while opt not in possible_inputs:
                opt=input('Do you wish to create more links? Y/N ').upper()

            
'''Creating BEHAVIOURS'''

print('========================== Creating now the stop conditions (Behaviours) =========================')   
optbeh = 'Y'
beh_list=[]
while optbeh == 'Y':   
    beh=input('Choose behaviour name: ')
    beh=Behaviour(name=f"{beh}")
    beh_list.append(beh)
    optcond='Y'
    while optcond=='Y':
        print('-------------------------------------------------------')
        print(names)
        attrcond=input(f'Choose component condition for {beh.name} to stop:  ')
        while attrcond not in names:
            print('Attribute not found!')
            attrcond=input(f'Choose component condition for {beh.name} to stop:  ')

        rep_cond=list_repeat(list_attr=names,attr=attrcond)
        if len(rep_cond)>1:
            print('Please select from which component and attribute do you wish to create a condition:')
            comp_names =[attributes[index].component.name for index in rep_cond]
            print(f'For {attrcond} there are:{comp_names} ')
            inp_cond= input('Select which component name do you wish: ').lower()
            while inp_cond not in comp_names:
                print(comp_names)
                print("Component not found. Careful with spacing")
                inp_cond= input('Select which component name do you wish: ').lower()
        
            attrcond_index = rep_cond[comp_names.index(inp_cond)]
        else:
            attrcond_index=names.index(attrcond)
        beh.addCondition(attributes[attrcond_index])    
        optcond=input('Wish to add more conditions? Y/N ' ).upper()
        while optcond not in possible_inputs:
            optcond=input('Wish to add more conditions? Y/N ' ).upper()

    optbeh= input('Wish to continue creating behaviour? Y/N ').upper()
    while optbeh not in possible_inputs:
        optbeh= input('Wish to continue creating behaviour? Y/N ').upper()

        
        
print('=========== Proceed to simulation ===========')
numb_of_interactions=(input('Run how many times the simulation? '))
numb_of_interactions=int(numb_of_interactions)
caminho=State_machine(components=list_comp,behaviour=beh_list,link_matrix=links,attrs= attributes, number_of_interaction=numb_of_interactions)

option=input('Wish to proceed with analysis? Y/N ').upper()
while option not in possible_inputs:
    option=input('Wish to proceed with analysis? Y/N ').upper()

if option == 'Y':
    df= analysis(path=caminho)
    result=countFailureMode(df=df)
    plot_heatmap(count_values=result)
else:
    exit