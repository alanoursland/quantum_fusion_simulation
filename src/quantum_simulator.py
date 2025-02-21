# src/quantum_simulator.py
import torch

class QuantumSimulator:
    def __init__(self, backend: str = 'pytorch') -> None:
        self.backend = backend.lower()
        self.device = self._setup_device()
        print(f"[QuantumSimulator] Initialized with backend: {self.backend} on device: {self.device}")

    def _setup_device(self) -> torch.device:
        if self.backend == 'pytorch' and torch.cuda.is_available():
            print("[QuantumSimulator] CUDA available. Using GPU.")
            return torch.device('cuda')
        else:
            print("[QuantumSimulator] CUDA not available or not using PyTorch backend. Using CPU.")
            return torch.device('cpu')

    def initialize(self) -> None:
        print("[QuantumSimulator] Simulation environment initialized.")

    def set_backend(self, backend: str) -> None:
        self.backend = backend.lower()
        print(f"[QuantumSimulator] Backend switched to: {self.backend}")

    def get_device(self) -> torch.device:
        return self.device

    def run(self) -> None:
        print(f"[QuantumSimulator] Running simulation with {self.backend} on {self.device}")
