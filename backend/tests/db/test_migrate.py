from sqlalchemy import create_engine, inspect, text

from app.db.connection import Base
from app.db.migrate import migrate

OLD_REVIEW_ITEMS = """
CREATE TABLE review_items (
    id INTEGER PRIMARY KEY, user_id INTEGER, question_id INTEGER, stage INTEGER,
    due_date DATE, completed_at DATETIME, UNIQUE (user_id, question_id, stage)
)"""


def test_migrate_upgrades_pre_plan_schema(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR)"))
        conn.execute(text("CREATE TABLE quiz_sessions (id INTEGER PRIMARY KEY, mode VARCHAR)"))
        conn.execute(text("CREATE TABLE attempts (id INTEGER PRIMARY KEY, mode VARCHAR)"))
        conn.execute(text(OLD_REVIEW_ITEMS))
        conn.execute(text("CREATE INDEX ix_review_items_user_id ON review_items (user_id)"))
        conn.execute(text("INSERT INTO review_items VALUES (1, 1, 7, 0, '2026-09-02', NULL)"))
    Base.metadata.create_all(engine)  # creates the other tables, leaves these alone
    migrate(engine)
    migrate(engine)  # idempotent

    insp = inspect(engine)
    for table in ("users", "quiz_sessions", "attempts", "review_items"):
        assert "plan" in {c["name"] for c in insp.get_columns(table)}
    assert [u["column_names"] for u in insp.get_unique_constraints("review_items")] == [
        ["user_id", "plan", "question_id", "stage"]
    ]
    with engine.begin() as conn:
        assert conn.execute(text("SELECT plan, question_id FROM review_items")).all() == [("topic", 7)]
        # The same question can now be scheduled in another plan.
        conn.execute(text("INSERT INTO review_items (user_id, plan, question_id, stage, due_date) "
                          "VALUES (1, 'sprint', 7, 0, '2026-09-02')"))


def test_plain_postgres_urls_use_psycopg():
    from app.db.connection import sqlalchemy_url

    neon = "postgresql://u:p@ep-x.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    assert sqlalchemy_url(neon) == "postgresql+psycopg://" + neon.removeprefix("postgresql://")
    assert sqlalchemy_url("postgres://u@h/db") == "postgresql+psycopg://u@h/db"
    assert sqlalchemy_url("postgresql+psycopg://u@h/db") == "postgresql+psycopg://u@h/db"
    assert sqlalchemy_url("sqlite:///./quiz.db") == "sqlite:///./quiz.db"
