# src/quantum_state.py
import torch
import numpy as np

class QuantumState:
    def __init__(self, num_ions: int) -> None:
        self.num_ions = num_ions
        self.state_vector = None
        self.density_matrix = None
        print(f"[QuantumState] Created quantum state for {self.num_ions} ions.")

    def set_initial_state(self, state_vector: torch.Tensor) -> None:
        self.state_vector = state_vector
        self.density_matrix = torch.outer(state_vector, state_vector.conj())
        print(f"[QuantumState] Initial state set to: {self.state_vector}")

    def set_wavefunction(self, wavefunction: np.ndarray) -> None:
        """
        Sets the quantum state using a physical wavefunction.
        The wavefunction is converted to a state vector representation.
        """
        self.state_vector = torch.tensor(wavefunction, dtype=torch.complex64)
        self.density_matrix = torch.outer(self.state_vector, self.state_vector.conj())
        print(f"[QuantumState] Wavefunction set to: {self.state_vector}")

    def create_superposition(self, states: list[torch.Tensor], coefficients: list[complex]) -> None:
        """
        Creates a superposition of given quantum states with specified coefficients.
        The resulting state vector is a linear combination of input states.
        """
        self.state_vector = sum(c * s for c, s in zip(coefficients, states))
        self.density_matrix = torch.outer(self.state_vector, self.state_vector.conj())
        print(f"[QuantumState] Superposition state set to: {self.state_vector}")

    def set_density_matrix(self, density_matrix: torch.Tensor) -> None:
        """
        Allows direct setting of a density matrix for mixed state representation.
        """
        self.density_matrix = density_matrix
        print(f"[QuantumState] Density matrix set.")
