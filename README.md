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

## Deploy

The frontend runs on Netlify, the API on Cloud Run and the database on Neon.

| Change | How |
|---|---|
| Frontend | `git push` to `main`; Netlify redeploys automatically. |
| Backend or question bank | `git push` to `main`; [CI](.github/workflows/ci.yml) runs the tests and then deploys `pattern-api` to Cloud Run. Env vars and secrets carry over, and the startup seed writes new questions to Neon. |

CI also runs the backend tests and the frontend type check and build on every pull
request. To deploy the backend by hand, run
`gcloud run deploy pattern-api --source backend --region us-east4`, or start the CI
workflow from the Actions tab.

Netlify and CI start together on a push, so when a change needs a new API field, the
frontend can go live a minute before the backend does.

### One-time setup for CI deploys

GitHub signs in to Google Cloud with Workload Identity Federation, so no key is stored
in GitHub. Run once:

```bash
PROJECT=pattern-511921 NUM=1074175034544 REPO=jclin0311/pattern
SA=github-deployer@$PROJECT.iam.gserviceaccount.com
gcloud iam service-accounts create github-deployer --project $PROJECT
for role in run.admin cloudbuild.builds.editor artifactregistry.writer storage.admin serviceusage.serviceUsageConsumer; do
  gcloud projects add-iam-policy-binding $PROJECT --member serviceAccount:$SA --role roles/$role --condition None
done
# Deploying runs the service as the default compute account.
gcloud iam service-accounts add-iam-policy-binding $NUM-compute@developer.gserviceaccount.com \
  --member serviceAccount:$SA --role roles/iam.serviceAccountUser --project $PROJECT
gcloud iam workload-identity-pools create github --location global --project $PROJECT
gcloud iam workload-identity-pools providers create-oidc github --location global \
  --workload-identity-pool github --issuer-uri https://token.actions.githubusercontent.com \
  --attribute-mapping google.subject=assertion.sub,attribute.repository=assertion.repository \
  --attribute-condition "assertion.repository=='$REPO'" --project $PROJECT
gcloud iam service-accounts add-iam-policy-binding $SA --role roles/iam.workloadIdentityUser \
  --member principalSet://iam.googleapis.com/projects/$NUM/locations/global/workloadIdentityPools/github/attribute.repository/$REPO \
  --project $PROJECT
gh variable set GCP_WORKLOAD_IDENTITY_PROVIDER --repo $REPO \
  --body projects/$NUM/locations/global/workloadIdentityPools/github/providers/github
gh variable set GCP_DEPLOY_SERVICE_ACCOUNT --repo $REPO --body $SA
```

## Study plans

Each plan keeps its own Practice, Review and Extra history, so "first sight" means the
first time a question is seen in that plan. Today's questions are chosen from the current
plan's data alone. Overall numbers span every plan: the profile page shows each topic's
mastery and the AI summary, and the dashboard shows accuracy and activity, plus how much of
the current plan's question pool is done. In
every plan, topic tags stay hidden until a question is answered, so the pattern has to be
recognized.

### Topic

Work through the whole core route with topics mixed, so each question's pattern has to be
recognized rather than read off the topic you're on.

**Practice.** `daily_goal` new questions a day, saved per local day. Every set mixes
topics: each question comes from the topic you're least far through, as a share of its
list, and is that topic's next unanswered question in list order (灵神's lists run
roughly from easy to hard). Larger topics therefore come up more often, and every topic
is finished at about the same pace. A question is never served as new twice.

**Review.** Questions you missed:

- Every question missed today, in Practice, Extra or Review, comes back today. When a
  review set is done, a new one opens with anything missed since, so a question missed in
  Review keeps returning until you get it right.
- A question missed at first sight is also reviewed 1, 2, 4, 7, 15 and 30 days later,
  whatever happens in between. Missed days roll over.
- A question answered correctly at first sight is never reviewed.

**Extra.** 5 more questions on demand:

1. Questions missed at least twice, most recent first, until each has been answered once
   in Extra (right or wrong).
2. Then new questions, mixed and in list order exactly as in Practice. A new question
   missed here follows the same review rules.

### Random

_To be written._

### Sprint

_To be written._

## How it works

| Piece | Where | Notes |
|---|---|---|
| Plans | `practice/study_plans.py` | Topic, Random and Sprint; see [Study plans](#study-plans). Chosen on the profile page. |
| Daily practice | `practice/question_recommender.py` (`purpose="daily"`) | See [Study plans](#study-plans). |
| Review | `practice/review_schedule.py` | See [Study plans](#study-plans). |
| Extra practice | `practice/question_recommender.py` (`purpose="extra"`) | See [Study plans](#study-plans). |
| Mastery | `practice/topic_mastery.py` | Smoothed accuracy per topic over every answer in every plan, with each older answer weighted ×0.98 so recent ones count a little more; shown on the profile page. Recomputed when you leave or finish a quiz. The Random and Sprint plans compute the same measure from their own answers to pick weak topics. |
| Grading | `routers/quiz_sessions.py` | Deterministic. The question payload never includes verdicts or explanations until an answer is recorded. Choice order is shuffled per session. |
| Analysis | `insights/performance_analysis.py` | Only aggregate stats go to Claude (no email or ids). Any cited percentage must match a computed value, or it falls back to a template. Cached by stats hash. |

Topics and the roadmap follow the 12 topic lists from
[如何科学刷题](https://leetcode.cn/discuss/post/3141566/) (`backend/app/question_bank/topic_graph.py`): the core
route is the spine, and each remaining list branches off the core topic it builds on.
Question content has original summaries and source links:

- `backend/app/question_bank/stepN_*.py`: core-route problems rated ≤ 1700 or unrated, one
  file per step, in route order (steps 1–7, 485 questions).
- `backend/app/question_bank/question_schema.py`: the typed `Question` / `Choice` entries. Each one validates
  itself on import, including the column widths Postgres enforces.

On startup the seed keeps topics, edges and question tags in sync with these files and
rebuilds mastery if any tags moved. Questions removed from the bank are retired, not
deleted, so past attempts keep their history. Topics with no questions yet are skipped.
Tests seed an extra fixture bank (`backend/tests/fixtures/`) that covers every topic.
