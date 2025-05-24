# Core logic
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..models.data_models import ParsedQuery, Desk, EmployeePreference, Policy, OrganizationalPolicies
from .llm_service import LLMService
from .data_loader import data_loader # Singleton instance

class RecommendationService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        # Access loaded data via the singleton data_loader
        self.all_desks = data_loader.get_desks()
        self.all_spaces = data_loader.get_spaces()
        self.all_occupancy_data = data_loader.get_occupancy_data()
        self.all_employee_preferences = data_loader.get_employee_preferences()
        self.org_policies = data_loader.get_organizational_policies()

    async def find_available_desks(self, query_text: str, employee_id: Optional[str] = None) -> List[Desk]:
        """
        Parses the natural language query, filters desks by availability,
        and applies preferences/policies.
        """
        parsed_query = self.llm_service.parse_query(query_text)

        # 1. Filter by Query Parameters
        filtered_desks = self._filter_desks_by_query(parsed_query)

        # 2. Apply Real-time Occupancy Data (Mocked)
        # For "tomorrow afternoon", we'll check the forecast
        if parsed_query.date and parsed_query.time_period and parsed_query.date == (datetime.now().date() + timedelta(days=1)).isoformat():
            # Check forecast for tomorrow afternoon for relevant areas
            forecast = self.all_occupancy_data.get("forecast", {})
            available_forecast_areas = []
            for area_id, area_forecast in forecast.items():
                # Assuming forecast is percentage of occupancy
                if area_forecast.get("next_day", {}).get(parsed_query.time_period) < 70: # Arbitrary threshold for "available"
                    available_forecast_areas.append(area_id)

            # Filter desks that are in potentially available areas
            filtered_desks = [
                desk for desk in filtered_desks
                if desk.vergesense_area_id in available_forecast_areas
            ]
        else:
            # For "today" or general, use current "status" from desk inventory
            # In a real system, you'd call VergeSense API here for real-time `occupancy_count`
            filtered_desks = [desk for desk in filtered_desks if desk.status == "available"]


        # 3. Apply Organizational Policies (Mandatory)
        filtered_desks = self._apply_mandatory_policies(filtered_desks)

        # 4. Apply Employee Preferences (Optional, if employee_id is provided)
        if employee_id:
            employee_pref = next((ep for ep in self.all_employee_preferences if ep.employee_id == employee_id), None)
            if employee_pref:
                filtered_desks = self._apply_employee_preferences(filtered_desks, employee_pref)

        # 5. Sort/Rank Recommendations (Based on preferred policies or other criteria)
        # For now, a simple sort, but can be enhanced.
        filtered_desks.sort(key=lambda d: d.location_description)

        return filtered_desks

    def _filter_desks_by_query(self, query: ParsedQuery) -> List[Desk]:
        """Filters desks based on parsed query parameters."""
        desks = self.all_desks

        if query.desk_type:
            desks = [d for d in desks if d.type == query.desk_type]
        if query.location_floor:
            desks = [d for d in desks if d.floor == query.location_floor]
        if query.location_team:
            # Find relevant area_ids for the team zone
            target_zones = [
                space.id for space in self.all_spaces
                if space.type == "zone" and query.location_team.lower() in space.name.lower()
            ]
            # Then find areas within those zones
            target_areas = [
                space.id for space in self.all_spaces
                if space.type == "area" and space.parent_id in target_zones
            ]
            desks = [d for d in desks if d.area_id in target_areas or d.zone.lower() == f"{query.location_team.lower()} zone"]

        for feature in query.features:
            desks = [d for d in desks if feature in d.features]

        return desks

    def _apply_mandatory_policies(self, desks: List[Desk]) -> List[Desk]:
        """Applies mandatory organizational policies to the desks."""
        active_mandatory_policies = [
            p for p in self.org_policies.policies
            if p.active and p.enforcement_level == "mandatory"
        ]

        # Example: Desk Sanitization (POL-002) - Assuming 4 hours after last_used
        # For tomorrow afternoon, this policy might not strictly apply based on 'last_used' today
        # but for real-time query you'd check if it's currently sanitized.
        # For mock, we'll exclude desks in 'maintenance' status which might imply sanitization.
        if any(p.id == "POL-002" for p in active_mandatory_policies):
             desks = [d for d in desks if d.status != "maintenance"] # Exclude maintenance desks

        # Example: Capacity Limits (POL-005) - this would be applied at a higher level (floor/zone)
        # and would impact if *any* desk can be recommended in a full area.
        # This requires more complex logic, potentially rejecting a whole area if it exceeds capacity.
        # For now, we'll rely on the forecast filtering earlier.

        # Example: Social Distancing (POL-001) - Highly complex, needs desk adjacency data.
        # This would require knowing the physical layout of desks and current occupied desks.
        # Too complex for this prototype, but note it as a future enhancement.

        return desks

    def _apply_employee_preferences(self, desks: List[Desk], preferences: EmployeePreference) -> List[Desk]:
        """Ranks/filters desks based on employee preferences."""
        # For the prototype, let's prioritize direct matches or slightly boost them
        # In a real system, this would involve scoring and ranking.

        preferred_desks = []
        other_desks = []

        for desk in desks:
            is_preferred = False
            # Check desk preferences (e.g., standing, near-window)
            if any(p in desk.features for p in preferences.desk_preferences) or \
               any(p == desk.type for p in preferences.desk_preferences):
                is_preferred = True

            # Check equipment needs
            if all(eq in desk.features for eq in preferences.equipment_needs):
                is_preferred = True # Boost if all equipment needs are met

            # Check preferred location/team (already largely handled by initial query filter)
            # This is more for subtle nudges if multiple zones are available

            if is_preferred:
                preferred_desks.append(desk)
            else:
                other_desks.append(desk)

        # Return preferred desks first, then others. More advanced would be a weighted score.
        return preferred_desks + other_desks