# src/main.py

import os
import json
from faster_whisper import WhisperModel
from .ml_models import load_summarizer, load_action_extractor, load_decision_extractor
from .utils import (
    ensure_team_folder, get_today_string, extract_people_and_dates, print_last_meeting_snapshot,
    update_knowledge_base, export_knowledge_base_to_csv
)
from .config import TEAMS

def transcribe_audio(audio_path):
    print("> Transcribing audio (Faster Whisper)...")
    model = WhisperModel("base", device="cpu")
    segments, _ = model.transcribe(audio_path)
    transcript = " ".join(segment.text for segment in segments).strip()
    return transcript

def extract_summary(summarizer, transcript):
    print("> Extracting summary (BART)...")
    return summarizer(transcript, max_length=120, min_length=40, do_sample=False)[0]["summary_text"]

def extract_action_items(action_extractor, transcript):
    """Extracts action items and safely parses the model's string output into JSON."""
    print("> Extracting action items (Flan-T5)...")
    prompt = (
        "Extract all action items from the transcript. Respond with ONLY a valid JSON list of objects, where each object has one key: 'task'. For example: [{\"task\": \"Send the report\"}, {\"task\": \"Update the slides\"}]\n"
        f"Transcript: {transcript}\nJSON Action Items:"
    )
    
    try:
        # The model returns a string that looks like a list of dicts
        result_string = action_extractor(prompt, max_length=200)[0]["generated_text"]
        
        # Clean and parse the string into a Python list
        action_items = json.loads(result_string)
        return action_items
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Warning: Could not parse action items from model output. Error: {e}")
        return []

def extract_decisions(decision_extractor, transcript):
    print("> Extracting decisions (Flan-T5)...")
    prompt = (
        "List all clear decisions made in this meeting transcript, one per line and be explicit. If none, say 'None.' Decisions:"
        f"\n{transcript}\nDecisions:"
    )
    results = decision_extractor(prompt, max_length=256, do_sample=False)[0]["generated_text"]
    lines = [line.strip('- ').strip() for line in results.split('\n') if line.strip() and 'none' not in line.lower()]
    items = [{"decision": line} for line in lines]
    return items

def main():
    print("Available teams:", TEAMS)
    team = input("Enter the team name: ").strip()
    while team not in TEAMS:
        print("Invalid team! Please pick from:", TEAMS)
        team = input("Enter the team name: ").strip()
    team_folder = ensure_team_folder(team)

    audio_path = input("Enter the path to the .mp3 file: ").strip()
    while not os.path.isfile(audio_path) or not audio_path.lower().endswith(".mp3"):
        print("Invalid .mp3 file path!")
        audio_path = input("Enter path to the .mp3 file: ").strip()

    today = get_today_string()
    transcript = transcribe_audio(audio_path)
    transcript_file = os.path.join(team_folder, f"{today}_transcript.txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Transcript saved at: {transcript_file}")

    summarizer = load_summarizer()
    action_extractor = load_action_extractor()
    decision_extractor = load_decision_extractor()

    summary = extract_summary(summarizer, transcript)
    action_items = extract_action_items(action_extractor, transcript)
    decisions = extract_decisions(decision_extractor, transcript)
    meeting_json = {
        "date": today,
        "transcript_file": os.path.basename(transcript_file),
        "summary": summary,
        "action_items": action_items,
        "decisions": decisions
    }
    json_file = os.path.join(team_folder, f"{today}_meeting.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(meeting_json, f, ensure_ascii=False, indent=2)
    print(f"Meeting JSON saved at: {json_file}")

    kb = update_knowledge_base(team_folder, meeting_json)

    print_last_meeting_snapshot(kb)
    print("\n===== Current Meeting Summary =====")
    print("Summary:", summary)
    print("Action Items:")
    for item in action_items:
        print(f" - {item['task']} owners: {item.get('owners',[])} | due: {item.get('due_dates',[])} [{item['status']}]")
    print("Decisions:")
    for item in decisions:
        print(f" - {item['decision']}")

    # Export for UI/CSV
    export_knowledge_base_to_csv(team_folder)
    print(f"\nAll files saved and knowledge base updated in: {team_folder}\n")

if __name__ == "__main__":
    main()
