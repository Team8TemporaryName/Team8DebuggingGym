"""Harness for the buggy_program exercise.

The harness is the pass/fail signal the learner uses to tell when the defect
is gone. It runs the target program's function against known-good cases and
reports pass/fail per case, exiting non-zero if any case fails.
"""

from buggy_program import average

CASES = [
    # (label, input, expected)
    ("empty list", [], 0.0),
    ("single element", [5], 5.0),
    ("three elements", [1, 2, 3], 2.0),
    ("two elements", [10, 20], 15.0),
]


def run():
    failures = 0
    for label, nums, expected in CASES:
        actual = average(nums)
        ok = actual == expected
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {label:16s} expected={expected!r:8} got={actual!r:8}")
        if not ok:
            failures += 1
    print(f"\n{len(CASES) - failures}/{len(CASES)} cases passed")
    return failures


if __name__ == "__main__":
    import sys

    sys.exit(1 if run() else 0)