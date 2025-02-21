# src/simulation_runner.py
from quantum_state import QuantumState

class SimulationRunner:
    def __init__(self, quantum_state: QuantumState) -> None:
        self.quantum_state = quantum_state
        print("[SimulationRunner] Initialized with quantum state.")
    
    def run_simulation(self, iterations: int = 100) -> None:
        print(f"[SimulationRunner] Running simulation for {iterations} iterations.")
        for i in range(iterations):
            print(f"[SimulationRunner] Iteration {i+1}/{iterations}")
        print("[SimulationRunner] Simulation completed.")

