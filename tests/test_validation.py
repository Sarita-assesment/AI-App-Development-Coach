"""Small offline tests that do not call the Groq API."""

from ai_service import split_guide_into_sections
from models import AppIdeaRequest


def test_request_validation() -> None:
    request = AppIdeaRequest(
        idea="Build an expense tracker for college students.",
        app_type="Mobile App",
        experience_level="Beginner",
        preferred_technology="Let AI Decide",
    )
    assert request.app_type == "Mobile App"


def test_section_parser() -> None:
    response = """## 1. UNDERSTAND
Problem details
## 2. PLAN
Planning details
## 3. BUILD
Build details
## 4. EXPLAIN
Explanation details
## 5. LEARN
Learning details
## 6. NEXT STEPS
Next actions
"""
    sections = split_guide_into_sections(response)
    assert sections["UNDERSTAND"] == "Problem details"
    assert sections["NEXT STEPS"] == "Next actions"

