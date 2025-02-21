import torch
from quantum_state import QuantumState
from coulomb_model import CoulombModel

class QuantumAlgorithms:
    def __init__(self, quantum_state: QuantumState, coulomb_model: CoulombModel) -> None:
        self.quantum_state = quantum_state
        self.coulomb_model = coulomb_model
        print("[QuantumAlgorithms] Initialized with quantum state and Coulomb model.")

    def apply_vqe(self, max_iterations: int = 100) -> None:
        print("[QuantumAlgorithms] Applying VQE.")
        state_vector = torch.nn.Parameter(
            self.quantum_state.state_vector.clone().detach(), requires_grad=True
        )
        optimizer = torch.optim.Adam([state_vector], lr=0.01)
        for iteration in range(max_iterations):
            optimizer.zero_grad()
            self.coulomb_model.apply_coulomb_interaction()
            loss = -torch.real(torch.sum(state_vector))
            loss.backward(retain_graph=True)
            optimizer.step()
            print(f"[VQE] Iteration {iteration}, Loss: {loss.item()}")
        with torch.no_grad():
            self.quantum_state.state_vector.copy_(state_vector.detach())
        print("[QuantumAlgorithms] VQE optimization completed.")

    def apply_qaoa(self, max_iterations: int = 100) -> None:
        print("[QuantumAlgorithms] Applying QAOA.")
        # Ensure state_vector is a leaf tensor
        state_vector = torch.nn.Parameter(
            self.quantum_state.state_vector.clone().detach(), requires_grad=True
        )
        optimizer = torch.optim.Adam([state_vector], lr=0.01)
        for iteration in range(max_iterations):
            optimizer.zero_grad()
            self.coulomb_model.apply_coulomb_interaction()
            cost = torch.norm(state_vector)  # Placeholder cost function
            cost.backward(retain_graph=True)
            optimizer.step()
            print(f"[QAOA] Iteration {iteration}, Cost: {cost.item()}")

        with torch.no_grad():
            self.quantum_state.state_vector.copy_(state_vector.detach())
        
        print("[QuantumAlgorithms] QAOA optimization completed.")

    def apply_custom_algorithm(self) -> None:
        print("[QuantumAlgorithms] Applying custom quantum algorithm.")
        self.coulomb_model.simulate_quantum_tunneling(barrier_width=1.0, barrier_height=10.0)
        self.quantum_state.state_vector = torch.nn.Parameter(
            self.quantum_state.state_vector.detach() * torch.tensor(1.1, dtype=torch.complex64), requires_grad=True
        )
        print(f"[Custom Algorithm] State vector: {self.quantum_state.state_vector}")
