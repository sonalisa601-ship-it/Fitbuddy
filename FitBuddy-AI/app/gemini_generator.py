from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.7-flash",
)


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    prompt = f"""
Create a general fitness workout plan.

User:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
- Give a practical weekly workout plan.
- Include warm-up and cool-down.
- Include exercises, sets, reps, and rest.
- Keep the guidance general and safe.
- Do not diagnose medical conditions.
- Do not prescribe medical treatment.
- Keep the response easy to read.
"""

    api_key = os.getenv(
        "GEMINI_API_KEY",
        "",
    ).strip()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    from google import genai

    client = genai.Client(
        api_key=api_key
    )
    import time

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=WORKOUT_MODEL,
                contents=prompt,
            )
            break

        except Exception as e:
            print(f"GEMINI ERROR - Attempt {attempt + 1}:", repr(e))

            if attempt == 2:
                raise

            time.sleep(3)

    text = (
        response.text
        if response.text
        else ""
    ).strip()

    if not text:
        raise RuntimeError(
            "Gemini returned an empty workout plan."
        )

    return text