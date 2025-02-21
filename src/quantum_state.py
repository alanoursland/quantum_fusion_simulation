# src/quantum_state.py
import torch

class QuantumState:
    def __init__(self, num_ions: int) -> None:
        self.num_ions = num_ions
        self.state_vector = None
        print(f"[QuantumState] Created quantum state for {self.num_ions} ions.")
    
    def set_initial_state(self, state_vector: torch.Tensor) -> None:
        self.state_vector = state_vector
        print(f"[QuantumState] Initial state set to: {self.state_vector}")
