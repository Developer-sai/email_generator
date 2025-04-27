"""Data handler for processing lead and product information."""
import json
import os
from typing import Dict, Any, List


class DataHandler:
    """Class to handle loading and processing of lead and product data."""

    def __init__(self, data_path: str):
        """Initialize with path to data file.

        Args:
            data_path: Path to the JSON data file
        """
        self.data_path = data_path
        if not os.path.exists(data_path):
            print(f"Warning: Data file {data_path} not found")
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file.

        Returns:
            Dict containing the loaded data
        """
        try:
            if not os.path.exists(self.data_path):
                print(f"Error: Data file {self.data_path} not found")
                return {"leads": [], "product": {}}
                
            with open(self.data_path, 'r') as file:
                data = json.load(file)
                # Validate expected structure
                if "leads" not in data or "product" not in data:
                    print("Warning: Data file missing 'leads' or 'product' sections")
                return data
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.data_path}")
            return {"leads": [], "product": {}}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {"leads": [], "product": {}}

    def get_lead_by_id(self, lead_id: int) -> Dict[str, Any]:
        """Get a specific lead by its ID.

        Args:
            lead_id: The ID of the lead to retrieve

        Returns:
            Dict containing lead information or empty dict if not found
        """
        for lead in self.data.get("leads", []):
            if lead.get("id") == lead_id:
                return lead
        return {}

    def get_all_leads(self) -> List[Dict[str, Any]]:
        """Get all leads from the data.

        Returns:
            List of lead dictionaries
        """
        return self.data.get("leads", [])

    def get_product_info(self) -> Dict[str, Any]:
        """Get product information from the data.

        Returns:
            Dict containing product information
        """
        return self.data.get("product", {})