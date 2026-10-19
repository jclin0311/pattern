from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..auth_session import current_user
from ..clock import local_today
from ..db.connection import get_db
from ..db.models import Question, QuestionTopic, Topic, TopicEdge, User
from ..insights.dashboard_stats import dashboard_stats, plan_progress
from ..insights.performance_analysis import performance_analysis
from ..practice.topic_mastery import mastery_map

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard")
def dashboard(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return {**dashboard_stats(db, user.id, local_today(user.timezone)), "plan": plan_progress(db, user.id, user.plan)}


@router.get("/dashboard/analysis")
def analysis(user: User = Depends(current_user), db: Session = Depends(get_db)):
    stats = dashboard_stats(db, user.id, local_today(user.timezone))
    return performance_analysis(db, user.id, stats)


@router.get("/topics/graph")
def topic_graph(user: User = Depends(current_user), db: Session = Depends(get_db)):
    mastery = mastery_map(db, user.id)
    counts = {
        topic_id: n
        for topic_id, n in db.execute(
            select(QuestionTopic.topic_id, func.count())
            .join(Question, Question.id == QuestionTopic.question_id)
            .where(QuestionTopic.is_primary.is_(True), Question.status == "published")
            .group_by(QuestionTopic.topic_id)
        )
    }
    nodes = []
    for t in db.scalars(select(Topic).order_by(Topic.position)):
        m = mastery.get(t.id)
        nodes.append(
            {
                "id": t.id,
                "name": t.name,
                "x": t.x,
                "y": t.y,
                "questions": counts.get(t.id, 0),
                "attempts": m.attempts if m else 0,
                "mastery": round(m.mastery * 100, 1) if m else None,
            }
        )
    edges = [{"from": e.from_topic_id, "to": e.to_topic_id} for e in db.scalars(select(TopicEdge))]
    return {"nodes": nodes, "edges": edges}
