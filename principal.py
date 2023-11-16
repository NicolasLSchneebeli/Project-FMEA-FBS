from objetos import *
from function import State_machine
import pandas as pd 
import time
import random as rd
import numpy as np 

Motor=Component(name="Motor")

GeometryMotor=Propriety(name="Geometry", component=Motor,risk=10)
MaterialMotor=Propriety(name="Material", component=Motor,risk=10)
TemperatureMotor=Propriety(name="Temperature", component=Motor,risk=10)

fan= Component(name="Fan")
GeometryFan= Propriety(name="Geometry", component=fan,risk=100)



Link(time=2, attribute1=GeometryFan,attribute2=MaterialMotor,risk=100)
Link(time=2,attribute1=TemperatureMotor,attribute2=GeometryMotor,risk=10)
Link(time=3,attribute1=TemperatureMotor,attribute2=MaterialMotor,risk=10)


comp= [Motor,fan]
tick=0
print('-----------------------------------------------------------')
State_machine(components=comp,tick=tick)
