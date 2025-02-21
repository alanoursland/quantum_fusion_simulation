import torch
from quantum_state import QuantumState
import numpy as np
from scipy.integrate import quad

elementary_charge = 1.602e-19
one_nanometer = 1e-10

class CoulombModel:
    def __init__(self, quantum_state: QuantumState, ion_charge: float = elementary_charge, interaction_distance: float = one_nanometer, external_potential: float = 0.0) -> None:
        self.quantum_state = quantum_state
        self.ion_charge = ion_charge
        self.interaction_distance = interaction_distance
        self.external_potential = external_potential
        print("[CoulombModel] Initialized with quantum state, ion charge, and interaction distance.")

    def apply_coulomb_interaction(self) -> None:
        k = 8.99e9
        potential_energy = k * (self.ion_charge ** 2) / self.interaction_distance
        potential_energy += self.external_potential
        print(f"[CoulombModel] Calculated potential energy: {potential_energy}")
        
        # Log-space: log(state) - V
        log_state = torch.log(self.quantum_state.state_vector + 1e-10)  # Avoid log(0)
        log_state -= torch.tensor(potential_energy, dtype=torch.complex64)
        self.quantum_state.state_vector = torch.exp(log_state)
        print(f"[CoulombModel] State vector after applying Coulomb interaction: {self.quantum_state.state_vector}")

    def simulate_quantum_tunneling_simple(self, barrier_width: float, barrier_height: float) -> None:
        print(f"[CoulombModel] Simulating quantum tunneling with barrier width {barrier_width} and height {barrier_height}.")
        mass = 1.67e-27  # Approximate mass of a hydrogen ion in kg
        hbar = 1.0545718e-34  # Reduced Planck's constant in Js

        # Calculate tunneling probability using a simple approximation
        kappa = np.sqrt(2 * mass * barrier_height) / hbar
        tunneling_probability = np.exp(-2 * kappa * barrier_width)

        print(f"[CoulombModel] Calculated tunneling probability: {tunneling_probability}")
        self.quantum_state.state_vector = self.quantum_state.state_vector * torch.tensor(tunneling_probability, dtype=torch.complex64)
        print(f"[CoulombModel] State vector after quantum tunneling simulation: {self.quantum_state.state_vector}")

    def simulate_quantum_tunneling(self, r_initial: float, energy: float) -> None:
        print(f"[CoulombModel] Simulating tunneling with r_initial={r_initial} m and energy={energy} J.")

        # Physical constants
        mass = 1.67e-27         # Proton mass (kg)
        hbar = 1.0545718e-34      # Reduced Planck's constant (J·s)
        k_e = 8.9875517923e9      # Coulomb constant (N·m²/C²)
        e_charge = 1.602e-19      # Elementary charge (C)
        r_nuclear = 1e-15         # Approximate nuclear radius (m)

        # If already inside the nuclear region, assume a high probability.
        if r_initial <= r_nuclear:
            # print(f"[CoulombModel] r_initial is within the nuclear region (r ≤ {r_nuclear}).")
            T = 0.9  # Use a high probability (or 1.0 if appropriate)
        else:
            # Coulomb potential at a given r: V(r) = k_e * e^2 / r.
            V_initial = k_e * e_charge**2 / r_initial

            # If the energy exceeds the potential at r_initial, there's no barrier.
            if energy >= V_initial:
                # print(f"[CoulombModel] Energy exceeds or equals the Coulomb potential at r_initial (V={V_initial}). No barrier.")
                T = 1.0
            else:
                # Determine the classical turning point.
                # For positive energy: r_turn = k_e * e^2 / energy.
                # For negative energy, use the absolute value.
                if energy > 0:
                    r_turn = k_e * e_charge**2 / energy
                else:
                    r_turn = k_e * e_charge**2 / abs(energy)
                
                # Ensure the integration domain is valid.
                r_turn = max(r_turn, r_initial + 1e-20)
                # print(f"[CoulombModel] Classical turning point: r_turn = {r_turn} m.")

                # Define the WKB integrand.
                def integrand(r):
                    V_r = k_e * e_charge**2 / r
                    return np.sqrt(2 * mass * (V_r - energy)) / hbar

                # Integrate from r_initial to r_turn.
                integral, abserr = quad(integrand, r_initial, r_turn)
                # print(f"[CoulombModel] WKB integral = {integral} (abserr = {abserr}).")
                
                # Calculate the tunneling probability.
                T = np.exp(-2 * integral)
        
        print(f"[CoulombModel] Calculated tunneling probability: {T}")

        # Handle potential numerical underflow.
        if T < 1e-30:
            T = 1e-30
            print("[CoulombModel] Warning: Underflow capped at 1e-30")

        # Update the quantum state by multiplying the state vector by sqrt(T).
        T_tensor = torch.tensor(T, dtype=torch.float64)
        self.quantum_state.state_vector *= torch.sqrt(T_tensor)
        print(f"[CoulombModel] Updated state vector: {self.quantum_state.state_vector}")
