"""Deterministic question recommendation.

Everything here comes from the current plan only: its question pool, history,
today's misses and a per-topic mastery computed from its own answers. The
overall mastery shown on the dashboard spans all plans and is not used.

Extra first brings back questions missed at least twice. New questions then come
one of two ways:

- Route-order plans (Topic) interleave topics, taking each topic's next unanswered
  question in list order from whichever topic is least far through its list.
- Other plans pick target topics (weak/uncertain, missed today, untried), rank
  questions by six features plus plan-specific ones, diversify by topic, and log
  scores and reasons.
"""

import random
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..db.models import Attempt, Question, QuizSession, RecommendationLog, Topic
from .study_plans import get_plan, in_pool, list_rank
from .topic_mastery import READY_ATTEMPTS, READY_MASTERY, compute_mastery

ALGORITHM_VERSION = "plans-v1"
DIFFICULTY_LEVEL = {"Easy": 0, "Medium": 1, "Hard": 2}

WEIGHTS = {
    "weakness": 0.25,
    "missed_today": 0.25,
    "novelty": 0.15,
    "difficulty_fit": 0.10,
    "staleness": 0.10,
}
# sprint: Hot 100 before Top Interview 150. random: shuffle within a fit.
PLAN_WEIGHTS = {
    "sprint": {"list": 0.30},
    "random": {"jitter": 0.35},
}


@dataclass
class Target:
    reason: str
    missed_today: bool = False
    priority: int = 0  # lower is more urgent


@dataclass
class PlanMastery:
    mastery: float
    attempts: int


@dataclass
class Scored:
    question_id: int
    topic_id: str
    score: float
    reason: str
    features: dict[str, float] = field(default_factory=dict)


def _target_level(mastery: float | None) -> int:
    if mastery is None or mastery < 0.5:
        return 0
    return 1 if mastery < 0.8 else 2


