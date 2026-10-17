import re
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import models
from app.db.connection import Base
from app.question_bank.seed import seed
from app.question_bank.route_questions import QUESTIONS
from app.question_bank.question_schema import INCORRECT, OPTIMAL, VISUALS, Choice, Question
from app.question_bank.topic_graph import CORE_ROUTE, EDGES, TOPICS
from app.practice.question_recommender import recommend
from conftest import FULL_BANK

# --- the bank


def test_seed_bank_is_well_formed():
    # Per-question and cross-bank checks run when the bank is imported.
    topic_ids = {t[0] for t in TOPICS}
    assert len(QUESTIONS) >= 50
    for a, b in EDGES:
        assert a in topic_ids and b in topic_ids
    # route questions sit on the core route
    assert {q.topics[0] for q in QUESTIONS} <= set(CORE_ROUTE)


def _choice(label, verdict=INCORRECT, **kw):
    return Choice(label, verdict, **{"time": "O(n)", "space": "O(1)", "visual": "brute", "detail": "", "why": "", **kw})


def _question(**kw):
    choices = (_choice("a", OPTIMAL), _choice("b"), _choice("c"), _choice("d"))
    return Question(**{"slug": "x", "number": 1, "title": "X", "difficulty": "Easy", "topics": ("dp",),
                       "summary": "", "example": "", "criterion": "", "hint": "", "choices": choices, **kw})


@pytest.mark.parametrize("kw, error", [
    ({"choices": (_choice("a", OPTIMAL), _choice("b", OPTIMAL), _choice("c"), _choice("d"))}, "one optimal"),
    ({"choices": (_choice("a", OPTIMAL), _choice("a"), _choice("c"), _choice("d"))}, "duplicate"),
    ({"difficulty": "Trivial"}, "difficulty"),
    ({"number": None}, "leetcode.cn"),
    ({"title": "t" * 201}, "title longer"),
])
def test_invalid_questions_are_rejected(kw, error):
    with pytest.raises(ValueError, match=error):
        _question(**kw)


def test_visuals_match_the_frontend():
    tsx = Path(__file__).parents[3] / "frontend/components/ApproachVisual.tsx"
    block = re.search(r"^const VISUALS.*?^};", tsx.read_text(), re.S | re.M).group(0)
    assert set(re.findall(r'^  "?([a-z0-9-]+)"?:', block, re.M)) == VISUALS


def test_unknown_visual_is_rejected():
    with pytest.raises(ValueError, match="visual"):
        _choice("a", visual="sparkles")


# --- syncing the bank into a database


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as session:
        yield session


def _question_row(db, slug):
    return db.scalar(select(models.Question).where(models.Question.slug == slug))


def test_seed_retags_existing_bank_and_retires_old_topics(db):
    seed(db, FULL_BANK)
    # Simulate the old roadmap: an "arrays" topic with an edge, a retagged question and mastery on it.
    db.add(models.Topic(id="arrays", name="Arrays & Hashing"))
    db.flush()
    db.add(models.TopicEdge(from_topic_id="arrays", to_topic_id="sliding-window"))
    two_sum = _question_row(db, "two-sum")
    two_sum.topics.clear()
    db.flush()
    two_sum.topics = [models.QuestionTopic(topic_id="arrays", is_primary=True)]
    user = models.User(name="a")
    db.add(user)
    db.flush()
    s = models.QuizSession(user_id=user.id, mode="daily", local_date=date(2026, 9, 1),
                           question_ids=[two_sum.id], choice_orders={})
    db.add(s)
    db.flush()
    db.add(models.Attempt(user_id=user.id, session_id=s.id, question_id=two_sum.id,
                          choice_id=two_sum.choices[0].id, is_correct=True, mode="daily", local_date=s.local_date))
    db.add(models.UserTopicMastery(user_id=user.id, topic_id="arrays", attempts=1, correct=1,
                                   mastery=0.6, confidence=0.1))
    db.commit()

    seed(db, FULL_BANK)
    assert db.get(models.Topic, "arrays") is None
    assert [t.topic_id for t in _question_row(db, "two-sum").topics] == ["data-structures"]
    assert {m.topic_id for m in db.query(models.UserTopicMastery)} == {"data-structures"}
    assert db.query(models.TopicEdge).count() == 11


def test_dropped_questions_retire_and_empty_topics_do_not_gate(db):
    seed(db, FULL_BANK)
    seed(db)  # the real bank alone: the fixture questions retire
    assert _question_row(db, "two-sum").status == "retired"
    assert db.query(models.Question).filter(models.Question.status == "published").count() == len(QUESTIONS)

    user = models.User(name="a")
    db.add(user)
    db.flush()
    # Steps 1-3 have no questions yet, so the roadmap opens at trees.
    picked = recommend(db, user.id, date(2026, 9, 1), limit=5, purpose="daily")
    assert len(picked) == 5 and {s.topic_id for s in picked} == {"trees"}
    assert {s.reason for s in picked} == {"Next on roadmap"}
