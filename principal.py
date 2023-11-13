from objetos import *
import pandas as pd 
import time
import random as rd
import numpy as np 

Motor=Component(name="Motor")
GeometryMotor=Propriety(name="Geometry", component=Motor,risk=50)
MaterialMotor=Propriety(name="Material", component=Motor,risk=0)
TemperatureMotor=Propriety(name="Temperature", component=Motor,risk=0)

fan= Component(name="Fan")
GeometryFan= Propriety(name="Geometry", component=fan,risk=1)
Link(time=10, attribute1=GeometryFan,attribute2=MaterialMotor,risk=10)
Link(time=3,attribute1=GeometryMotor,attribute2=MaterialMotor,risk=100)
Link(time=12,attribute1=GeometryMotor,attribute2=TemperatureMotor,risk=50)




comp= [Motor,fan]
tick=0

State_machine(components=comp,tick=tick)
    