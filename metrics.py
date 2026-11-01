import time
import statistics

from dataclasses import dataclass, field
from datetime import datetime
#from rag_helper import RAGBase

@dataclass
class LLMCallRecord:
    model: str
    prompt: str
    instructions: str
    answer: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    response_time: float
    cost: float
    timestamp: datetime = field(default_factory=datetime.now)

def summarize_evaluations(results):
    results = list(results)
    if not results:
        return {"count": 0, "pass_rate": 0.0}
    passed = sum(bool(item.get("passes_basic_checks")) for item in results)
    return {"count": len(results), "pass_rate": passed / len(results)}


def measure_execution_time(function, *args, **kwargs):
    start_time = time.perf_counter()

    try:
        result = function(*args, **kwargs)
        return result, time.perf_counter() - start_time
    except Exception:
        raise


def calculate_response_metrics(records):
    durations = [
        float(record["duration"])
        for record in records
        if record.get("duration") is not None
    ]

    if not durations:
        return {
            "total_questions": len(records),
            "total_answers": 0,
            "average_duration": 0,
            "fastest_duration": 0,
            "slowest_duration": 0,
        }

    return {
        "total_questions": len(records),
        "total_answers": sum(
            bool(record.get("answer")) for record in records
        ),
        "average_duration": statistics.mean(durations),
        "fastest_duration": min(durations),
        "slowest_duration": max(durations),
    }
