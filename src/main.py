from quantum_simulator import QuantumSimulator
from quantum_state import QuantumState
from coulomb_model import CoulombModel
from quantum_operations import QuantumOperations
from quantum_algorithms import QuantumAlgorithms
from measurement_tools import MeasurementTools
from simulation_runner import SimulationRunner
from data_handler import DataHandler

import torch

# Initialize the simulation environment
simulator = QuantumSimulator(backend='pytorch')
simulator.initialize()

# Initialize quantum state for two hydrogen ions
quantum_state = QuantumState(num_ions=2)
initial_state = torch.tensor([1.0, 0.0, 0.0, 0.0], dtype=torch.complex64, requires_grad=True)
quantum_state.set_initial_state(initial_state)

initial_distance = 1e-14

# Apply Coulomb interaction model
coulomb_model = CoulombModel(quantum_state, interaction_distance=initial_distance)
coulomb_model.apply_coulomb_interaction()

# Quantum manipulations
quantum_operations = QuantumOperations()
quantum_operations.apply_superposition(quantum_state)
quantum_operations.apply_phase_shift(quantum_state, angle=3.1415 / 4)
quantum_operations.apply_entanglement(quantum_state, target_indices=(0, 1))

# Apply quantum algorithms
quantum_algorithms = QuantumAlgorithms(quantum_state, coulomb_model)
quantum_algorithms.apply_vqe(max_iterations=100)
# quantum_algorithms.apply_qaoa(max_iterations=100)
quantum_algorithms.apply_custom_algorithm(r_initial=initial_distance, energy=1.6e-15, max_iterations=100)

# quantum_algorithms.coulomb_model.simulate_quantum_tunneling(r_initial=5e-15, energy=2.3e-13)  # First test case
# quantum_algorithms.coulomb_model.simulate_quantum_tunneling(r_initial=1e-14, energy=1.6e-15)  # Second test case (original)
# quantum_algorithms.coulomb_model.simulate_quantum_tunneling(r_initial=1e-15, energy=1.6e-15)   #Third test case, inside r_fusion.
# quantum_algorithms.coulomb_model.simulate_quantum_tunneling(r_initial=1e-14, energy=-1.6e-15) # Fourth test case, negative energy



# # Measurement and analysis
measurement_tools = MeasurementTools()
measurement_data = measurement_tools.measure_state(quantum_state)
analysis_results = measurement_tools.analyze_results(measurement_data)

# # Run simulation and optimization
simulation_runner = SimulationRunner(quantum_state)
simulation_runner.run_simulation(iterations=100)

# # Data handling and visualization
data_handler = DataHandler()
data_handler.save_data(analysis_results, 'simulation_results.json')
data_handler.visualize(analysis_results)

print("Simulation completed successfully.")
