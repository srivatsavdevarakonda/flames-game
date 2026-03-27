"""
test_flames_engine.py
---------------------
Unit tests for the FLAMES backend algorithm.
Run with: pytest tests/test_flames_engine.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pytest
from flames_engine import (
    remove_common_letters,
    apply_flames_elimination,
    calculate_flames,
    FLAMES_LABELS,
)


# ─── remove_common_letters ────────────────────────────────────────────────────

class TestRemoveCommonLetters:

    def test_basic_common(self):
        r1, r2, common = remove_common_letters("Rohan", "Sohan")
        # Common: O, H, A, N → remaining: R (from Rohan), S (from Sohan)
        assert "R" in r1
        assert "S" in r2
        assert len(common) == 4

    def test_no_common(self):
        r1, r2, common = remove_common_letters("xyz", "abc")
        assert common == []
        assert r1 == "XYZ"
        assert r2 == "ABC"

    def test_identical_names(self):
        r1, r2, common = remove_common_letters("Akash", "Akash")
        assert r1 == ""
        assert r2 == ""
        assert len(common) == len("akash")

    def test_case_insensitive(self):
        r1a, r2a, ca = remove_common_letters("AKASH", "akash")
        r1b, r2b, cb = remove_common_letters("akash", "akash")
        assert len(ca) == len(cb)

    def test_spaces_ignored(self):
        r1, r2, common = remove_common_letters("Raj Kumar", "Rani Sharma")
        # Spaces should be stripped before matching
        assert " " not in r1 and " " not in r2

    def test_duplicate_letters(self):
        # "aab" vs "abc" — only one 'a' matched
        r1, r2, common = remove_common_letters("aab", "abc")
        assert common.count("A") == 1


# ─── apply_flames_elimination ─────────────────────────────────────────────────

class TestApplyFlamesElimination:

    def test_count_1_winner_is_s(self):
        # Count 1: F eliminated first, L second... last one standing
        winner, elim = apply_flames_elimination(1)
        assert winner in "FLAMES"
        assert len(elim) == 5

    def test_winner_not_in_eliminated(self):
        for count in range(1, 20):
            winner, elim = apply_flames_elimination(count)
            assert winner not in elim

    def test_all_letters_covered(self):
        for count in range(1, 7):
            winner, elim = apply_flames_elimination(count)
            all_letters = set("FLAMES")
            assert set(elim) | {winner} == all_letters

    def test_zero_treated_as_one(self):
        # Should not crash; falls back to count=1
        winner, elim = apply_flames_elimination(0)
        assert winner in "FLAMES"

    def test_known_result_count_2(self):
        # Count 2: L eliminated, then A, then S, then F, then M → E wins (or F)
        winner, elim = apply_flames_elimination(2)
        assert winner in "FLAMES"
        assert len(elim) == 5


# ─── calculate_flames (integration) ──────────────────────────────────────────

class TestCalculateFlames:

    def test_returns_valid_winner(self):
        result = calculate_flames("Akash", "Priya")
        assert result.winner in "FLAMES"
        assert result.label in FLAMES_LABELS.values()

    def test_steps_populated(self):
        result = calculate_flames("Raj", "Ria")
        assert len(result.steps) == 3
        for s in result.steps:
            assert s.description
            assert s.step_number in (1, 2, 3)

    def test_total_count(self):
        result = calculate_flames("Sita", "Gita")
        assert result.total_count == len(result.remaining_name1) + len(result.remaining_name2)

    def test_example_rohan_sohan(self):
        # Rohan vs Sohan: common O,H,A,N → remaining R, S → count 2
        result = calculate_flames("Rohan", "Sohan")
        assert result.total_count == 2
        assert result.remaining_name1 == "R"
        assert result.remaining_name2 == "S"

    def test_example_vikas_vani(self):
        # Vikas vs Vani: common V,I,A → remaining K,S from Vikas, N from Vani → count 3
        result = calculate_flames("Vikas", "Vani")
        assert result.total_count == 3

    def test_emoji_present(self):
        result = calculate_flames("Tom", "Jerry")
        assert result.emoji  # Should not be empty

    @pytest.mark.parametrize("n1,n2", [
        ("A", "B"),
        ("Xyz", "Pdq"),
        ("Sameer", "Suman"),
        ("Akash", "Akshita"),
    ])
    def test_various_names(self, n1, n2):
        result = calculate_flames(n1, n2)
        assert result.winner in "FLAMES"
        assert result.name1 == n1
        assert result.name2 == n2
