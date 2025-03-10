from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumRegister, ClassicalRegister
from numpy import pi
# Paramètres
phi_values = np.linspace(0, 2*pi, 20)  # Variation du déphasage
alpha = 0  # Rotation de l’ancilla

energyValues = []

for phi in phi_values :

    qreg_q = QuantumRegister(3, 'q')
    creg_c = ClassicalRegister(7, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)

    circuit.reset(qreg_q[0])
    circuit.reset(qreg_q[1])
    circuit.h(qreg_q[0])
    circuit.h(qreg_q[1])
    circuit.cx(qreg_q[1],qreg_q[2])
    circuit.p(phi, qreg_q[0])
    circuit.ch(qreg_q[1], qreg_q[0])

    circuit.ry(alpha, qreg_q[2])

    circuit.measure(qreg_q[0], creg_c[0])
    circuit.measure(qreg_q[2], creg_c[1])

    # Exécution sur simulateur
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    result = simulator.run(compiled_circuit).result()
    # Affichage des résultats
    energy = result.get_counts()['0000010'] / 1024
    energyValues.append(energy)



#circuit.draw(output='mpl')
plt.plot(phi_values,energyValues)
plt.show()