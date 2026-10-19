"""Topic mastery: smoothed accuracy per topic over every answer, recent ones weighted a little more."""

from collections import defaultdict

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .. import clock
from ..db.models import Attempt, QuestionTopic, UserTopicMastery

DECAY = 0.98  # weight multiplier per older attempt: 50 answers back still counts about a third
READY_MASTERY = 0.65
READY_ATTEMPTS = 3


def compute_mastery(outcomes_newest_first: list[bool]) -> tuple[float, float]:
    """Return (mastery, confidence) for a topic.

    mastery is a Beta(1,1)-smoothed accuracy over every answer, gently weighted
    toward recent ones, so a single lucky answer does not read as mastery.
    confidence grows with evidence.
    """
    weight_sum = 0.0
    correct_sum = 0.0
    for i, ok in enumerate(outcomes_newest_first):
        w = DECAY**i
        weight_sum += w
        correct_sum += w * ok
    mastery = (correct_sum + 1) / (weight_sum + 2)
    n = len(outcomes_newest_first)
    confidence = n / (n + 5)
    return round(mastery, 4), round(confidence, 4)


def recompute_user_mastery(db: Session, user_id: int) -> None:
    rows = db.execute(
        select(QuestionTopic.topic_id, Attempt.is_correct)
        .join(QuestionTopic, QuestionTopic.question_id == Attempt.question_id)
        .where(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc(), Attempt.id.desc())
    ).all()
    by_topic: dict[str, list[bool]] = defaultdict(list)
    for topic_id, ok in rows:
        by_topic[topic_id].append(bool(ok))

    db.execute(delete(UserTopicMastery).where(UserTopicMastery.user_id == user_id))
    for topic_id, outcomes in by_topic.items():
        mastery, confidence = compute_mastery(outcomes)
        db.add(
            UserTopicMastery(
                user_id=user_id,
                topic_id=topic_id,
                attempts=len(outcomes),
                correct=sum(outcomes),
                mastery=mastery,
                confidence=confidence,
                updated_at=clock.now(),
            )
        )
    db.commit()


def mastery_map(db: Session, user_id: int) -> dict[str, UserTopicMastery]:
    return {
        m.topic_id: m
        for m in db.scalars(select(UserTopicMastery).where(UserTopicMastery.user_id == user_id))
    }
