from objetos import *
import pandas as pd 
import time
import random as rd
#Reading the mock file!
# df= pd.read_excel("Teste.xlsx",header=0)

# #

Motor=Component(name="Motor")
GeometryMotor=Propriety(name="Geometry", component=Motor,risk=100)
MaterialMotor=Propriety(name="Material", component=Motor,risk=0)
Link(time=3,attribute1=GeometryMotor,attribute2=MaterialMotor,risk=12)
comp= [Motor]



time.sleep(5)
tick=0

State_machine(components=comp,tick=tick)
    