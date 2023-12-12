# CREATED BY Nicolas LOVATTE SCHNEEBELI  with orientation from Professor Jelena PETRONIJEVIC

OOP Simulation for python. User inputs a excel sheet and creates links. The output is which components are critical in their desig. 
# HELP GUIDE FOR PROTOTYPE:

## Classes:

There are 3 classes currently: 

### Components:

Components are the container for the whole system: They will hold all the attributes and also be the input of the simulation as a list of components


- Syntax: 

    - To create a component: $\textcolor{red}{Component(name=\textit{STRING})}$

    - To create add an Attribute to it: $\textcolor{red}{COMPONENT.addAttribute(name=ATTRIBUTE)}$

    - To view all Attributes being currently a part of the Component: $\textcolor{red}{COMPONENT.getAttributes()}$

### Propriety:

Proprieties are the main point of the simulation. Name in the program as Attributes, they are linked to each other and they generate the simulation.

- Syntax: 

    - To create a attribute: $\textcolor{red}{Propriety(name=\textit{STRING},component=COMPONENT, risk=\textit{DOUBLE})}$

    - To view to which component this attribute is linked: $\textcolor{red}{ATTRIBUTE.getComponent()}$

    - To add when the Attribute failed: $\textcolor{red}{ATTRIBUTE.addFailedTick(tick=time,data=df, origin= ORIGIN)}$ $\\$
    data is the dataframe responsible to save the data for simulation,
    origin is where the failure came from: self or infected by another via their link $\\$

    - To add different types of failure: $\textcolor{red}{ATTRIBUTE.addFailureMode( NAMES=[LIST],Risk=[LIST])}$ $\\$
    To add different types of failures to the attribute. For exemple $\textit{Excess of ..., Loss of ...}$

### Behaviour:

The behaviours acts as a stop method for the simulation. Once certain criteria is done, the simulation stops its self and generates a .csv containing the pertinant info.

- Syntax: 

    - To check the condition of the set of behaviours given as parameters: $\textcolor{red}{BEHAVIOUR.checkCondition()}$

    - To add a set of condition for the behaviour: $\textcolor{red}{BEHAVIOUR.addCondition(Condition)}$ $\\$
    Note: It has to be added one by one for now.


# Preparing to simulate

- You use: $\\$
$\textcolor{red}{list\_components,list\_attributes= readFile('EXCEL\_FILE.xlsx')}$. 
    - The Excel sheet Probability of Failure should be a float separeted by $\bold{dot (.)}$ 
    - It returns 2 lists: $\textcolor{blue}{Components}$ and $\textcolor{blue}{Attributes}$. To create the links accordinly what you desire using: 
- To create the links matrix: $\textcolor{red}{createMatrix(attributes\_list=attributes\_list)}$  
    - This will create a zeros matrix relating all the attributes to them self in a N $\times$ N matrix. This numbers will be the identifiers of the attributes throughout the whole process. 
- To create links: $ \textcolor{red}{createLink(matrix, attribute\_list, attribute_1[Number], attribute_2[Number])}$ 

Now your link matrix is done, you can start the simulation:
- To start the simulation: $\textcolor{red}{State\_machine(component\_list,behaviour\_list, link\_matrix, list\_attributes, **Number\_of\_interactions(default=1)}$
    - This will start the simulation, arguments containing ** before means that they are optional and have a value by default. The others are mandatory.
    - The simulation will output 2 csv files: 1 with criteria that stopped and containing all the attributes failures (with tick,name,component and origin (self or infect by other)). The other csv file will be the same, but without the criteria to stop.  