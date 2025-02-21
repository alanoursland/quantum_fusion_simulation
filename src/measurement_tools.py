import torch
from typing import Any, Dict
from quantum_state import QuantumState
import numpy as np

class MeasurementTools:
    def measure_state(self, quantum_state: QuantumState, num_samples: int = 1000) -> Dict[str, Any]:
        print("[MeasurementTools] Measuring quantum state using probabilistic sampling.")
        state_vector = quantum_state.state_vector
        probabilities = torch.abs(state_vector) ** 2

        # Normalize probabilities to ensure they sum to 1
        probabilities = probabilities / probabilities.sum()

        # Sample the quantum state based on probabilities
        samples = np.random.choice(len(probabilities), size=num_samples, p=probabilities.detach().numpy())
        measurement_counts = dict(zip(*np.unique(samples, return_counts=True)))
        measurement_data = {
            "state_vector": state_vector,
            "probabilities": probabilities,
            "measurement_counts": measurement_counts
        }
        print(f"[MeasurementTools] Measurement data: {measurement_data}")
        return measurement_data

    def analyze_results(self, measurement_data: Dict[str, Any]) -> Dict[str, Any]:
        print("[MeasurementTools] Analyzing measurement data with fusion probability estimation.")
        measurement_counts = measurement_data["measurement_counts"]

        # Estimate fusion probability based on a custom probabilistic model
        total_measurements = sum(measurement_counts.values())
        fusion_state = max(measurement_counts, key=measurement_counts.get, default=0)
        fusion_probability = measurement_counts.get(fusion_state, 0) / total_measurements

        # Include the full measurement data along with the analysis
        analysis_results = {
            "fusion_probability": fusion_probability,
            "fusion_state": fusion_state,
            "state_vector": measurement_data["state_vector"],
            "probabilities": measurement_data["probabilities"],
            "measurement_counts": measurement_counts
        }
        print(f"[MeasurementTools] Analysis results: {analysis_results}")
        return analysis_results

    def visualize_measurements(self, measurement_data: Dict[str, Any]) -> None:
        import matplotlib.pyplot as plt

        print("[MeasurementTools] Visualizing measurement data.")
        measurement_counts = measurement_data["measurement_counts"]
        states = list(measurement_counts.keys())
        counts = list(measurement_counts.values())

        plt.figure(figsize=(8, 6))
        plt.bar(states, counts, color='blue')
        plt.xlabel('Quantum State')
        plt.ylabel('Measurement Counts')
        plt.title('Quantum State Measurement Distribution')
        plt.show()
