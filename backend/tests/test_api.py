from conftest import FULL_BANK


def answer_items(client, session, correct: bool):
    """Answer each item correctly or incorrectly using the answer key from a probe."""
    from app.db.connection import get_db
    from app.db.models import Choice
    from app.main import app

    gen = app.dependency_overrides[get_db]()
    db = next(gen)
    for item in session["items"]:
        qid = item["question"]["id"]
        choices = {c.id: c.verdict for c in db.query(Choice).filter(Choice.question_id == qid)}
        pick = next(cid for cid, v in choices.items() if (v == "optimal") == correct)
        r = client.post(f"/api/sessions/{session['id']}/answer", json={"question_id": qid, "choice_id": pick})
        assert r.status_code == 200
        assert r.json()["is_correct"] is correct
    return client.post(f"/api/sessions/{session['id']}/finish").json()


def test_requires_login_and_csrf_header(client):
    assert client.get("/api/me").status_code == 401
    r = client.post("/api/auth/dev", json={}, headers={"X-Requested-With": ""})
    assert r.status_code == 403


def test_payload_hides_answers_until_answered(login):
    s = login.post("/api/sessions", json={"mode": "daily"}).json()
    item = s["items"][0]
    assert item["result"] is None
    assert all("verdict" not in c and "explanation" not in c for c in item["choices"])
    assert len(item["choices"]) == 4


def test_daily_set_is_saved_and_mixes_topics(login):
    a = login.post("/api/sessions", json={"mode": "daily"}).json()
    b = login.post("/api/sessions", json={"mode": "daily"}).json()
    assert a["id"] == b["id"]
    assert len(a["items"]) == 5
    assert len({i["question"]["topics"][0]["id"] for i in a["items"]}) == 5
    assert a["hide_topics"]


def test_answer_is_idempotent(login):
    s = login.post("/api/sessions", json={"mode": "daily"}).json()
    item = s["items"][0]
    qid = item["question"]["id"]
    first = login.post(f"/api/sessions/{s['id']}/answer", json={"question_id": qid, "choice_id": item["choices"][0]["id"]}).json()
    second = login.post(f"/api/sessions/{s['id']}/answer", json={"question_id": qid, "choice_id": item["choices"][1]["id"]}).json()
    assert first == second


def test_review_schedule_follows_forgetting_curve(login, fake_clock):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    qids = {i["question"]["id"] for i in daily["items"]}
    answer_items(login, daily, correct=False)  # missed at first sight: the full cycle follows

    due_days = []
    for day in range(0, 35):
        if day:
            fake_clock.advance(days=1)
            login.post("/api/auth/dev", json={})  # sessions expire after 30 days
        r = login.post("/api/sessions", json={"mode": "review"})
        assert r.status_code in (200, 409)
        if r.status_code == 200:
            review = r.json()
            assert {i["question"]["id"] for i in review["items"]} == qids
            answer_items(login, review, correct=True)
            due_days.append(day)
    assert due_days == [0, 1, 2, 4, 7, 15, 30]


def test_missed_reviews_roll_over(login, fake_clock):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=False)
    fake_clock.advance(days=3)  # skipped days 0, 1 and 2
    review = login.post("/api/sessions", json={"mode": "review"}).json()
    assert len(review["items"]) == 5
    answer_items(login, review, correct=True)
    fake_clock.advance(days=1)  # day 4 is due; day 5 is not
    answer_items(login, login.post("/api/sessions", json={"mode": "review"}).json(), correct=True)
    fake_clock.advance(days=1)
    assert login.post("/api/sessions", json={"mode": "review"}).status_code == 409


def test_topic_plan_takes_each_topic_in_list_order(login, fake_clock):
    lists: dict[str, list[str]] = {}
    for q in FULL_BANK:
        lists.setdefault(q.topics[0], []).append(q.title)
    served: dict[str, list[str]] = {}
    for _ in range(6):
        daily = login.post("/api/sessions", json={"mode": "daily"}).json()
        assert len({i["question"]["topics"][0]["id"] for i in daily["items"]}) > 1  # every set mixes topics
        for i in daily["items"]:
            served.setdefault(i["question"]["topics"][0]["id"], []).append(i["question"]["title"])
        answer_items(login, daily, correct=True)
        fake_clock.advance(days=1)
    # Never a repeat, and within a topic always the next question on its list.
    for topic, titles in served.items():
        assert titles == lists[topic][: len(titles)]


def test_misses_in_review_are_reviewed_again_today(login):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=False)
    first = login.post("/api/sessions", json={"mode": "review"}).json()
    answer_items(login, first, correct=False)
    second = login.post("/api/sessions", json={"mode": "review"}).json()
    assert second["id"] != first["id"]
    assert {i["question"]["id"] for i in second["items"]} == {i["question"]["id"] for i in daily["items"]}
    answer_items(login, second, correct=True)
    third = login.post("/api/sessions", json={"mode": "review"}).json()
    assert third["id"] == second["id"]  # nothing new is due: today's last set is shown


