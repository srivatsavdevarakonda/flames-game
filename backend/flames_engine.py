"""
flames_engine.py
----------------
Core FLAMES algorithm logic.
Responsibility: Friend 1 (Backend)

Handles:
- Common letter removal
- Remaining letter counting
- Circular FLAMES elimination
- Returning structured result + step trace
"""

from dataclasses import dataclass, field
from typing import List, Optional


FLAMES_LABELS = {
    "F": "Friends",
    "L": "Loves",
    "A": "Affection",
    "M": "Marriage",
    "E": "Enemies",
    "S": "Siblings",
}

FLAMES_EMOJIS = {
    "F": "🤝",
    "L": "❤️",
    "A": "🥰",
    "M": "💐",
    "E": "😬",
    "S": "😊",
}


@dataclass
class FlamesStep:
    step_number: int
    description: str
    detail: Optional[str] = None


@dataclass
class FlamesResult:
    name1: str
    name2: str
    common_letters: List[str]
    remaining_name1: str
    remaining_name2: str
    total_count: int
    elimination_order: List[str]
    winner: str
    label: str
    emoji: str
    steps: List[FlamesStep] = field(default_factory=list)


def remove_common_letters(name1: str, name2: str):
    """
    Remove letters that are common between both names.
    Matching is done character by character (case-insensitive, ignoring spaces).
    Each common letter is counted and removed once per occurrence.

    Returns:
        remaining1 (str): Letters left from name1
        remaining2 (str): Letters left from name2
        common    (list): The matched common letters
    """
    a = list(name1.lower().replace(" ", ""))
    b = list(name2.lower().replace(" ", ""))
    common = []

    for i in range(len(a)):
        if a[i] is None:
            continue
        for j in range(len(b)):
            if b[j] is None:
                continue
            if a[i] == b[j]:
                common.append(a[i].upper())
                a[i] = None
                b[j] = None
                break

    remaining1 = "".join(c for c in a if c is not None).upper()
    remaining2 = "".join(c for c in b if c is not None).upper()
    return remaining1, remaining2, common


def apply_flames_elimination(count: int):
    """
    Perform circular FLAMES elimination.
    Starting from the last eliminated position, count forward `count` steps
    and eliminate that letter. Repeat until one letter remains.

    Args:
        count (int): The number of remaining letters (used as step size)

    Returns:
        winner          (str): The surviving FLAMES letter
        elimination_order (list): Letters in the order they were eliminated
    """
    flames = list("FLAMES")
    if count == 0:
        count = 1  # Treat 0 as 1 to avoid division errors

    idx = 0
    elimination_order = []

    while len(flames) > 1:
        idx = (idx + count - 1) % len(flames)
        eliminated = flames.pop(idx)
        elimination_order.append(eliminated)
        if idx >= len(flames):
            idx = 0

    return flames[0], elimination_order


def calculate_flames(name1: str, name2: str) -> FlamesResult:
    """
    Full FLAMES calculation pipeline.

    Args:
        name1 (str): First person's name
        name2 (str): Second person's name

    Returns:
        FlamesResult: Complete result object with all steps and outcome
    """
    steps = []

    # Step 1: Remove common letters
    remaining1, remaining2, common = remove_common_letters(name1, name2)
    steps.append(FlamesStep(
        step_number=1,
        description="Remove common letters between both names",
        detail=(
            f"Common letters found: {', '.join(common) if common else 'None'}\n"
            f"  {name1} → '{remaining1 or '(empty)'}'\n"
            f"  {name2} → '{remaining2 or '(empty)'}'"
        )
    ))

    # Step 2: Count remaining letters
    total = len(remaining1) + len(remaining2)
    effective_count = total if total > 0 else 1
    steps.append(FlamesStep(
        step_number=2,
        description="Count all remaining letters",
        detail=(
            f"  {name1} remaining: {len(remaining1)} letters\n"
            f"  {name2} remaining: {len(remaining2)} letters\n"
            f"  Total count: {total}{' (treated as 1)' if total == 0 else ''}"
        )
    ))

    # Step 3: FLAMES elimination
    winner, elim_order = apply_flames_elimination(effective_count)
    steps.append(FlamesStep(
        step_number=3,
        description=f"Apply FLAMES elimination with count = {effective_count}",
        detail=(
            f"  Elimination order: {' → '.join(elim_order)}\n"
            f"  Winner: {winner} = {FLAMES_LABELS[winner]}"
        )
    ))

    return FlamesResult(
        name1=name1,
        name2=name2,
        common_letters=common,
        remaining_name1=remaining1,
        remaining_name2=remaining2,
        total_count=total,
        elimination_order=elim_order,
        winner=winner,
        label=FLAMES_LABELS[winner],
        emoji=FLAMES_EMOJIS[winner],
        steps=steps,
    )
