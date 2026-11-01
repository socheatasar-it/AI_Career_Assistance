import streamlit as st
import time

from assistant import answer_question
from db_init import init_db
from db_query import get_profile_count, get_career_suggestions
from db_save import save_profile
from dashboard import show_dashboard

st.set_page_config(page_title="AI Career Assistant", page_icon="🤖", layout="wide")
init_db()

st.title("🤖 AI Career Assistant Chatbot")
st.caption("Explore career options, build skills, and save your career profile.")

with st.sidebar:
    st.header("Your career profile")
    name = st.text_input("Your Name (optional)")
    experience = st.text_area("Experience", placeholder="ex. 2 years in marketing, 5 years in software development")
    interests = st.text_area("Interests", placeholder="ex. Business, Technology, Design")
    skills = st.text_area("Current skills", placeholder="ex. Business Analysis, Python, Database, Communication")
    education = st.text_input("Education", placeholder="ex. High school, Bachelor's degree, Master's degree, etc.")
    goal = st.text_area("Career goal", placeholder="What kind of work would you like to do?")
    if st.button("Save profile", type="primary"):
        save_profile(name, experience, interests, skills, education, goal)
        st.success("Profile saved.")

tab_chat, tab_careers, tab_dashboard = st.tabs(["💬 Chat with AI", "🔎 Career suggestions", "📊 Dashboard"])

with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! Tell me about your interests, skills, or career goals, "
                    "and I'll help you explore options."
                ),
            }
        ]

    # Initialize question & answer performance history
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Get the user's question
    prompt = st.chat_input(
        "Ask about careers, skills, resumes, or interviews..."
    )

    if prompt:
        # Display and save the user's question
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate the answer and measure execution duration
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                start_time = time.perf_counter()

                reply = answer_question(
                    prompt,
                    st.session_state.messages[:-1]
                )

                duration = time.perf_counter() - start_time

            st.markdown(reply)

            st.caption(
                f"⏱️ Response time: {duration:.2f} seconds"
            )

        # Save the assistant's answer
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        # Save performance information for the dashboard
        st.session_state.qa_history.append(
            {
                "question": prompt,
                "answer": reply,
                "duration": duration,
            }
        )

with tab_careers:
    st.write("Enter a skill or interest to find matching career ideas!")
    query = st.text_input("Search careers", placeholder="ex. business, data, design, marketing, engineering")
    if st.button("Find careers"):
        rows = get_career_suggestions(query)
        if rows:
            for row in rows:
                with st.container(border=True):
                    st.subheader(row["title"])
                    st.write(row["description"])
                    st.caption("Skills: " + row["skills"])
        else:
            st.info("No matching careers found yet, please try another broader search!")

with tab_dashboard:
    show_dashboard()