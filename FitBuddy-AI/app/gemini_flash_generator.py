from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv()


TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-3.8-flash",
)

ALLOW_DEMO_FALLBACK = (
    os.getenv(
        "ALLOW_DEMO_FALLBACK",
        "true",
    ).lower()
    == "true"
)


def demo_tip(goal: str) -> str:

    goal_lower = goal.lower()

    if (
        "muscle" in goal_lower
        or "gain" in goal_lower
    ):

        return (
            "Nutrition tip: Include a protein-rich "
            "food in each main meal, such as eggs, "
            "fish, chicken, beans, tofu, or Greek "
            "yogurt. Stay hydrated to support "
            "training recovery."
        )

    if (
        "loss" in goal_lower
        or "fat" in goal_lower
    ):

        return (
            "Nutrition tip: Build meals around "
            "vegetables or fruit, a protein source, "
            "and sensible portions of whole-food "
            "carbohydrates. Hydrate regularly and "
            "avoid crash diets."
        )

    return (
        "Recovery tip: Prioritize regular hydration, "
        "balanced meals, adequate protein, and "
        "consistent sleep. These basics support "
        "energy and recovery across many fitness goals."
    )


def generate_nutrition_tip_with_flash(
    goal: str,
) -> str:

    prompt = f"""
Give one concise, practical nutrition or recovery
tip for a person whose fitness goal is:

{goal}

Requirements:

• Under 80 words.
• Practical and easy to follow.
• General wellness guidance.
• Do not diagnose conditions.
• Do not prescribe medical treatment.
"""

    api_key = os.getenv(
        "GEMINI_API_KEY",
        "",
    ).strip()

    if not api_key:

        if ALLOW_DEMO_FALLBACK:
            return demo_tip(goal)

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    try:

        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        response = client.models.generate_content(
            model=TIP_MODEL,
            contents=prompt,
        )

        text = (
            response.text
            if response.text
            else ""
        ).strip()

        if not text:
            raise RuntimeError(
                "Gemini returned an empty nutrition tip."
            )

        return text

    except Exception:

        if ALLOW_DEMO_FALLBACK:
            return demo_tip(goal)

        raise