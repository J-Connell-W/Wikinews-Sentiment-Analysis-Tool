from fastapi import FastAPI
from pydantic import BaseModel


class Story(BaseModel):
    id: str
    original_language: str
    translation_language: str
    summarization: bool
    visualization: bool


class NoTranslationStory(BaseModel):
    id: str
    original_language: str
    summarization: bool
    visualization: bool
