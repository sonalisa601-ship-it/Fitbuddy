from __future__ import annotations

from datetime import datetime
from pathlib import Path

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = "sqlite:///" + str(BASE_DIR / "fitbuddy.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(120)
    )

    age: Mapped[int] = mapped_column(
        Integer
    )

    weight: Mapped[float] = mapped_column(
        Float
    )

    goal: Mapped[str] = mapped_column(
        String(80)
    )

    intensity: Mapped[str] = mapped_column(
        String(20)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(80),
        index=True,
    )

    original_plan: Mapped[str] = mapped_column(
        Text
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def save_user(
    user_id: str,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> User:

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user:

            user.username = username
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity

        else:

            user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
            )

            db.add(user)

        db.commit()
        db.refresh(user)

        return user


def save_plan(
    user_id: str,
    original_plan: str,
    nutrition_tip: str,
) -> Plan:

    with SessionLocal() as db:

        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .first()
        )

        if plan:

            plan.original_plan = original_plan
            plan.updated_plan = None
            plan.feedback = None
            plan.nutrition_tip = nutrition_tip
            plan.updated_at = None

        else:

            plan = Plan(
                user_id=user_id,
                original_plan=original_plan,
                nutrition_tip=nutrition_tip,
            )

            db.add(plan)

        db.commit()
        db.refresh(plan)

        return plan


def update_plan(
    user_id: str,
    updated_plan: str,
    feedback: str,
    nutrition_tip: str | None = None,
) -> Plan | None:

    with SessionLocal() as db:

        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .first()
        )

        if not plan:
            return None

        plan.updated_plan = updated_plan
        plan.feedback = feedback
        plan.updated_at = datetime.utcnow()

        if nutrition_tip:
            plan.nutrition_tip = nutrition_tip

        db.commit()
        db.refresh(plan)

        return plan


def get_user(user_id: str) -> User | None:

    with SessionLocal() as db:

        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )


def get_plan(user_id: str) -> Plan | None:

    with SessionLocal() as db:

        return (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .first()
        )


def get_original_plan(user_id: str) -> str | None:

    plan = get_plan(user_id)

    if plan:
        return plan.original_plan

    return None


def get_all_users() -> list[User]:

    with SessionLocal() as db:

        return (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )


def get_all_plans() -> list[Plan]:

    with SessionLocal() as db:

        return (
            db.query(Plan)
            .order_by(Plan.created_at.desc())
            .all()
        )


def delete_user(user_id: str) -> bool:

    with SessionLocal() as db:

        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .first()
        )

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            return False

        if plan:
            db.delete(plan)

        db.delete(user)

        db.commit()

        return True