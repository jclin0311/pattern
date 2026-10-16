from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from ..db.models import Attempt, Choice, Question, QuestionTopic, Topic, TopicEdge, UserTopicMastery
from ..services.mastery import recompute_user_mastery
from . import schema
from .bank import QUESTIONS, validate_bank
from .topics import EDGES, TOPICS


def seed(db: Session, questions: Sequence[schema.Question] = QUESTIONS) -> None:
    """Idempotently load topics, the topic graph and the question bank.

    Topics, edges and question topic tags follow the seed, so retagging a
    question or retiring a topic here updates existing databases too.
    Questions dropped from the bank are retired, not deleted: attempts and
    old sessions still reference them.
    """
    validate_bank(questions)
    existing_topics = {t.id: t for t in db.scalars(select(Topic))}
    for i, (tid, name, x, y) in enumerate(TOPICS):
        if tid in existing_topics:
            # Layout is presentation, not user data: keep it in sync with the seed.
            t = existing_topics[tid]
            t.name, t.position, t.x, t.y = name, i, x, y
        else:
            db.add(Topic(id=tid, name=name, position=i, x=x, y=y))
    wanted_edges = set(EDGES)
    existing_edges = set()
    for e in db.scalars(select(TopicEdge)):
        if (e.from_topic_id, e.to_topic_id) in wanted_edges:
            existing_edges.add((e.from_topic_id, e.to_topic_id))
        else:
            db.delete(e)
    for a, b in EDGES:
        if (a, b) not in existing_edges:
            db.add(TopicEdge(from_topic_id=a, to_topic_id=b))
    db.flush()

    existing = {q.slug: q for q in db.scalars(select(Question).options(selectinload(Question.topics)))}
    wanted = {q.slug for q in questions}
    for slug, question in existing.items():
        question.status = "published" if slug in wanted else "retired"
    retagged = False
    for q in questions:
        if q.slug in existing:
            question = existing[q.slug]
            question.source_url, question.ref = q.source_url, q.ref
            current = [t.topic_id for t in question.topics]
            if current[:1] != list(q.topics[:1]) or set(current) != set(q.topics):
                question.topics.clear()
                db.flush()
                question.topics = [
                    QuestionTopic(topic_id=t, is_primary=(i == 0)) for i, t in enumerate(q.topics)
                ]
                retagged = True
            continue
        question = Question(
            slug=q.slug,
            lc_number=q.number,
            ref=q.ref,
            title=q.title,
            difficulty=q.difficulty,
            summary=q.summary,
            example=q.example,
            criterion=q.criterion,
            hint=q.hint,
            source_url=q.source_url,
        )
        question.topics = [
            QuestionTopic(topic_id=t, is_primary=(i == 0)) for i, t in enumerate(q.topics)
        ]
        question.choices = [
            Choice(
                position=i,
                label=c.label,
                detail=c.detail,
                time_complexity=c.time,
                space_complexity=c.space,
                visual=c.visual,
                verdict=c.verdict.value,
                explanation=c.why,
            )
            for i, c in enumerate(q.choices)
        ]
        db.add(question)

    stale = set(existing_topics) - {t[0] for t in TOPICS}
    if stale:
        db.flush()
        db.execute(delete(UserTopicMastery).where(UserTopicMastery.topic_id.in_(stale)))
        db.execute(delete(QuestionTopic).where(QuestionTopic.topic_id.in_(stale)))
        db.execute(delete(Topic).where(Topic.id.in_(stale)))
    db.commit()

    # Mastery is per topic, so it is rebuilt from attempts whenever tags move.
    if retagged or stale:
        for user_id in db.scalars(select(Attempt.user_id).distinct()):
            recompute_user_mastery(db, user_id)
