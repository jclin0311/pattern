"""Daily practice and Ebbinghaus-style review scheduling. Deterministic, no LLM."""

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import clock
from ..db.models import Question, ReviewItem

# A question missed the first time it is seen, on day d, is reviewed on d+1, d+2, d+4, d+7,
# d+15 and d+30. A question answered correctly at first sight is never reviewed.
REVIEW_OFFSETS = (1, 2, 4, 7, 15, 30)
# Every miss, in any session, is also reviewed again the same day. One reusable item per
# question holds that, reopened on each miss.
SAME_DAY_STAGE = -1


def schedule_reviews(db: Session, user_id: int, plan: str, question_id: int, solved_on: date) -> None:
    """Create the review cycle for a question missed at first sight in a plan. No-op afterwards."""
    exists = db.scalar(
        select(ReviewItem.id).where(
            ReviewItem.user_id == user_id,
            ReviewItem.plan == plan,
            ReviewItem.question_id == question_id,
            ReviewItem.stage >= 0,
        )
    )
    if exists:
        return
    for stage, offset in enumerate(REVIEW_OFFSETS):
        db.add(
            ReviewItem(
                user_id=user_id,
                plan=plan,
                question_id=question_id,
                stage=stage,
                due_date=solved_on + timedelta(days=offset),
            )
        )


def due_review_question_ids(db: Session, user_id: int, plan: str, today: date) -> list[int]:
    """Questions with at least one incomplete review due today or earlier (missed days roll over)."""
    rows = db.execute(
        select(ReviewItem.question_id, ReviewItem.due_date)
        .join(Question, Question.id == ReviewItem.question_id)
        .where(
            Question.status == "published",  # retired questions leave the review queue
            ReviewItem.user_id == user_id,
            ReviewItem.plan == plan,
            ReviewItem.due_date <= today,
            ReviewItem.completed_at.is_(None),
        )
        .order_by(ReviewItem.due_date, ReviewItem.question_id)
    ).all()
    seen: dict[int, None] = {}
    for qid, _ in rows:
        seen.setdefault(qid, None)
    return list(seen)


def complete_due_reviews(db: Session, user_id: int, plan: str, question_id: int, today: date) -> None:
    """Answering a review clears every stage of that question that is already due."""
    items = db.scalars(
        select(ReviewItem).where(
            ReviewItem.user_id == user_id,
            ReviewItem.plan == plan,
            ReviewItem.question_id == question_id,
            ReviewItem.due_date <= today,
            ReviewItem.completed_at.is_(None),
        )
    )
    for item in items:
        item.completed_at = clock.now()


def review_again_today(db: Session, user_id: int, plan: str, question_id: int, today: date) -> None:
    """A missed question is due for review again today, whichever session it was missed in."""
    item = db.scalar(
        select(ReviewItem).where(
            ReviewItem.user_id == user_id,
            ReviewItem.plan == plan,
            ReviewItem.question_id == question_id,
            ReviewItem.stage == SAME_DAY_STAGE,
        )
    )
    if item is None:
        db.add(ReviewItem(user_id=user_id, plan=plan, question_id=question_id, stage=SAME_DAY_STAGE, due_date=today))
    else:
        item.due_date, item.completed_at = today, None
