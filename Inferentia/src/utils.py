# src/utils.py

import os
import json
import datefinder
from .ml_models import load_ner_model
from .config import OUTPUT_DIR
from transformers import Pipeline


ner_model = None

def ensure_team_folder(team_name):
    folder = os.path.join(OUTPUT_DIR, team_name)
    os.makedirs(folder, exist_ok=True)
    return folder

def get_today_string():
    from datetime import datetime
    return datetime.today().strftime('%Y-%m-%d')

# Make sure this function is updated to accept the model as an argument
def extract_people_and_dates(task_sentence: str, ner_model: Pipeline):
    """
    Extracts people and dates from a sentence using a PRE-LOADED NER model.
    """
    if not ner_model:
        raise ValueError("NER model is not loaded or passed correctly.")
        
    persons = [e['word'] for e in ner_model(task_sentence) if e['entity_group'] == 'PER']
    dates = list(datefinder.find_dates(task_sentence))
    dates_str = [d.strftime("%Y-%m-%d") for d in dates] if dates else []
    return persons, dates_str

def print_last_meeting_snapshot(kb):
    if len(kb) < 2:
        print("\n(No previous meeting to display for context)\n")
        return
    last = kb[-2]
    print(f"\n===== Previous Meeting on {last['date']} =====")
    print("Summary:", last.get("summary", ""))
    print("Action Items:")
    for item in last.get("action_items", []):
        print(f" - {item.get('task', item)} owners: {item.get('owners',[])} | due: {item.get('due_dates',[])} [{item.get('status','')}]")
    print("Decisions:")
    for item in last.get("decisions", []):
        print(f" - {item.get('decision','')}")
    print("=" * 40)

def update_knowledge_base(team_folder, meeting_json):
    kb_path = os.path.join(team_folder, "knowledge_base.json")
    if os.path.isfile(kb_path):
        with open(kb_path, "r", encoding="utf-8") as f:
            kb = json.load(f)
    else:
        kb = []
    kb.append(meeting_json)
    kb = sorted(kb, key=lambda d: d["date"])
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2)
    return kb

def export_knowledge_base_to_csv(team_folder):
    import csv
    kb_path = os.path.join(team_folder, "knowledge_base.json")
    export_path = os.path.join(team_folder, "knowledge_base_export.csv")
    if not os.path.exists(kb_path):
        print("No knowledge base yet!")
        return
    with open(kb_path, "r", encoding="utf-8") as f:
        kb = json.load(f)
    with open(export_path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Type', 'Task/Decision', 'Owners', 'Due Dates', 'Status'])
        for entry in kb:
            date = entry['date']
            for a in entry['action_items']:
                writer.writerow([date, "Action Item", a.get("task", ""), ", ".join(a.get("owners", [])), ", ".join(a.get("due_dates", [])), a.get("status", "")])
            for d in entry['decisions']:
                writer.writerow([date, "Decision", d.get("decision", ""), "", "", d.get("status", "Finalized")])
    print(f"Exported full knowledge base to {export_path}")
