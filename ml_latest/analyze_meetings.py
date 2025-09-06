import os
import sys
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"

PROMPT_TEMPLATE = """
You are a meeting assistant. Extract precise, structured bullet-point insights from the transcript.

Return only valid JSON with exactly three arrays: "summary", "open_tasks", and "completed_tasks".
Each array should be a list of strings starting with "- ".

Transcript:
{transcript}
"""

def analyze(transcript: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(PROMPT_TEMPLATE.format(transcript=transcript))

    if not response.candidates:
        raise ValueError("API returned no content.")
    
    try:
        content = response.candidates[0].content.parts[0].text.strip()
    except (IndexError, AttributeError):
        raise ValueError("API returned malformed content.")
    
    if not content:
        raise ValueError("API returned an empty response.")
        
    # Strip markdown code block tags if they exist
    if content.startswith("```json") and content.endswith("```"):
        json_string = content[len("```json"):-len("```")].strip()
    else:
        json_string = content
        
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}\n\nResponse:\n{json_string}")

def main_individual(input_filename):
    # (This is the code you already have for single file analysis)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    input_path = os.path.join(INPUT_DIR, input_filename)

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    try:
        analysis = analyze(text)
        out_path = os.path.join(OUTPUT_DIR, input_filename.replace(".txt", "_analysis.json"))
        
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved analysis to: {out_path}")
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
        
    except ValueError as ve:
        print(f"❌ Error analyzing {input_filename}: {ve}")

def main_combined():
    # (This is the combined tasks code I provided earlier)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_open_tasks = []
    all_completed_tasks = []

    input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.txt')]
    print(f"Found {len(input_files)} meeting files to process.")

    for input_filename in input_files:
        input_path = os.path.join(INPUT_DIR, input_filename)
        
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        try:
            analysis = analyze(text)
            all_open_tasks.extend(analysis.get("open_tasks", []))
            all_completed_tasks.extend(analysis.get("completed_tasks", []))
            print(f"✅ Successfully analyzed {input_filename}")
        except ValueError as ve:
            print(f"❌ Error analyzing {input_filename}: {ve}")
    
    combined_tasks = {
        "open_tasks": all_open_tasks,
        "completed_tasks": all_completed_tasks
    }
    
    out_path = os.path.join(OUTPUT_DIR, "all_meetings_tasks.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined_tasks, f, ensure_ascii=False, indent=2)

    print("\n---")
    print(f"✅ Saved combined tasks to: {out_path}")
    print(json.dumps(combined_tasks, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'all':
        main_combined()
    elif len(sys.argv) > 1:
        main_individual(sys.argv[1])
    else:
        print("Usage:")
        print("  - To analyze a single meeting: python analyze_meetings.py <input_file.txt>")
        print("  - To analyze all meetings: python analyze_meetings.py all")