"""The question bank: the core route of 如何科学刷题 (leetcode.cn/discuss/post/3141566).

Problems rated ≤ 1700 or unrated, one module per route step, in step order.
"""

from collections import Counter
from collections.abc import Sequence

from ..schema import Question
from ..topics import TOPICS
from . import step4_tree_dfs, step5_grid_dfs

QUESTIONS: tuple[Question, ...] = (
    *step4_tree_dfs.QUESTIONS,
    *step5_grid_dfs.QUESTIONS,
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
