# Author: Sean Seneviratne
import pennylane as qml
from pennylane import numpy as np

# https://pennylane.ai/qml/demos/tutorial_qubit_rotation.html
# Before creating a quantum node, we need to initialize a device 
# A quantum device is anything that can apply quantum operations and return a value
# Devices include: hardware plug-ins or software 

# The default qubit is a device provided by PennyLane - a simple pure-state qubit simulator
# All devices accept (name) and (wires:number of subsystems device is initiliazed with) as parameters
dev1 = qml.device("default.qubit", wires = 1)

# Constructing a Quantum Node
# QNodes are an encapsulation of a quantum function. QNodes are bound to a particular device which is 
# used to evaluate expectation and variance values of this circuit

@qml.qnode(dev1)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.PauliZ(0))

# print(circuit([0.54, 0.12]))

# Gradient of the function Circuit, can be computed. 
dcircuit = qml.grad(circuit, argnum = 0)
print(dcircuit([0.54, 0.12]))

# Optimizing - We can optimize the two circuit parameters such that the qubit orignally in state (0)
# is rotated to be in state (1). In order to do this we need to define a cost function that will 
# determine the values of the circuit parameters that produce the desired outcome.

# the goal is to change the value to -1

def cost(x):
    return circuit(x)
init_params = np.array([0.011, 0.012])
# print(cost(init_params))

opt = qml.GradientDescentOptimizer(stepsize=0.4)

steps = 100

params = init_params

for i in range(steps):
    params = opt.step(cost,params)

    if (i+1) % 5 == 0:
        print("cost after step {:5d}: {: .7f}".format(i + 1, cost(params)))


print("Optimized rotation angles: {}".format(params))