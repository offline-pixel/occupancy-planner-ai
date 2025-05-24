# For loading mock data
import json
from pathlib import Path
from typing import List, Dict
from ..models.data_models import (
    Space, OccupancyData, Sensor, Metric, Desk, EmployeePreference,
    OrganizationalPolicies, Policy, DeskAssignmentRule, AreaForecast, ForecastDetails
)

DATA_DIR = Path(__file__).parent.parent.parent / "data"

class DataLoader:
    _instance = None
    _data = {} # Cache

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._load_all_data() # Load only once
        return cls._instance

    def _load_json(self, filename: str):
        filepath = DATA_DIR / filename
        with open(filepath, 'r') as f:
            return json.load(f)

    def _load_all_data(self):
        print(f"Loading data from: {DATA_DIR}")
        self._data["spaces"] = [Space(**s) for s in self._load_json("verge_spaces.json")["spaces"]]
        self._data["occupancy"] = self._load_json("verge_occupancy.json")
        self._data["sensors"] = [Sensor(**s) for s in self._load_json("verge_sensors.json")["sensors"]]
        self._data["metrics"] = [Metric(**m) for m in self._load_json("verge_metrics.json")["metrics"]]
        self._data["desks"] = [Desk(**d) for d in self._load_json("desk_inventory.json")["desks"]]
        self._data["employee_preferences"] = [
            EmployeePreference(**ep) for ep in self._load_json("employee_preferences.json")["employee_preferences"]
        ]
        self._data["organizational_policies"] = OrganizationalPolicies(
            **self._load_json("organizational_policies.json")
        )
        print("All mock data loaded successfully.")

    def get_spaces(self) -> List[Space]:
        return self._data["spaces"]

    def get_occupancy_data(self) -> Dict:
        return self._data["occupancy"]

    def get_sensors(self) -> List[Sensor]:
        return self._data["sensors"]

    def get_metrics(self) -> List[Metric]:
        return self._data["metrics"]

    def get_desks(self) -> List[Desk]:
        return self._data["desks"]

    def get_employee_preferences(self) -> List[EmployeePreference]:
        return self._data["employee_preferences"]

    def get_organizational_policies(self) -> OrganizationalPolicies:
        return self._data["organizational_policies"]

# Instantiate the loader once
data_loader = DataLoader()