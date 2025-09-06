# src/database.py

import motor.motor_asyncio
from beanie import Document, init_beanie
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Import the connection string from your config
from .config import MONGO_CONNECTION_STRING

# --- Pydantic Models for Embedded Documents ---
# These are not top-level documents in MongoDB, but parts of a Meeting document.
class ActionItem(BaseModel):
    task: str
    status: str
    owners: List[str]
    due_dates: List[str]

class Decision(BaseModel):
    decision: str

# --- Beanie Document Model (Represents a MongoDB Collection) ---
class Meeting(Document):
    team: str
    date: date
    summary: str
    transcript_file: str
    action_items: List[ActionItem]
    decisions: List[Decision]
    
    class Settings:
        # This is the name of the collection in your MongoDB database
        name = "summaries"

# --- Database Initialization ---
async def init_db():
    """
    Initializes the MongoDB database connection and Beanie.
    """
    # Create a Motor client for the MongoDB connection
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    
    # Get the specific database from the client. Beanie will create it if it doesn't exist.
    database = client.get_database("projectManagementDB")

    # Initialize Beanie with the database client and a list of your Document models
    await init_beanie(database=database, document_models=[Meeting])
    print(" > MongoDB database initialized with Beanie!")