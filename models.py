"""Pydantic models used to validate information entered by the user."""

from pydantic import BaseModel, Field


class AppIdeaRequest(BaseModel):
    """Validated details required to generate an app-development guide."""

    idea: str = Field(
        min_length=20,
        max_length=4000,
        description="The application idea written by the user.",
    )
    app_type: str
    experience_level: str
    preferred_technology: str


class GeneratedGuide(BaseModel):
    """The generated guide and the model that produced it."""

    content: str
    model: str

