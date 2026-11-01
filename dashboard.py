import streamlit as st
import pandas as pd

from db_query import get_profile_count
from db_init import init_db
from metrics import calculate_response_metrics

st.set_page_config(page_title="Career Dashboard", page_icon="📊")
init_db()

def show_dashboard():    
    st.markdown(
        """
        <h2 style="font-size: 28px;">
            🖥️ OS Dashboard — Chatbot Performance
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write("Monitor question-and-answer execution performance.")

    # Load session history
    records = st.session_state.get("qa_history", [])

    # Calculate metrics
    metrics = calculate_response_metrics(records)

    # KPI cards
    st.subheader("📊 Performance Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Questions", metrics["total_questions"])
    col2.metric("Total Answers", metrics["total_answers"])
    col3.metric(
        "Average Response Time",
        f'{metrics["average_duration"]:.2f} sec'
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "⚡ Fastest Response",
        f'{metrics["fastest_duration"]:.2f} sec'
    )
    col5.metric(
        "🐢 Slowest Response",
        f'{metrics["slowest_duration"]:.2f} sec'
    )

    # Stop here if no history is available
    if not records:
        st.info(
            "No questions recorded yet. Ask the chatbot a question "
            "to see performance charts."
        )
        return

    # Convert history to DataFrame
    df = pd.DataFrame(records)

    # Ensure required columns exist
    if "duration" not in df.columns:
        st.warning("Response-time data is not available.")
        return

    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df = df.dropna(subset=["duration"]).copy()

    if df.empty:
        st.info("No valid response-time measurements are available yet.")
        return

    df.index = range(1, len(df) + 1)
    df.index.name = "Request #"

    # Chart 1: Line chart
    st.subheader("📈 Response Time Trend")

    line_df = df[["duration"]].rename(
        columns={"duration": "Response Time (seconds)"}
    )

    st.line_chart(line_df)

    # Chart 2: Bar chart
    st.subheader("📊 Response Time by Question")

    bar_df = df[["duration"]].rename(
        columns={"duration": "Response Time (seconds)"}
    )

    st.bar_chart(bar_df)

    # Chart 3: Answer status pie chart
    st.subheader("🥧 Answer Status")

    if "answer" in df.columns:
        answered = int(
            df["answer"].fillna("").astype(str).str.strip().ne("").sum()
        )
        unanswered = len(df) - answered

        status_df = pd.DataFrame(
            {
                "Status": ["Answered", "Unanswered"],
                "Count": [answered, unanswered]
            }
        )

        st.vega_lite_chart(
            status_df,
            {
                "mark": {"type": "arc", "innerRadius": 50},
                "encoding": {
                    "theta": {
                        "field": "Count",
                        "type": "quantitative"
                    },
                    "color": {
                        "field": "Status",
                        "type": "nominal"
                    },
                    "tooltip": [
                        {"field": "Status", "type": "nominal"},
                        {"field": "Count", "type": "quantitative"}
                    ]
                },
                "view": {"stroke": None}
            },
            use_container_width=True
        )

    # Chart 4: Response-time distribution
    st.subheader("⏱️ Response Time Distribution")

    st.bar_chart(
        df["duration"].value_counts(
            bins=5, sort=False
        ).sort_index(),
        x_label="Response Time Range",
        y_label="Number of Questions"
    )

    # Execution history table
    st.subheader("📋 Question & Answer Execution History")

    display_df = df.reset_index()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Download history
    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Execution History (CSV)",
        data=csv_data,
        file_name="chatbot_execution_history.csv",
        mime="text/csv"
    )