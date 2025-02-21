import torch
from quantum_state import QuantumState
from typing import List, Dict, Any

class SimulationRunner:
    def __init__(self, quantum_state: QuantumState) -> None:
        self.quantum_state = quantum_state
        self.results = []
        print("[SimulationRunner] Initialized with quantum state.")

    def run_simulation(self, iterations: int = 100, adaptive: bool = False, batch_params: List[Dict[str, Any]] = None, stopping_threshold: float = None) -> None:
        if batch_params:
            print(f"[SimulationRunner] Running batch simulations with {len(batch_params)} parameter sets.")
            self.run_batch_simulations(batch_params, stopping_threshold)
        else:
            print(f"[SimulationRunner] Running simulation for {iterations} iterations.")
            self.run_adaptive_simulation(iterations, adaptive, stopping_threshold)

    def run_adaptive_simulation(self, iterations: int, adaptive: bool, stopping_threshold: float) -> None:
        for i in range(iterations):
            # print(f"[SimulationRunner] Iteration {i+1}/{iterations}")
            if adaptive:
                self.adapt_simulation_parameters()
            if stopping_threshold and self.check_stopping_condition(stopping_threshold):
                print("[SimulationRunner] Stopping condition met. Terminating simulation early.")
                break
            self.results.append(self.quantum_state.state_vector.clone())
        print("[SimulationRunner] Simulation completed.")

    def run_batch_simulations(self, batch_params: List[Dict[str, Any]], stopping_threshold: float) -> None:
        for idx, params in enumerate(batch_params):
            print(f"[SimulationRunner] Running batch {idx+1}/{len(batch_params)} with parameters: {params}")
            self.quantum_state.set_initial_state(params['initial_state'])
            self.run_adaptive_simulation(params.get('iterations', 100), params.get('adaptive', False), stopping_threshold)

    def adapt_simulation_parameters(self) -> None:
        print("[SimulationRunner] Adapting simulation parameters dynamically.")
        # Placeholder for parameter adaptation logic

    def check_stopping_condition(self, threshold: float) -> bool:
        current_value = torch.norm(self.quantum_state.state_vector).item()
        print(f"[SimulationRunner] Checking stopping condition: Current value = {current_value}, Threshold = {threshold}")
        return current_value >= threshold

    def get_results(self) -> List[torch.Tensor]:
        return self.results
