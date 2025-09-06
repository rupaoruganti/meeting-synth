# app_processing.py

from typing import Dict, Any

# Import your ML extraction functions
from src.main import extract_summary, extract_action_items, extract_decisions
from src.utils import get_today_string, extract_people_and_dates

# This dictionary will be populated at startup by app.py
models = {}

def process_meeting_audio(transcript: str) -> Dict[str, Any]:
    """
    Runs the full ML pipeline on a given transcript.
    This is synchronous code that will be called by the async API endpoint.
    """
    summary = extract_summary(models["summarizer"], transcript)
    raw_action_items = extract_action_items(models["action_extractor"], transcript)
    decisions = extract_decisions(models["decision_extractor"], transcript)

    enriched_action_items = []
    for item in raw_action_items:
        task_sentence = item.get("task", "")
        owners, due_dates = extract_people_and_dates(task_sentence, ner_model=models["ner_model"])
        item["owners"] = owners
        item["due_dates"] = due_dates
        if "status" not in item:
            item["status"] = "Confirmed"
        enriched_action_items.append(item)

    return {
        "date": get_today_string(),
        "summary": summary,
        "action_items": enriched_action_items,
        "decisions": decisions
    }