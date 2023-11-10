from objetos import *
import pandas as pd 
import time
import random as rd
#Reading the mock file!
# df= pd.read_excel("Teste.xlsx",header=0)

# #

Motor=Component(name="Motor")
GeometryMotor=Propriety(name="Geometry", component=Motor,risk=10)
print(GeometryMotor.component.name)



tick=0

State_machine(propriety=GeometryMotor,tick=tick)
    