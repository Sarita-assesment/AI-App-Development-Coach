"""Groq API integration and response parsing."""

import re
from typing import Dict

from groq import Groq

from models import AppIdeaRequest, GeneratedGuide
from prompts import SYSTEM_PROMPT, build_user_prompt


MODEL_NAME = "openai/gpt-oss-120b"

SECTION_NAMES = (
    "UNDERSTAND",
    "PLAN",
    "BUILD",
    "EXPLAIN",
    "LEARN",
    "NEXT STEPS",
)


def generate_guide(api_key: str, request: AppIdeaRequest) -> GeneratedGuide:
    """Call Groq and return the generated app-development guide."""

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(request)},
        ],
        temperature=0.35,
        max_completion_tokens=5000,
        top_p=1,
        stream=False,
    )

    content = completion.choices[0].message.content
    if not content or not content.strip():
        raise RuntimeError("The AI returned an empty response. Please try again.")

    return GeneratedGuide(content=content.strip(), model=MODEL_NAME)


def split_guide_into_sections(content: str) -> Dict[str, str]:
    """Split the model's Markdown response into the six display tabs."""

    sections = {name: "" for name in SECTION_NAMES}
    heading_pattern = re.compile(
        r"^##\s*(?:\d+\.)?\s*(UNDERSTAND|PLAN|BUILD|EXPLAIN|LEARN|NEXT STEPS)\s*$",
        flags=re.IGNORECASE | re.MULTILINE,
    )
    matches = list(heading_pattern.finditer(content))

    if not matches:
        sections["UNDERSTAND"] = content
        return sections

    for index, match in enumerate(matches):
        section_name = match.group(1).upper()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections[section_name] = content[start:end].strip()

    return sections

