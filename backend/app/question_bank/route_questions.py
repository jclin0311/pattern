"""The question bank: the core route of 如何科学刷题 (leetcode.cn/discuss/post/3141566).

Problems rated ≤ 1700 or unrated, one module per route step, in step order.
"""

from collections import Counter
from collections.abc import Sequence

from . import (
    step1_sliding_window,
    step2_binary_search,
    step3_data_structures,
    step4_tree_dfs,
    step5_grid_dfs,
    step6_backtracking,
    step7_dp,
)
from .question_schema import Question
from .topic_graph import TOPICS

QUESTIONS: tuple[Question, ...] = (
    *step1_sliding_window.QUESTIONS,
    *step2_binary_search.QUESTIONS,
    *step3_data_structures.QUESTIONS,
    *step4_tree_dfs.QUESTIONS,
    *step5_grid_dfs.QUESTIONS,
    *step6_backtracking.QUESTIONS,
    *step7_dp.QUESTIONS,
)


def validate_bank(questions: Sequence[Question]) -> None:
    """Checks across questions; each question validates itself on creation."""
    for key in ("slug", "number"):
        counts = Counter(getattr(q, key) for q in questions)
        if dupes := sorted(str(k) for k, n in counts.items() if n > 1 and k is not None):
            raise ValueError(f"duplicate {key}: {', '.join(dupes)}")
    topic_ids = {t[0] for t in TOPICS}
    for q in questions:
        if unknown := set(q.topics) - topic_ids:
            raise ValueError(f"{q.slug}: unknown topics {sorted(unknown)}")


validate_bank(QUESTIONS)
