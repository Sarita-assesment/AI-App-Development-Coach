"""Streamlit user interface for the AI App Development Coach."""

import os

import streamlit as st
from dotenv import load_dotenv
from pydantic import ValidationError

from ai_service import MODEL_NAME, generate_guide, split_guide_into_sections
from models import AppIdeaRequest


load_dotenv()

st.set_page_config(
    page_title="AI App Development Coach",
    page_icon="🚀",
    layout="wide",
)


def get_api_key() -> str:
    """Read the API key locally or from Streamlit Community Cloud secrets."""

    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
    except (FileNotFoundError, KeyError):
        secret_key = ""
    return secret_key or os.getenv("GROQ_API_KEY", "")


def reset_result() -> None:
    """Remove the previous guide when the user requests a reset."""

    st.session_state.pop("guide", None)
    st.session_state.pop("request", None)


st.title("🚀 AI App Development Coach")
st.caption("Turn an application idea into a plan, starter build and learning roadmap.")

with st.sidebar:
    st.header("How it works")
    st.markdown(
        """
        1. Describe your app idea.
        2. Select your preferences.
        3. Generate the guide.
        4. Study each development stage.
        """
    )
    st.info(f"AI model: `{MODEL_NAME}`")
    st.button("Start again", on_click=reset_result, use_container_width=True)

with st.form("app_idea_form"):
    idea = st.text_area(
        "Describe the application you want to build",
        height=170,
        placeholder=(
            "Example: I want to build a personal expense-tracking mobile app "
            "for college students. Users should record expenses, select "
            "categories, set budgets and view monthly reports."
        ),
    )

    column_one, column_two, column_three = st.columns(3)
    with column_one:
        app_type = st.selectbox(
            "Application type",
            ("Web App", "Mobile App", "Desktop App", "AI Agent", "Let AI Decide"),
        )
    with column_two:
        experience_level = st.selectbox(
            "Your experience level",
            ("Beginner", "Intermediate", "Advanced"),
        )
    with column_three:
        preferred_technology = st.selectbox(
            "Preferred technology",
            ("Let AI Decide", "Python", "React", "Flutter", "Java / Spring Boot"),
        )

    submitted = st.form_submit_button(
        "Generate Development Guide",
        type="primary",
        use_container_width=True,
    )

if submitted:
    api_key = get_api_key()
    if not api_key:
        st.error(
            "GROQ_API_KEY is missing. Add it to your local .env file or to "
            "Streamlit Community Cloud secrets."
        )
    else:
        try:
            request = AppIdeaRequest(
                idea=idea.strip(),
                app_type=app_type,
                experience_level=experience_level,
                preferred_technology=preferred_technology,
            )
            with st.spinner("Understanding your idea and preparing the guide..."):
                guide = generate_guide(api_key, request)
            st.session_state["guide"] = guide
            st.session_state["request"] = request
            st.success("Your app-development guide is ready.")
        except ValidationError:
            st.warning("Please describe your app idea using at least 20 characters.")
        except Exception as error:
            st.error(f"The guide could not be generated: {error}")

if "guide" in st.session_state:
    guide = st.session_state["guide"]
    request = st.session_state["request"]
    sections = split_guide_into_sections(guide.content)

    st.divider()
    st.subheader("Your AI-generated development guide")
    st.write(f"**Idea:** {request.idea}")

    labels = ("Understand", "Plan", "Build", "Explain", "Learn", "Next Steps")
    tabs = st.tabs(labels)
    for tab, section_name in zip(tabs, sections):
        with tab:
            section_content = sections[section_name]
            if section_content:
                st.markdown(section_content)
            else:
                st.info("This section was not returned. Generate the guide again.")

    report = f"# AI App Development Guide\n\n**App idea:** {request.idea}\n\n{guide.content}"
    st.download_button(
        "Download Guide as Markdown",
        data=report,
        file_name="ai_app_development_guide.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.divider()
st.caption(
    "This prototype assists with planning, starter code and learning. "
    "Review and test generated code before using it in a real application."
)

