import numpy as np
from qiskit import *
import matplotlib.pyplot as plt

# The fundamental unit of Qiskit is the quantum circuit.
# Basic workflow consists of two stages: Build & Execute
# Build: make different QC's, Execute: run them on diff backends

circ = QuantumCircuit(3) # creates circuit with 3 Qubit registers

# These are operations we are adding to our circuit. 
circ.h(0)
circ.cx(0,1)
circ.cx(0,2)

# circ.draw(output='mpl')
# plt.show()

# Qiskit Aer is a package for simulating quantum circuits. Provides backends for doing a simulation
# The most common backend is statevector_simualtor. It returns the quantum state, which is a complex
# vector of dimensions 2^n, where n is the number of qubits

from qiskit import Aer

backend = Aer.get_backend('statevector_simulator')
job = execute(circ, backend)
result = job.result()
outputstate = result.get_statevector(circ, decimals=3)
print(outputstate)

from qiskit.visualization import plot_state_city
plot_state_city(outputstate)
plt.show()