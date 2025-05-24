# For NLP parsing
import spacy
from typing import Optional, List, Dict
from ..models.data_models import ParsedQuery
from datetime import datetime, timedelta

# Load SpaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Downloading it...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class LLMService:
    def parse_query(self, query_text: str) -> ParsedQuery:
        """
        Parses a natural language query into a structured ParsedQuery object.
        This is a rule-based or SpaCy-based approach for simplicity.
        For more complex queries, integrate a true LLM.
        """
        doc = nlp(query_text.lower())
        parsed_data = ParsedQuery(features=[])

        # --- Extract Desk Type ---
        if "standing desk" in query_text.lower():
            parsed_data.desk_type = "standing"
        elif "regular desk" in query_text.lower() or "normal desk" in query_text.lower():
            parsed_data.desk_type = "regular"

        # --- Extract Location (Floor, Team) ---
        for token in doc:
            if token.text in ["1st", "2nd", "3rd", "4th", "5th"] and token.head.text == "floor":
                try:
                    parsed_data.location_floor = int(token.text.replace('st', '').replace('nd', '').replace('rd', '').replace('th', ''))
                except ValueError:
                    pass # Ignore if conversion fails

        # Simple keyword matching for team - can be improved with entity linking
        if "marketing team" in query_text.lower():
            parsed_data.location_team = "Marketing"
        elif "sales team" in query_text.lower():
            parsed_data.location_team = "Sales"
        elif "engineering team" in query_text.lower():
            parsed_data.location_team = "Engineering"

        # --- Extract Time Period ---
        if "tomorrow afternoon" in query_text.lower():
            # For "tomorrow afternoon", set date to tomorrow and time_period to "afternoon"
            tomorrow = datetime.now().date() + timedelta(days=1)
            parsed_data.date = tomorrow.isoformat() # YYYY-MM-DD
            parsed_data.time_period = "afternoon"
        elif "tomorrow morning" in query_text.lower():
            tomorrow = datetime.now().date() + timedelta(days=1)
            parsed_data.date = tomorrow.isoformat()
            parsed_data.time_period = "morning"
        elif "today afternoon" in query_text.lower():
            today = datetime.now().date()
            parsed_data.date = today.isoformat()
            parsed_data.time_period = "afternoon"
        # Add more date/time parsing as needed (e.g., specific dates, "next week")

        # --- Extract Features ---
        if "dual monitors" in query_text.lower() or "dual-monitors" in query_text.lower():
            parsed_data.features.append("dual-monitors")
        if "ergonomic chair" in query_text.lower() or "ergonomic-chair" in query_text.lower():
            parsed_data.features.append("ergonomic-chair")
        if "adjustable height" in query_text.lower() or "adjustable-height" in query_text.lower():
            parsed_data.features.append("adjustable-height")
        if "near window" in query_text.lower() or "near-window" in query_text.lower():
            parsed_data.features.append("near-window")
        if "quiet area" in query_text.lower() or "quiet-area" in query_text.lower():
            parsed_data.features.append("quiet-area")


        print(f"Parsed Query: {parsed_data.dict()}") # For debugging
        return parsed_data