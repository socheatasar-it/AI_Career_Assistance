def basic_answer_checks(answer):
    text = (answer or "").strip()
    return {
        "non_empty": bool(text),
        "length_chars": len(text),
        "contains_next_step": any(word in text.lower() for word in ("next step", "try", "practice", "start by")),
    }
