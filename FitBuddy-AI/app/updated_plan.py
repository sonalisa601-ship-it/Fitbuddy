from __future__ import annotations


def update_workout_plan(
    original_plan: str,
    feedback: str,
) -> str:

    return (
        f"{original_plan}\n\n"
        f"Updated based on your feedback:\n"
        f"{feedback}\n\n"
        "Please adjust the workout gradually "
        "and focus on proper form and recovery."
    )