import json
import h5py
import torch
import matplotlib.pyplot as plt
from typing import Any, Dict, List
import numpy as np

class DataHandler:
    def save_data(self, data: Dict[str, Any], filename: str, format: str = 'json') -> None:
        print(f"[DataHandler] Saving data to {filename} in {format} format.")

        # Convert non-serializable objects to serializable formats
        def convert_to_serializable(obj):
            # print(f"Converting {obj} {type(obj)}")
            
            if isinstance(obj, torch.Tensor):
                # Convert tensors to lists and handle complex numbers if present
                array = obj.detach().cpu().numpy()
                if np.iscomplexobj(array):
                    return [{"real": float(v.real), "imag": float(v.imag)} for v in array]
                return array.tolist()
            
            if isinstance(obj, np.integer):
                return int(obj)  # Convert numpy int to native int
            
            if isinstance(obj, np.floating):
                return float(obj)  # Convert numpy float to native float
            
            if isinstance(obj, np.ndarray):
                # Handle numpy arrays, including complex arrays
                if np.iscomplexobj(obj):
                    return [{"real": float(v.real), "imag": float(v.imag)} for v in obj]
                return obj.tolist()
            
            if isinstance(obj, complex):
                # Convert complex numbers to a JSON-compatible dictionary
                return {"real": float(obj.real), "imag": float(obj.imag)}
            
            if isinstance(obj, dict):
                # Recursively convert dictionary keys and values
                return {str(k): convert_to_serializable(v) for k, v in obj.items()}
            
            if isinstance(obj, (list, tuple, set)):
                # Recursively convert elements in iterable containers
                return [convert_to_serializable(v) for v in obj]
            
            # Specific handling for PyTorch data types
            if type(obj) in [torch.int32, torch.int64, torch.float32, torch.float64]:
                return obj.item()  # Convert to a native Python scalar

            return str(obj)  # Fallback for any other types

        # Preprocess the entire data dictionary
        data = convert_to_serializable(data)

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
        import matplotlib.pyplot as plt
        import numpy as np

        print(f"[DataHandler] Visualizing data with plot type: {plot_type}.")
        
        if plot_type == 'wavefunction':
            # Correctly access the 'state_vector' for visualization
            state_vector = np.abs(data['state_vector'].detach().numpy())
            plt.figure(figsize=(8, 6))
            plt.plot(state_vector, label='Wavefunction', marker='o')
            plt.xlabel('State Index')
            plt.ylabel('Amplitude')
            plt.title('Quantum State Wavefunction Visualization')
            plt.legend()
            plt.grid(True)
            plt.show()
            
        elif plot_type == 'probability_distribution':
            probabilities = np.array(data['probabilities'])
            plt.figure(figsize=(8, 6))
            plt.bar(range(len(probabilities)), probabilities, color='blue')
            plt.xlabel('State Index')
            plt.ylabel('Probability')
            plt.title('Probability Distribution of Quantum States')
            plt.grid(True)
            plt.show()
        
        else:
            print(f"[Visualization] Unsupported plot type: {plot_type}")

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
