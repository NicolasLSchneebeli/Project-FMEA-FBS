from objetos import *
from function import *

motor= Component(name="Motor")
geometry= Propriety(name="Geometry", component= motor,risk=90)
material= Propriety(name="Material",component= motor, risk=90)
Link(time=2, attribute1=geometry, attribute2=material,risk=90)
material.getLinks()



Mov=Behaviour(name="Movement")
Mov.addCondition(material)
Mov.addCondition(geometry)
Inf_Iteraction= Behaviour(name="teste")



# motor=Component(name="Motor")
# motor1=Component(name="Motor1")

# GeometryMotor=Propriety(name="Geometry", component=Motor,risk=10)
# MaterialMotor=Propriety(name="Material", component=Motor,risk=10)
# TemperatureMotor=Propriety(name="Temperature", component=Motor,risk=10)

# fan= Component(name="Fan")
# GeometryFan= Propriety(name="Geometry", component=fan,risk=100)



# Link(time=2, attribute1=GeometryFan,attribute2=MaterialMotor,risk=100)
# Link(time=2,attribute1=TemperatureMotor,attribute2=GeometryMotor,risk=10)
# Link(time=3,attribute1=TemperatureMotor,attribute2=MaterialMotor,risk=10)


comp= [motor]
tick=0

State_machine(components=comp,tick=tick,behaviour=[Mov])

