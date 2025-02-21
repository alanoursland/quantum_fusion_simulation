import json
import h5py
import matplotlib.pyplot as plt
from typing import Any, Dict, List
import numpy as np

class DataHandler:
    def save_data(self, data: Dict[str, Any], filename: str, format: str = 'json') -> None:
        print(f"[DataHandler] Saving data to {filename} in {format} format.")
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(data, f)
        elif format == 'hdf5':
            with h5py.File(filename, 'w') as f:
                for key, value in data.items():
                    f.create_dataset(key, data=value)
        else:
            raise ValueError(f"Unsupported format: {format}")
        print("[DataHandler] Data saved successfully.")

    def visualize(self, data: Dict[str, Any], plot_type: str = 'wavefunction') -> None:
        print(f"[DataHandler] Visualizing data with plot type: {plot_type}.")
        if plot_type == 'wavefunction':
            state_vector = np.abs(np.array(data['state_vector']))
            plt.plot(state_vector, label='Wavefunction')
            plt.xlabel('State Index')
            plt.ylabel('Amplitude')
            plt.title('Quantum State Wavefunction Visualization')
            plt.legend()
            plt.show()
        elif plot_type == 'probability_distribution':
            probabilities = np.array(data['probabilities'])
            plt.bar(range(len(probabilities)), probabilities)
            plt.xlabel('State Index')
            plt.ylabel('Probability')
            plt.title('Probability Distribution of Quantum States')
            plt.show()

    def compare_simulations(self, results: List[Dict[str, Any]]) -> None:
        print("[DataHandler] Comparing multiple simulation results.")
        for idx, result in enumerate(results):
            probabilities = np.array(result['probabilities'])
            plt.plot(probabilities, label=f'Simulation {idx+1}')
        plt.xlabel('State Index')
        plt.ylabel('Probability')
        plt.title('Comparative Analysis of Simulation Results')
        plt.legend()
        plt.show()
