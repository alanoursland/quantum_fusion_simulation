import torch
from quantum_state import QuantumState
from typing import Tuple

class QuantumOperations:
    def apply_superposition(self, quantum_state: QuantumState) -> None:
        print("[QuantumOperations] Applying superposition.")
        # Apply a Hadamard gate to create a superposition state
        hadamard_matrix = torch.tensor([[1, 1], [1, -1]], dtype=torch.complex64) / torch.sqrt(torch.tensor(2.0))
        quantum_state.state_vector = torch.matmul(hadamard_matrix, quantum_state.state_vector)
        print(f"[QuantumOperations] New state after superposition: {quantum_state.state_vector}")

    def apply_phase_shift(self, quantum_state: QuantumState, angle: float) -> None:
        print(f"[QuantumOperations] Applying phase shift by {angle} radians.")
        phase_matrix = torch.tensor([[1, 0], [0, torch.exp(1j * angle)]], dtype=torch.complex64)
        quantum_state.state_vector = torch.matmul(phase_matrix, quantum_state.state_vector)
        print(f"[QuantumOperations] New state after phase shift: {quantum_state.state_vector}")

    def apply_entanglement(self, quantum_state: QuantumState, target_indices: Tuple[int, int]) -> None:
        print(f"[QuantumOperations] Entangling indices {target_indices}.")
        # Implementing a CNOT gate for entanglement
        cnot_matrix = torch.tensor(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 0, 1],
             [0, 0, 1, 0]], dtype=torch.complex64)
        quantum_state.state_vector = torch.matmul(cnot_matrix, quantum_state.state_vector)
        print(f"[QuantumOperations] State after entanglement: {quantum_state.state_vector}")

    def apply_pauli_x(self, quantum_state: QuantumState) -> None:
        print("[QuantumOperations] Applying Pauli-X (NOT) gate.")
        pauli_x = torch.tensor([[0, 1], [1, 0]], dtype=torch.complex64)
        quantum_state.state_vector = torch.matmul(pauli_x, quantum_state.state_vector)
        print(f"[QuantumOperations] State after Pauli-X: {quantum_state.state_vector}")

    def apply_custom_gate(self, quantum_state: QuantumState, gate_matrix: torch.Tensor) -> None:
        print("[QuantumOperations] Applying custom quantum gate.")
        quantum_state.state_vector = torch.matmul(gate_matrix, quantum_state.state_vector)
        print(f"[QuantumOperations] State after custom gate: {quantum_state.state_vector}")
