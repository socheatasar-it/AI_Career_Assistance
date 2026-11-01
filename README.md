## Final Project: AI Career Assistant Chatbot
The Streamlit chatbot using the OpenAI API with Postgre support and a local SQLite fallback.

## 1. Install dependencies (Windows PowerShell)
```powershell
python -m pip install -r requirements.txt
```

## 2. Configure environment
Copy `.env.config` to `.env`, then set `OPENAI_API_KEY` to your own secret key.
Create an OpenAI API key at https://platform.openai.com/api-keys.

Do not share or commit `.env`. API usage can be billed separately from a ChatGPT subscription.

## 3. Start PostgreSQL
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

## 4. Initialize and run
```powershell
python ingest.py
python -m streamlit run app.py
```

## Project files
- `app.py`: Streamlit chatbot interface
- `assistant.py`: OpenAI chat integration
- `db_init.py`: database connection and table setup
- `db_query.py`, `db_save.py`, `db_feedback.py`: database operations
- `rag_helper.py`: simple career catalogue retrieval helper
- `ingest.py`, `generate_data.py`: initialize/seed career data
- `evaluation_utils.py`, `judge.py`, `metrics.py`: basic answer evaluation utilities
- `dashboard.py`: basic dashboard page
