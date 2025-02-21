# src/data_handler.py
import json
from typing import Any, Dict

class DataHandler:
    def save_data(self, data: Dict[str, Any], filename: str) -> None:
        print(f"[DataHandler] Saving data to {filename}.")
        with open(filename, 'w') as f:
            json.dump(data, f)
        print("[DataHandler] Data saved successfully.")

    def visualize(self, data: Dict[str, Any]) -> None:
        print("[DataHandler] Visualizing data.")
        print(data)