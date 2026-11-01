import os
from dotenv import load_dotenv
#from openai import OpenAI

#from ingest import load_faq_data, build_index
#from rag_helper import RAGBase

load_dotenv()

SYSTEM_PROMPT = """You are a supportive AI career assistant. Give practical, realistic guidance
about career exploration, education, skill development, resumes, and interviews. Ask clarifying
questions when useful. Do not promise employment or invent qualifications. Keep advice actionable."""


def answer_question(question, history=None):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your_actual_openai_api_key_here":
        return ("OpenAI API key is not configured yet. Add OPENAI_API_KEY to your .env file. "
                "Meanwhile, tell me your interests and current skills and I can help you plan locally.")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for item in (history or [])[-10:]:
            if item.get("role") in ("user", "assistant"):
                messages.append({"role": item["role"], "content": item.get("content", "")})
        messages.append({"role": "user", "content": question})
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages=messages,
            temperature=0.5,
        )
        return response.choices[0].message.content or "Sorry, I couldn't generate a response."
    except Exception as exc:
        return f"I couldn't reach the OpenAI API. Check your API key, model name, and API billing. Details: {exc}"
