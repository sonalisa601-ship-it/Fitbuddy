from __future__ import annotations

from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    user_id: str
    age: int
    weight: float
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str