def recommend(
    db: Session,
    user_id: int,
    today: date,
    limit: int,
    purpose: str,  # "daily" (new material) or "extra" (react to today's performance)
    plan: str = "topic",
    exclude: set[int] | None = None,
) -> list[Scored]:
    p = get_plan(plan)
    topics = {t.id: t for t in db.scalars(select(Topic).order_by(Topic.position))}
    exclude = set(exclude or ())
    plan_weights = PLAN_WEIGHTS.get(p.id, {})

    # Questions already served today in this plan are not repeated, except that
    # Extra may bring back a repeatedly missed question served earlier today.
    served_extra_today: set[int] = set()
    for mode, qids in db.execute(
        select(QuizSession.mode, QuizSession.question_ids).where(
            QuizSession.user_id == user_id, QuizSession.plan == p.id, QuizSession.local_date == today
        )
    ):
        exclude.update(qids)
        if mode == "extra":
            served_extra_today.update(qids)

    attempts = db.execute(
        select(Attempt.question_id, Attempt.is_correct, Attempt.local_date, Attempt.plan, Attempt.mode)
        .where(Attempt.user_id == user_id)
        .order_by(Attempt.created_at)
    ).all()
    last_seen: dict[int, date] = {}
    last_correct: dict[int, bool] = {}
    misses: dict[int, int] = defaultdict(int)
    extra_due: set[int] = set()  # missed twice and not yet answered in Extra since
    for qid, ok, d, a_plan, a_mode in attempts:
        if a_plan == p.id:
            last_seen[qid] = d
            last_correct[qid] = ok
            misses[qid] += not ok
            if a_mode == "extra":
                extra_due.discard(qid)
            elif not ok and misses[qid] == 2:
                extra_due.add(qid)

    questions = list(
        db.scalars(
            select(Question)
            .where(Question.status == "published")
            .options(selectinload(Question.topics))
        )
    )
    q_by_id = {q.id: q for q in questions}
    missed_today_topics: set[str] = set()
    outcomes: dict[str, list[bool]] = defaultdict(list)  # this plan's answers per topic, newest first
    for qid, ok, d, a_plan, _ in reversed(attempts):
        if a_plan != p.id or qid not in q_by_id:
            continue
        for t in q_by_id[qid].topics:
            outcomes[t.topic_id].append(ok)
            if d == today and not ok:
                missed_today_topics.add(t.topic_id)
    mastery = {t: PlanMastery(compute_mastery(o)[0], len(o)) for t, o in outcomes.items()}
    questions = [q for q in questions if in_pool(p, q.lc_number)]
    rng_seed = f"{user_id}:{today.isoformat()}:{p.id}:{purpose}"

    by_topic: dict[str, list[Question]] = defaultdict(list)  # primary topic → questions in list order
    for q in sorted(questions, key=lambda q: q.position):
        by_topic[q.primary_topic_id].append(q)

    # --- target topics (ranked plans)
    targets: dict[str, Target] = {}

    def add_target(topic_id: str, target: Target) -> None:
        if topic_id not in targets or target.priority < targets[topic_id].priority:
            targets[topic_id] = target

    if purpose == "extra":
        for t in missed_today_topics:
            add_target(t, Target("Missed today", missed_today=True, priority=0))
    for t, m in mastery.items():
        if m.mastery < READY_MASTERY:
            add_target(t, Target(f"Weak · {round(m.mastery * 100)}%", priority=1))
        elif m.attempts < READY_ATTEMPTS:
            add_target(t, Target("Needs practice", priority=2))
    for t in topics:
        m = mastery.get(t)
        if t in by_topic and (m is None or m.attempts < READY_ATTEMPTS):
            add_target(t, Target("New topic", priority=1 if purpose == "daily" else 3))

    # --- filter
    def eligible(q: Question, allow_seen: bool) -> bool:
        if q.id in exclude:
            return False
        if q.id in last_seen and not allow_seen:
            return False
        # Recently answered correctly: no need to see it again yet.
        if q.id in last_seen and last_correct.get(q.id) and (today - last_seen[q.id]).days < 3:
            return False
        return True

    def score(q: Question, target: Target | None, topic_id: str) -> Scored:
        m = mastery.get(topic_id)
        seen = q.id in last_seen
        features = {
            "weakness": 1 - (m.mastery if m else 0.5),
            "missed_today": 1.0 if target and target.missed_today else 0.0,
            "novelty": 1.0 if not seen else (0.3 if not last_correct.get(q.id) else 0.0),
            "difficulty_fit": 1 - abs(DIFFICULTY_LEVEL[q.difficulty] - _target_level(m.mastery if m else None)) / 2,
            "staleness": 1.0 if not seen else min((today - last_seen[q.id]).days, 30) / 30,
        }
        if "list" in plan_weights:
            features["list"] = list_rank(q.lc_number) or 0.0
        if "jitter" in plan_weights:
            features["jitter"] = random.Random(f"{rng_seed}:{q.id}").random()
        s = sum({**WEIGHTS, **plan_weights}[k] * v for k, v in features.items())
        if target:
            s += 0.05 * (3 - target.priority)  # urgency tie-breaker
        if topic_id != q.primary_topic_id:
            s -= 0.1  # a secondary tag is weaker evidence the question practices this topic
        # Stable topic order as the final tie-breaker.
        s -= topics[topic_id].position * 1e-4 + q.id * 1e-7
        reason = target.reason if target else "New topic"
        if p.id == "sprint" and reason == "New topic":
            reason = "Hot 100" if features["list"] == 1.0 else "Interview 150"
        return Scored(q.id, topic_id, round(s, 6), reason, {k: round(v, 3) for k, v in features.items()})

    def ranked(allow_seen: bool, only_targets: bool) -> list[Scored]:
        out = []
        for q in questions:
            if not eligible(q, allow_seen):
                continue
            q_topics = [t.topic_id for t in q.topics]
            hit = next((t for t in q_topics if t in targets), None)
            if only_targets and hit is None:
                continue
            topic_id = hit or q_topics[0]
            out.append(score(q, targets.get(topic_id), topic_id))
        return sorted(out, key=lambda s: -s.score)

    # --- assemble the set
    picked: list[Scored] = []
    per_topic: dict[str, int] = defaultdict(int)

    def take(candidates: list[Scored], cap: int | None) -> None:
        for c in candidates:
            if len(picked) >= limit:
                return
            if any(x.question_id == c.question_id for x in picked):
                continue
            if cap is not None and per_topic[c.topic_id] >= cap:
                continue
            picked.append(c)
            per_topic[c.topic_id] += 1

    def next_mixed() -> list[Scored]:
        """Unanswered questions with topics interleaved, each topic in list order. Each pick
        comes from the topic least far through its list, so every set mixes topics."""
        queues = {t: [q for q in qs if q.id not in last_seen and q.id not in exclude] for t, qs in by_topic.items()}
        done = {t: sum(q.id in last_seen for q in qs) for t, qs in by_topic.items()}
        order = {t: i for i, t in enumerate(topics)}
        out: list[Scored] = []
        while len(out) < limit:
            open_topics = [t for t in queues if queues[t]]
            if not open_topics:
                break
            t = min(open_topics, key=lambda t: (done[t] / len(by_topic[t]), order.get(t, 0)))
            q = queues[t].pop(0)
            done[t] += 1
            out.append(Scored(q.id, t, 0.0, "New", {"position": q.position}))
        return out

    def missed_again() -> list[Scored]:
        """Questions missed at least twice and not yet answered in Extra, latest first."""
        pool = [qid for qid in extra_due if qid in q_by_id and qid not in served_extra_today]
        pool.sort(key=lambda qid: (last_seen[qid], q_by_id[qid].position), reverse=True)
        return [Scored(qid, q_by_id[qid].primary_topic_id, 0.0, f"Missed {misses[qid]}×", {}) for qid in pool]

    if purpose == "extra":
        take(missed_again(), None)
    if p.route_order:
        take(next_mixed(), None)
    else:
        take(ranked(allow_seen=False, only_targets=True), p.per_topic_cap)
        take(ranked(allow_seen=False, only_targets=True), None)
        take(ranked(allow_seen=False, only_targets=False), None)
    if purpose == "daily":
        take(ranked(allow_seen=True, only_targets=False), None)

    db.add(
        RecommendationLog(
            user_id=user_id,
            algorithm_version=ALGORITHM_VERSION,
            items=[
                {"question_id": s.question_id, "topic": s.topic_id, "score": s.score,
                 "reason": s.reason, "features": s.features, "purpose": purpose, "plan": p.id}
                for s in picked
            ],
        )
    )
    return picked
