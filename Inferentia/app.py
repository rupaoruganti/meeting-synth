# app.py

import os
import tempfile
from typing import List
from datetime import datetime
import traceback
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Your project's functions
from src.main import transcribe_audio
from src.ml_models import load_summarizer, load_action_extractor, load_decision_extractor, load_ner_model
from src.utils import ensure_team_folder, get_today_string, extract_people_and_dates
from src.database import init_db, Meeting, ActionItem, Decision
from app_processing import process_meeting_audio, models

# --- Application Setup ---
app = FastAPI(
    title="Meeting Summarization API (MongoDB)",
    description="An API to transcribe, process, and store meeting audio in MongoDB.",
    version="2.0.1-debug"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# --- CORSMiddleware configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Events ---
@app.on_event("startup")
async def startup_event():
    await init_db()
    print(" > Loading ML models...")
    models["summarizer"] = load_summarizer()
    models["action_extractor"] = load_action_extractor()
    models["decision_extractor"] = load_decision_extractor()
    models["ner_model"] = load_ner_model()
    print(" > Models loaded successfully!")

# --- API Endpoints ---
@app.post("/process-meeting/", tags=["Meeting Processing"])
async def process_meeting_endpoint(team: str = Form(...), audio_file: UploadFile = File(...)):
    print("\n--- Received new request for /process-meeting/ ---")
    temp_audio_path = ""
    try:
        print("✅ Checkpoint 1: Saving uploaded file to a temporary location...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as tmp:
            tmp.write(await audio_file.read())
            temp_audio_path = tmp.name
        print(f"   - File saved to: {temp_audio_path}")

        # 1. Transcribe & Process
        print("✅ Checkpoint 2: Starting audio transcription...")
        transcript = transcribe_audio(temp_audio_path)
        if not transcript:
            print("❌ ERROR: Transcription returned an empty result.")
            raise HTTPException(status_code=400, detail="Audio could not be transcribed.")
        print("   - Transcription successful.")

        print("✅ Checkpoint 3: Running ML models for summary and extraction...")
        meeting_results = process_meeting_audio(transcript)
        print("   - ML processing successful.")
        # print(f"   - Results: {meeting_results}")  # Uncomment for detailed output

        # 2. Create the Meeting document
        print("✅ Checkpoint 4: Preparing data for database insertion...")
        new_meeting = Meeting(
            team=team,
            date=datetime.strptime(meeting_results["date"], "%Y-%m-%d").date(),
            summary=meeting_results["summary"],
            transcript_file=f"{meeting_results['date']}_transcript.txt",
            action_items=[ActionItem(**item) for item in meeting_results["action_items"]],
            decisions=[Decision(**item) for item in meeting_results["decisions"]]
        )
        print("   - Meeting document created successfully.")

        # 3. Insert the document into MongoDB
        print("✅ Checkpoint 5: Inserting document into MongoDB...")
        await new_meeting.insert()
        print("   - 🎉 SUCCESS: Document inserted into the database!")

        # (Optional) Save local transcript file if needed
        team_folder = ensure_team_folder(team)
        transcript_filepath = os.path.join(team_folder, new_meeting.transcript_file)
        with open(transcript_filepath, "w", encoding="utf-8") as f:
            f.write(transcript)

        return {"message": "Meeting processed and saved to MongoDB", "meeting_id": str(new_meeting.id)}

    except Exception as e:
        print(f"❌ AN ERROR OCCURRED: {str(e)}")
        print("--- Full Error Traceback ---")
        traceback.print_exc()
        print("--------------------------")
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")

    finally:
        # Clean up the temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)
            print("🧹 Checkpoint 6: Cleaned up temporary file.")

# --- GET Endpoint ---
@app.get("/meetings/{team}", response_model=List[Meeting], tags=["Data Retrieval"])
async def get_team_meetings(team: str):
    meetings = await Meeting.find(Meeting.team == team).sort(-Meeting.date).to_list()
    if not meetings:
        raise HTTPException(status_code=404, detail=f"No meetings found for team '{team}'")
    return meetings

# --- Main Run ---
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
