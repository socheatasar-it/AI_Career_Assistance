from db_query import get_career_suggestions

def retrieve_context(query, limit=4):
    matches = get_career_suggestions(query)
    if not matches:
        matches = get_career_suggestions("")
    return "\n".join(
        f"{row['title']}: {row['description']} Skills: {row['skills']}"
        for row in matches[:limit]
    )
