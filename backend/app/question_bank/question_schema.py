"""Typed question-bank entries, validated when the bank is imported.

Summaries are original paraphrases; the full problem lives at `source_url`.
Each question has exactly one optimal choice. Approaches that would tie with
the optimal one under the stated criterion are deliberately left out.
"""

from dataclasses import KW_ONLY, dataclass
from enum import StrEnum
from typing import Literal

Difficulty = Literal["Easy", "Medium", "Hard"]

LEETCODE = "https://leetcode.com/problems/{}/"
LEETCODE_CN = "https://leetcode.cn/"

# Keys of the VISUALS map in frontend/components/ApproachVisual.tsx.
VISUALS = frozenset({
    "array-copy", "backtrack", "binary-search", "bits", "brute", "counting", "dijkstra", "dp-1d", "dp-2d",
    "fast-slow", "graph-bfs", "graph-dfs", "greedy", "hashmap", "heap", "intervals", "linked-list", "math",
    "matrix", "monotonic-stack", "prefix", "queue", "recursion", "set", "sliding-window", "sort", "stack",
    "topo", "tree-bfs", "tree-dfs", "trie", "two-pointers", "union-find",
})


class Verdict(StrEnum):
    OPTIMAL = "optimal"
    SUBOPTIMAL = "suboptimal"  # valid but not the best
    INCORRECT = "incorrect"


OPTIMAL, SUBOPTIMAL, INCORRECT = Verdict


def _fits(name: str, value: str | None, limit: int) -> None:
    # Column widths in models.py; Postgres rejects longer values.
    if value is not None and len(value) > limit:
        raise ValueError(f"{name} longer than {limit} characters: {value!r}")


@dataclass(frozen=True, slots=True)
class Choice:
    label: str
    verdict: Verdict
    _: KW_ONLY
    time: str
    space: str
    visual: str
    detail: str
    why: str  # Socratic explanation shown after answering

    def __post_init__(self) -> None:
        if self.visual not in VISUALS:
            raise ValueError(f"unknown visual {self.visual!r}")
        _fits("label", self.label, 120)
        _fits("time", self.time, 40)
        _fits("space", self.space, 40)


@dataclass(frozen=True, slots=True, kw_only=True)
class Question:
    slug: str
    number: int | None  # None for leetcode.cn-only problems (LCP, LCS, 面试题)
    title: str
    difficulty: Difficulty
    topics: tuple[str, ...]  # first one is primary
    summary: str
    example: str
    criterion: str
    hint: str
    choices: tuple[Choice, Choice, Choice, Choice]
    ref: str | None = None  # display id when there is no number, e.g. "LCP 67"
    url: str | None = None  # defaults to the leetcode.com problem page

    def __post_init__(self) -> None:
        try:
            if self.difficulty not in ("Easy", "Medium", "Hard"):
                raise ValueError(f"bad difficulty {self.difficulty!r}")
            if not self.topics:
                raise ValueError("needs at least one topic")
            if len(self.choices) != 4:
                raise ValueError(f"expected 4 choices, got {len(self.choices)}")
            if sum(c.verdict is OPTIMAL for c in self.choices) != 1:
                raise ValueError("expected exactly one optimal choice")
            if len({c.label for c in self.choices}) != 4:
                raise ValueError("duplicate choice labels")
            if self.number is None and not (self.ref and self.source_url.startswith(LEETCODE_CN)):
                raise ValueError("a problem without a number needs a ref and a leetcode.cn url")
            _fits("slug", self.slug, 120)
            _fits("title", self.title, 200)
            _fits("ref", self.ref, 20)
            _fits("url", self.url, 500)
        except ValueError as e:
            raise ValueError(f"{self.slug}: {e}") from None

    @property
    def source_url(self) -> str:
        return self.url or LEETCODE.format(self.slug)
