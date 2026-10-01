# AI App Development Coach

A Round 1 prototype that converts an app idea into a guided development journey:

**Prompt → Understand → Plan → Build → Explain → Learn**

The user describes an application, selects an app type, experience level and
preferred technology, and receives an AI-generated MVP plan, architecture,
starter code, explanations and a learning roadmap.

## Features

- Validates the app idea with Pydantic.
- Generates a six-stage development guide.
- Adapts explanations to the user's experience level.
- Displays results in separate Streamlit tabs.
- Allows the guide to be downloaded as a Markdown file.
- Keeps the Groq API key outside the source code.

## Technologies Used

- Python
- Streamlit
- Groq API
- `openai/gpt-oss-120b`
- Pydantic
- python-dotenv
- Git and GitHub
- Streamlit Community Cloud

## Project Structure

```text
AI_App_Development_Coach/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── tests/
│   └── test_validation.py
├── .env.example
├── .gitignore
├── ai_service.py
├── app.py
├── models.py
├── prompts.py
├── pytest.ini
├── README.md
└── requirements.txt
```

## Step 1: Install Python

Install Python 3.10 or newer. Confirm it is available:

```bash
python --version
```

## Step 2: Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Step 3: Install the Requirements

```bash
pip install -r requirements.txt
```

## Step 4: Add the Groq API Key

1. Create a Groq API key in GroqCloud.
2. Make a copy of `.env.example`.
3. Rename the copy to `.env`.
4. Replace `your_groq_api_key_here` with the actual key.

Never upload `.env` to GitHub.

## Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, normally at:

```text
http://localhost:8501
```

## Step 6: Run the Offline Tests

```bash
pytest -q
```

These tests validate the user-input model and section parser without using API
credits.

## Example Input

```text
I want to build a personal expense-tracking mobile app for college students.
Users should record expenses, select categories, set monthly budgets and view
monthly spending reports.
```

## Deploy on Streamlit Community Cloud

1. Upload the project to a public or private GitHub repository.
2. Open Streamlit Community Cloud and create a new app.
3. Select the repository and set the main file to `app.py`.
4. Open the app settings and add this secret:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

5. Deploy the application.

## Round 1 Submission Description

AI App Development Coach is an AI-powered prototype that helps users convert an
application idea into a practical learning and development roadmap. Instead of
only generating code, it guides users through understanding requirements,
planning an MVP, building the architecture and starter code, understanding how
the components work, and learning the required concepts.

## AI Usage Disclosure

AI tools were used to assist with planning, code generation, explanations and
learning guidance. The prototype was integrated, reviewed and tested by the
developer. Generated code should be reviewed and tested before production use.
