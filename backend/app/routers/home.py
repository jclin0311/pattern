from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..auth_session import current_user
from ..clock import local_today
from ..db.connection import get_db
from ..db.models import Attempt, QuizSession, User
from ..insights.dashboard_stats import streak
from ..practice.review_schedule import due_review_question_ids
from ..practice.study_plans import get_plan
from .profile import user_payload

router = APIRouter(prefix="/api", tags=["home"])


def _progress(db: Session, session: QuizSession | None) -> dict | None:
    if session is None:
        return None
    answered = db.scalar(
        select(func.count()).select_from(Attempt).where(Attempt.session_id == session.id)
    )
    correct = db.scalar(
        select(func.count())
        .select_from(Attempt)
        .where(Attempt.session_id == session.id, Attempt.is_correct.is_(True))
    )
    return {
        "session_id": session.id,
        "mode": session.mode,
        "total": len(session.question_ids),
        "answered": answered,
        "correct": correct,
    }


def _review_card(db: Session, user_id: int, plan: str, today: date, reviews: list[QuizSession]) -> dict:
    """Today's latest review set, or the questions now due if it's done (misses join the same day)."""
    latest = _progress(db, reviews[-1]) if reviews else None
    if latest and latest["answered"] < latest["total"]:
        return latest
    due = len(due_review_question_ids(db, user_id, plan, today))
    if latest and not due:
        return latest
    return {"session_id": None, "total": due, "answered": 0, "correct": 0}


@router.get("/home")
def home(user: User = Depends(current_user), db: Session = Depends(get_db)):
    today = local_today(user.timezone)
    plan = get_plan(user.plan).id
    sessions = list(
        db.scalars(
            select(QuizSession)
            .where(QuizSession.user_id == user.id, QuizSession.plan == plan, QuizSession.local_date == today)
            .order_by(QuizSession.id)
        )
    )
    daily = next((s for s in sessions if s.mode == "daily"), None)
    reviews = [s for s in sessions if s.mode == "review"]
    extras = [s for s in sessions if s.mode == "extra"]

    progress = [p for p in (_progress(db, s) for s in sessions) if p]
    unfinished = next((p for p in reversed(progress) if 0 < p["answered"] < p["total"]), None)

    return {
        "user": user_payload(user),
        "today": today.isoformat(),
        "streak": streak(db, user.id, today),
        "daily": _progress(db, daily) or {"session_id": None, "total": user.daily_goal, "answered": 0, "correct": 0},
        "review": _review_card(db, user.id, plan, today, reviews),
        "extra": [_progress(db, s) for s in extras],
        "resume": unfinished,
    }
