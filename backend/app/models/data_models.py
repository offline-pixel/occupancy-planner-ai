# Pydantic models
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime

# --- VergeSense API Mocks ---
class Space(BaseModel):
    id: str
    name: str
    type: Literal["floor", "zone", "area"]
    capacity: int
    parent_id: Optional[str] = None

class OccupancyData(BaseModel):
    area_id: str
    timestamp: datetime
    occupancy_count: int
    occupancy_percentage: int

class ForecastDetails(BaseModel):
    morning: int
    afternoon: int
    evening: int

class AreaForecast(BaseModel):
    next_day: ForecastDetails

class OccupancyResponse(BaseModel):
    occupancy_data: List[OccupancyData]
    forecast: Dict[str, AreaForecast]

class Sensor(BaseModel):
    id: str
    type: str
    status: str
    area_id: str
    last_reading: datetime

class Metric(BaseModel):
    area_id: str
    date: str # parse to date if needed for calculation
    peak_occupancy: int
    average_occupancy: int
    utilization_rate: float

# --- Desk Inventory and Mapping Data ---
class Desk(BaseModel):
    id: str
    type: Literal["standing", "regular"]
    area_id: str
    vergesense_area_id: str
    floor: int
    zone: str
    location_description: str
    features: List[str]
    status: Literal["available", "occupied", "maintenance"]
    last_used: datetime

# --- Employee Preference Data ---
class EmployeePreference(BaseModel):
    employee_id: str
    name: str
    team: str
    desk_preferences: List[str]
    equipment_needs: List[str]
    preferred_days: List[str]
    preferred_location: str
    accessibility_needs: Optional[str]
    adjacency_preferences: List[str]

# --- Organizational Policies ---
class Policy(BaseModel):
    id: str
    name: str
    description: str
    active: bool
    enforcement_level: Literal["mandatory", "preferred"]

class DeskAssignmentRule(BaseModel):
    rule_id: str
    description: str
    priority: int

class OrganizationalPolicies(BaseModel):
    policies: List[Policy]
    desk_assignment_rules: List[DeskAssignmentRule]

# --- Query Structure (for LLM output and internal use) ---
class ParsedQuery(BaseModel):
    desk_type: Optional[str] = None
    location_floor: Optional[int] = None
    location_team: Optional[str] = None
    time_period: Optional[Literal["morning", "afternoon", "evening"]] = None
    date: Optional[str] = None
    features: List[str] = []
    employee_id: Optional[str] = None


# Add this new model for your request body
class QueryInput(BaseModel):
    query_text: str = Field(..., example="Find me an available standing desk near the marketing team on the 3rd floor for tomorrow afternoon.")