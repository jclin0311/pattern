# Pattern Quiz

A web app for learning to recognize algorithm patterns through short multiple-choice
quizzes: each question shows four approaches, you pick the best one, and a Socratic
explanation shows why each approach wins or loses. The design is in
[docs/20260929-pattern-quiz-design.docx](docs/20260929-pattern-quiz-design.docx).

```
backend/                FastAPI + SQLAlchemy (PostgreSQL or SQLite)
  app/
    main.py             app entry: creates tables, migrates, seeds, mounts routers
    config.py           settings from the environment
    clock.py            current time and the learner's local day
    auth_session.py     Google sign-in, login sessions, current user
    db/                 connection, models, additive migrations
    routers/            HTTP endpoints: auth, profile, home, quiz_sessions, dashboard
    practice/           what to study: study_plans, question_recommender, review_schedule, topic_mastery
    insights/           how it's going: dashboard_stats, performance_analysis
    question_bank/      topic_graph, question_schema, seed, and one module per core-route step
                        (step4_tree_dfs.py, ...), collected in route_questions.py
  tests/                mirrors app/ (db/, practice/, insights/, question_bank/); test_api.py
                        covers the endpoints; fixtures/ holds a test-only bank
frontend/               Next.js (App Router): home, quiz, dashboard (Recharts), profile
  app/  components/  lib/
docs/                   design document
docker-compose.yml      local Postgres
```

The frontend proxies `/api/*` to the backend, so both are served from one origin and
the session cookie is first-party.

## Run locally

Needs Python 3.12 with [uv](https://docs.astral.sh/uv/), Node 20+, and Docker only if you
want Postgres.

### First-time setup

```bash
cd backend
uv venv .venv && uv pip install -r requirements.txt --python .venv/bin/python
cp .env.example .env    # settings; all optional
cd ../frontend
npm install
```

### Start

Two terminal tabs, both from the repo root.

```bash
# Tab 1: API at http://127.0.0.1:8000 (interactive docs at /docs)
cd backend
.venv/bin/uvicorn app.main:app --reload --port 8000 --env-file .env

# Tab 2: web app at http://localhost:3000
cd frontend
npm run dev
```

Open http://localhost:3000 and sign in with the demo account.

On startup the API creates the tables, applies migrations and syncs the question bank, so
it is safe to restart at any time. Run `cat backend/.env.example` to see every setting.

### Database

By default the API uses a SQLite file, `backend/quiz.db`. Delete it to start fresh.

To match production, use Postgres in Docker instead:

```bash
docker compose up -d db    # starts in the background
```

Then uncomment `DATABASE_URL` in `backend/.env` and restart the API.

### Stop

Press **Ctrl+C** in both tabs. If you started Postgres:

```bash
docker compose stop        # keeps your data
docker compose down -v     # deletes the database too
```

If a server was started in the background, stop it with:

```bash
pkill -f "next (dev|start)"       # web app
pkill -f "uvicorn app.main:app"   # API
```

### Google sign-in

Create an OAuth 2.0 **Web** client in Google Cloud Console, add `http://localhost:3000`
as an authorized JavaScript origin, and set `GOOGLE_CLIENT_ID` on the backend. The
frontend reads the client id from `GET /api/auth/config`; the backend verifies the ID
token and issues its own httpOnly session cookie.

## Tests

```bash
cd backend && .venv/bin/python -m pytest -q
cd frontend && npx tsc --noEmit
```

## How it works

| Piece | Where | Notes |
|---|---|---|
| Plans | `practice/study_plans.py` | Topic (roadmap, one pattern at a time), Random (no roadmap, one question per topic, tags hidden until answered), Sprint (Hot 100, then Top Interview 150). Chosen on the profile page. Each plan has its own Practice, Review and Extra; mastery and progress span all plans. |
| Daily practice | `practice/question_recommender.py` (`purpose="daily"`) | `daily_goal` new questions, following the topic roadmap. The set is saved per local day. |
| Review | `practice/review_schedule.py` | A question first answered on day *d* is reviewed on *d*+1, 2, 6, 31. Missed days roll over. |
| Extra practice | `practice/question_recommender.py` (`purpose="extra"`) | 5 questions targeting topics missed today. If a topic's prerequisites aren't ready, it practices the prerequisite first. |
| Mastery | `practice/topic_mastery.py` | Recency-weighted, smoothed accuracy per topic. A topic is "ready" at ≥ 65% over ≥ 3 answers. Recomputed when you leave or finish a quiz. |
| Grading | `routers/quiz_sessions.py` | Deterministic. The question payload never includes verdicts or explanations until an answer is recorded. Choice order is shuffled per session. |
| Analysis | `insights/performance_analysis.py` | Only aggregate stats go to Claude (no email or ids). Any cited percentage must match a computed value, or it falls back to a template. Cached by stats hash. |

Topics and the roadmap follow the 12 topic lists from
[如何科学刷题](https://leetcode.cn/discuss/post/3141566/) (`backend/app/question_bank/topic_graph.py`): the core
route is the spine, and each remaining list branches off the core topic it builds on.
Question content has original summaries and source links:

- `backend/app/question_bank/stepN_*.py`: core-route problems rated ≤ 1700, one file per step,
  in route order (binary tree DFS and grid DFS so far).
- `backend/app/question_bank/question_schema.py`: the typed `Question` / `Choice` entries. Each one validates
  itself on import, including the column widths Postgres enforces.

On startup the seed keeps topics, edges and question tags in sync with these files and
rebuilds mastery if any tags moved. Questions removed from the bank are retired, not
deleted, so past attempts keep their history. Topics with no questions yet don't gate the
roadmap. Tests seed an extra fixture bank (`backend/tests/fixtures/`) that covers every topic.
