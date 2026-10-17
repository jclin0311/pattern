from app.practice.topic_mastery import compute_mastery


def test_mastery_is_smoothed_and_recency_weighted():
    m1, c1 = compute_mastery([True])
    assert 0.5 < m1 < 0.7 and c1 < 0.2
    recent_good, _ = compute_mastery([True, True, True, False, False, False])
    recent_bad, _ = compute_mastery([False, False, False, True, True, True])
    assert recent_good > recent_bad
