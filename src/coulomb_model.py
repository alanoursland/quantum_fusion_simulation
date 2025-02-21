import torch
from quantum_state import QuantumState
import numpy as np

class CoulombModel:
    def __init__(self, quantum_state: QuantumState, ion_charge: float = 1.0, interaction_distance: float = 1.0, external_potential: float = 0.0) -> None:
        self.quantum_state = quantum_state
        self.ion_charge = ion_charge
        self.interaction_distance = interaction_distance
        self.external_potential = external_potential
        print("[CoulombModel] Initialized with quantum state, ion charge, and interaction distance.")

    def apply_coulomb_interaction(self) -> None:
        # Implementing Coulomb potential: V = k * (q1 * q2) / r
        k = 8.9875517923e9  # Coulomb's constant in N·m²/C²
        potential_energy = k * (self.ion_charge ** 2) / self.interaction_distance
        potential_energy += self.external_potential
        print(f"[CoulombModel] Calculated potential energy: {potential_energy}")

        # Update the quantum state with the potential energy
        self.quantum_state.state_vector *= torch.exp(-torch.tensor([potential_energy], dtype=torch.complex64))
        print(f"[CoulombModel] State vector after applying Coulomb interaction: {self.quantum_state.state_vector}")

    def simulate_quantum_tunneling(self, barrier_width: float, barrier_height: float) -> None:
        print(f"[CoulombModel] Simulating quantum tunneling with barrier width {barrier_width} and height {barrier_height}.")
        mass = 1.67e-27  # Approximate mass of a hydrogen ion in kg
        hbar = 1.0545718e-34  # Reduced Planck's constant in Js

        # Calculate tunneling probability using a simple approximation
        kappa = np.sqrt(2 * mass * barrier_height) / hbar
        tunneling_probability = np.exp(-2 * kappa * barrier_width)

        print(f"[CoulombModel] Calculated tunneling probability: {tunneling_probability}")
        self.quantum_state.state_vector *= torch.tensor(tunneling_probability, dtype=torch.complex64)
        print(f"[CoulombModel] State vector after quantum tunneling simulation: {self.quantum_state.state_vector}")
