# AGENTS.md — Instructions for AI Coding Agents

This file documents the conventions of this repository so that AI agents (Cline, etc.)
can consistently create problem templates, tests, and comments.

## Repository Layout

```
src/leetcodepy/problems/<category>/pNNNN_<snake_case_title>.py   # solutions
tests/problems/<category>/test_pNNNN_<snake_case_title>.py      # pytest tests
notes/                                                           # study notes
pyproject.toml                                                   # pytest + ruff + mypy config
.vscode/settings.json                                            # format-on-save with ruff (workspace-only)
```

Categories (directories) include: `arrays`, `dp`, `graphs`, `sliding_window`, `strings`, `trees`.
Create a new category directory (with `__init__.py` in the tests tree) if a problem doesn't fit.

## Creating a New Problem Template

File name: `pNNNN_<snake_case_problem_title>.py` where `NNNN` is the LeetCode problem
number zero-padded to 4 digits (e.g., problem 3 → `p0003_...`, problem 643 → `p0643_...`).

Template structure:

```python
# <N>. <Problem Title>
# https://leetcode.com/problems/<problem-slug>/
# Difficulty: <Easy|Medium|Hard>


class Solution:
    def methodNameFromLeetCode(self, s: str) -> int:
        pass
```

Rules:
- Header is exactly 3 comment lines: number+title, URL, difficulty.
- Use LeetCode's original camelCase method signature with full Python type hints
  (`list[int]`, `str`, etc. — repo targets Python 3.11+).
- When multiple approaches exist for one problem, suffix the method name with the
  approach, e.g. `lengthOfLongestSubstringSlidingWindow`, and keep them all in the
  same `Solution` class.
- camelCase method names trigger ruff N802 — this is accepted repo-wide; do NOT
  rename methods to snake_case and do NOT add noqa comments.
- Empty template bodies use `pass`.

## Creating the Matching Test File

Path: `tests/problems/<category>/test_pNNNN_<same_name>.py`. Same category directory
as the solution; ensure the directory has an `__init__.py`.

Test structure (see `tests/problems/sliding_window/test_p0643_maximum_average_subarray_i.py`):

```python
import pytest

from leetcodepy.problems.<category>.pNNNN_<name> import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("arg1", "expected"),
    [
        (..., ...),  # short English note explaining the case
    ],
)
def test_<snake_case_method_name>(sol: Solution, arg1: ..., expected: ...) -> None:
    assert sol.methodName(arg1) == expected
```

Rules:
- Always include the official LeetCode examples as the first parametrize cases,
  plus edge cases (empty input, single element, all-same values, negatives, etc.).
- Use `pytest.approx` for float comparisons.
- Test function names are snake_case; keep the `sol` fixture pattern.
- If the solution method has an approach suffix, the test must call that exact name.

## Adding Detailed Chinese Comments (加中文注释)

After a solution is verified correct, add detailed Chinese comments following this style
(see `p0003_longest_substring_without_repeating_characters.py` as the reference):

1. Above the method: 解法名称 + 时间复杂度 + 空间复杂度, e.g.
   ```python
   # 解法: 滑动窗口 (Sliding Window)
   # 时间复杂度 O(n): left 和 right 指针各自最多移动 n 次
   # 空间复杂度 O(min(n, m)): m 为字符集大小
   ```
2. Explain each variable's meaning where it is declared.
3. Number the main algorithm steps (`# 1. ...`, `# 2. ...`, `# 3. ...`) and explain
   the key insight / invariant of each step (为什么这样做, 循环不变量是什么).
4. Short inline comments (`# 左边界右移一位`) for non-obvious single lines.

**CRITICAL — punctuation rule:** ruff rule RUF003 is enabled and rejects fullwidth
punctuation in comments. Inside Chinese comments, always use ASCII punctuation:
- use `:` not `：`
- use `,` not `，`
- use `.` not `。`
- use `(` `)` not `（` `）`

Chinese characters themselves are fine; only punctuation must be ASCII.

## Verification Workflow (always run before finishing)

```bash
# run the problem's tests
python -m pytest tests/problems/<category>/test_pNNNN_<name>.py

# lint the solution file (N802 camelCase warning is expected and acceptable)
ruff check src/leetcodepy/problems/<category>/pNNNN_<name>.py
```

All tests must pass. The only acceptable remaining ruff warning is N802.

## Tooling Notes

- Formatting: ruff (config in `pyproject.toml`, line-length 100). VS Code
  format-on-save is already configured in `.vscode/settings.json` — do not change
  user-level/global editor settings.
- Type checking: mypy strict mode (`python_version = 3.11`).
- Do NOT modify global git config or store credentials; this repo intentionally
  sets repo-local `credential.helper=` (empty) so pushes prompt for a GitHub
  Personal Access Token each time and nothing is saved to the keychain.