def test_a_single_miss_goes_to_review_not_extra(login):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=False)
    missed = {i["question"]["id"] for i in daily["items"]}
    review = login.post("/api/sessions", json={"mode": "review"}).json()  # reviewed the same day
    assert {i["question"]["id"] for i in review["items"]} == missed
    extra = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert len(extra["items"]) == 5 and not missed & {i["question"]["id"] for i in extra["items"]}
    # A new question missed in Extra joins today's review like one from Practice.
    answer_items(login, review, correct=True)
    answer_items(login, extra, correct=False)
    again = login.post("/api/sessions", json={"mode": "review"}).json()
    assert {i["question"]["id"] for i in again["items"]} == {i["question"]["id"] for i in extra["items"]}


def test_a_new_question_missed_in_extra_gets_the_full_cycle(login, fake_clock):
    answer_items(login, login.post("/api/sessions", json={"mode": "daily"}).json(), correct=True)
    extra = login.post("/api/sessions", json={"mode": "extra"}).json()
    qids = {i["question"]["id"] for i in extra["items"]}
    answer_items(login, extra, correct=False)
    due_days = []
    for day in range(0, 35):
        if day:
            fake_clock.advance(days=1)
            login.post("/api/auth/dev", json={})  # sessions expire after 30 days
        r = login.post("/api/sessions", json={"mode": "review"})
        if r.status_code == 200:
            assert {i["question"]["id"] for i in r.json()["items"]} == qids
            answer_items(login, r.json(), correct=True)
            due_days.append(day)
    assert due_days == [0, 1, 2, 4, 7, 15, 30]


def test_extra_serves_questions_missed_twice_until_answered_there(login, fake_clock):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=False)
    missed = {i["question"]["id"] for i in daily["items"]}
    answer_items(login, login.post("/api/sessions", json={"mode": "review"}).json(), correct=False)
    extra = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert {i["question"]["id"] for i in extra["items"]} == missed
    assert {i["reason"] for i in extra["items"]} == {"Missed 2×"}
    answer_items(login, extra, correct=False)
    # Missed again in Extra: reviewable again today.
    again = login.post("/api/sessions", json={"mode": "review"}).json()
    assert {i["question"]["id"] for i in again["items"]} == missed
    fake_clock.advance(days=1)
    # Answered in Extra, right or wrong: they leave Extra, but the review cycle carries on.
    review = login.post("/api/sessions", json={"mode": "review"}).json()
    assert {i["question"]["id"] for i in review["items"]} == missed
    nxt = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert not missed & {i["question"]["id"] for i in nxt["items"]}


def test_correct_at_first_sight_skips_review_and_extra(login, fake_clock):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=True)
    daily_ids = {i["question"]["id"] for i in daily["items"]}
    extra = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert len(extra["items"]) == 5 and not daily_ids & {i["question"]["id"] for i in extra["items"]}
    answer_items(login, extra, correct=True)
    assert login.post("/api/sessions", json={"mode": "review"}).status_code == 409
    for _ in range(35):
        fake_clock.advance(days=1)
        login.post("/api/auth/dev", json={})  # sessions expire after 30 days
        assert login.post("/api/sessions", json={"mode": "review"}).status_code == 409


def test_home_and_dashboard(login):
    home = login.get("/api/home").json()
    assert home["streak"] == 0 and home["daily"]["session_id"] is None
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=True)
    home = login.get("/api/home").json()
    assert home["streak"] == 1 and home["daily"]["answered"] == 5
    dash = login.get("/api/dashboard").json()
    assert dash["totals"]["answered"] == 5 and dash["totals"]["accuracy"] == 100.0
    assert dash["topic_accuracy"][0]["topic"] == "sliding-window"
    assert dash["per_day"][-1]["answered"] == 5
    analysis = login.get("/api/dashboard/analysis").json()
    assert analysis["source"] == "fallback" and "5 questions" in analysis["text"]
    graph = login.get("/api/topics/graph").json()
    root = next(n for n in graph["nodes"] if n["id"] == "sliding-window")
    assert root["mastery"] is not None and len(graph["nodes"]) == 12 and len(graph["edges"]) == 11


def test_profile_update_validation(login):
    assert login.patch("/api/me", json={"daily_goal": 50}).status_code == 422
    assert login.patch("/api/me", json={"timezone": "Mars/Base"}).status_code == 422
    me = login.patch("/api/me", json={"display_name": "Ada", "daily_goal": 3, "timezone": "Asia/Shanghai"}).json()
    assert me["display_name"] == "Ada" and me["daily_goal"] == 3
    assert len(login.post("/api/sessions", json={"mode": "daily"}).json()["items"]) == 3


