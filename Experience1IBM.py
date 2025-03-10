from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit import QuantumRegister, ClassicalRegister

service = QiskitRuntimeService()

backend = service.least_busy(operational=True, simulator=False, min_num_qubits=1)
print(backend.name)

# Paramètres
phi_values = np.linspace(0, 4*np.pi, 30)  # Variation du déphasage
alpha = 0  # Rotation de l’ancilla

energyValues = []

for phi in phi_values :
    qreg_q = QuantumRegister(2, 'q')
    creg_c = ClassicalRegister(7, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)

    circuit.reset(qreg_q[0])
    circuit.reset(qreg_q[1])
    circuit.h(qreg_q[0])
    circuit.ry(alpha, qreg_q[1])
    circuit.p(phi, qreg_q[0])
    circuit.ch(qreg_q[1], qreg_q[0])
    circuit.measure(qreg_q[0], creg_c[0])


    qc_transpiled = transpile(circuit, backend, optimization_level=2)
    sampler = Sampler(backend)
    qc_job = sampler.run([qc_transpiled], shots=1000)
    result = qc_job.result()[0].data.c.get_counts()

    # Affichage des résultats

    energy = result['0000000'] / 1024
    energyValues.append(energy)

plt.plot(phi_values,energyValues)
plt.show()