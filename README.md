## Final Project: AI Career Assistant Chatbot
## 1. Project Overview
The AI Career Assistant is an AI-powered application designed to help users explore career opportunities, identify suitable career paths, and prepare for professional development. The application uses artificial intelligence to provide personalized career guidance based on users' interests, skills, experience, and career goals.

The system aims to simplify career planning by offering an interactive chatbot that answers career-related questions and helps users make informed decisions about their professional future.

## 2. Project Objectives
The main objectives of the project are:

- Provide personalized career recommendations based on users' interests and skills.
- Help users explore different career paths and job opportunities.
- Provide an interactive chatbot for answering career-related questions.
- Maintain career profiles and display useful statistics through a dashboard.
- Monitor chatbot performance, including response time and question-and-answer history.

## 3. Technology Used

- Python: Main programming language.
- Streamlit: Framework for building the interactive web application.
- OpenAI API: Provides AI-powered responses to career-related questions.
- PostgreSQL: Database for storing and managing structured application data.
- Pandas: Supports data processing and dashboard analytics.
- Python-dotenv: Loads configuration values and API credentials from environment variables.

## 4. Install dependencies (Windows PowerShell)

Streamlit chatbot using the OpenAI API with Postgre support and a local SQLite fallback.

```powershell
python -m pip install -r requirements.txt
```

## 5. Configure environment
Copy `.env.config` to `.env`, then set `OPENAI_API_KEY` to your own secret key.
Create an OpenAI API key at https://platform.openai.com/api-keys.

Do not share or commit `.env`. API usage can be billed separately from a ChatGPT subscription.

## 6. Start PostgreSQL
Option A: Install Postgre for Windows and create a database named `career_assistance`.

Option B: If Docker Desktop is installed, run:

```powershell
docker compose up -d
```

The sample Docker Compose password is only for local development. Change it before use.

Set `DATABASE_URL` in `.env`. Example:

```text
DATABASE_URL=postgresql+psycopg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/career_assistance
```

If your password contains special characters such as `@`, `:`, `/`, or `#`, URL-encode them in the connection string.

To use SQLite instead, leave `DATABASE_URL` blank and the app uses `career_assistance.db`.

## 7. Initialize and run
```powershell
python ingest.py
python -m streamlit run app.py
```

## 8. Project files
- `app.py`: Streamlit chatbot interface
- `assistant.py`: OpenAI chat integration
- `db_init.py`: database connection and table setup
- `db_query.py`, `db_save.py`, `db_feedback.py`: database operations
- `rag_helper.py`: simple career catalogue retrieval helper
- `ingest.py`, `generate_data.py`: initialize/seed career data
- `evaluation_utils.py`, `judge.py`, `metrics.py`: basic answer evaluation utilities
- `dashboard.py`: basic dashboard page
