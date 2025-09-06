# src/config.py

import os

# Teams in your org
TEAMS = ["VP", "FrontendTeam", "BackendTeam", "DatabaseTeam"]

# Model names for Hugging Face pipelines
SUMMARY_MODEL = "facebook/bart-large-cnn"
ACTION_MODEL = "google/flan-t5-base"     # <-- Stable, public model
DECISION_MODEL = "google/flan-t5-base"   # <-- Same for decisions
NER_MODEL = "dbmdz/bert-large-cased-finetuned-conll03-english"

# Base directories (Always absolute, resolves from project root!)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

MONGO_CONNECTION_STRING = os.getenv(
    "MONGO_CONNECTION_STRING", 
    "mongodb+srv://pskunder2005_db_user:prerna1234@cluster1.7bip3zx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
)
