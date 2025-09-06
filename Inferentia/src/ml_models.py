# src/ml_models.py

from transformers import pipeline
from .config import SUMMARY_MODEL, ACTION_MODEL, DECISION_MODEL, NER_MODEL

def load_summarizer():
    return pipeline("summarization", model=SUMMARY_MODEL)

def load_action_extractor():
    return pipeline("text2text-generation", model=ACTION_MODEL)

def load_decision_extractor():
    return pipeline("text2text-generation", model=DECISION_MODEL)

def load_ner_model():
    return pipeline("ner", model=NER_MODEL, aggregation_strategy="simple")
    