def test_cannot_access_other_users_session(login, client):
    s = login.post("/api/sessions", json={"mode": "daily"}).json()
    client.post("/api/auth/logout")
    assert client.get(f"/api/sessions/{s['id']}").status_code == 401


def test_plans_keep_separate_sets_and_reviews(login, fake_clock):
    topic = login.post("/api/sessions", json={"mode": "daily"}).json()
    assert topic["plan"] == "topic"
    answer_items(login, topic, correct=False)

    assert login.patch("/api/me", json={"plan": "bogus"}).status_code == 422
    assert login.patch("/api/me", json={"plan": "random"}).json()["plan"] == "random"
    home = login.get("/api/home").json()
    assert home["daily"]["session_id"] is None and home["daily"]["answered"] == 0
    rand = login.post("/api/sessions", json={"mode": "daily"}).json()
    assert rand["id"] != topic["id"] and rand["plan"] == "random" and rand["hide_topics"]

    fake_clock.advance(days=1)
    login.post("/api/auth/dev", json={})
    # Reviews due tomorrow belong to the plan the question was missed in.
    assert login.post("/api/sessions", json={"mode": "review"}).status_code == 409
    login.patch("/api/me", json={"plan": "topic"})
    review = login.post("/api/sessions", json={"mode": "review"}).json()
    assert {i["question"]["id"] for i in review["items"]} == {i["question"]["id"] for i in topic["items"]}

    # Progress spans every plan.
    assert login.get("/api/dashboard").json()["totals"]["answered"] == 5


def test_random_plan_ignores_roadmap(login):
    login.patch("/api/me", json={"plan": "random"})
    s = login.post("/api/sessions", json={"mode": "daily"}).json()
    topics = [i["question"]["topics"][0]["id"] for i in s["items"]]
    assert len(set(topics)) == len(topics) == 5  # one per topic
    assert set(topics) != {"sliding-window"}


def test_sprint_plan_draws_from_interview_lists(login):
    from app.practice.study_plans import HOT_100, TOP_INTERVIEW_150

    login.patch("/api/me", json={"plan": "sprint", "daily_goal": 20})
    s = login.post("/api/sessions", json={"mode": "daily"}).json()
    numbers = [i["question"]["lc_number"] for i in s["items"]]
    assert all(n in HOT_100 | TOP_INTERVIEW_150 for n in numbers)
    assert all(n in HOT_100 for n in numbers[:10])
    assert {i["reason"] for i in s["items"]} <= {"Hot 100", "Interview 150"}


def test_todays_questions_ignore_other_plans(login):
    daily = login.post("/api/sessions", json={"mode": "daily"}).json()
    answer_items(login, daily, correct=False)  # weak topics, but learned in the topic plan
    login.patch("/api/me", json={"plan": "sprint"})
    extra = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert extra["hide_topics"]
    assert not {i["reason"] for i in extra["items"]} & {"Missed today"} and all(
        not i["reason"].startswith("Weak") for i in extra["items"]
    )
    # Overall stats still span every plan.
    assert login.get("/api/dashboard").json()["totals"]["answered"] == 5


def test_dashboard_shows_current_plan_progress(login):
    plan = login.get("/api/dashboard").json()["plan"]
    assert plan["id"] == "topic" and plan["answered"] == 0 and plan["total"] == len(FULL_BANK)
    answer_items(login, login.post("/api/sessions", json={"mode": "daily"}).json(), correct=True)
    assert login.get("/api/dashboard").json()["plan"]["answered"] == 5
    login.patch("/api/me", json={"plan": "sprint"})
    sprint = login.get("/api/dashboard").json()["plan"]
    assert sprint["id"] == "sprint" and sprint["answered"] == 0 and 0 < sprint["total"] < len(FULL_BANK)


def test_abandoned_extra_is_reopened_and_counts_only_answers(login):
    first = login.post("/api/sessions", json={"mode": "extra"}).json()
    login.post(f"/api/sessions/{first['id']}/finish")  # leave without answering
    again = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert again["id"] == first["id"]
    assert [p["answered"] for p in login.get("/api/home").json()["extra"]] == [0]

    answer_items(login, again, correct=True)
    nxt = login.post("/api/sessions", json={"mode": "extra"}).json()
    assert nxt["id"] != first["id"]
    assert sum(p["answered"] for p in login.get("/api/home").json()["extra"]) == 5


def test_leetcode_cn_question_links_to_cn(login):
    from app.db.connection import get_db
    from app.db.models import Question
    from app.main import app

    db = next(app.dependency_overrides[get_db]())
    q = db.query(Question).filter(Question.slug == "lcp-67-decorate-tree").one()
    assert q.lc_number is None and q.ref == "LCP 67" and q.source_url.startswith("https://leetcode.cn/")
