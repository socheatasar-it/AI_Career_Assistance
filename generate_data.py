from db_init import init_db
from db_query import get_career_suggestions

if __name__ == "__main__":
    init_db()
    print(f"Career records available: {len(get_career_suggestions(''))}")
