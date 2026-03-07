# LeetCodePy

LeetCode solutions in Python — organized, tested, and well-structured.

## Project Structure

```
LeetCodePy/
├── src/leetcodepy/
│   ├── solutions/      # LeetCode solutions
│   └── utils/          # Shared helper utilities
├── tests/              # Unit tests (mirrors solutions/)
├── pyproject.toml      # Project config & dependencies
└── Makefile            # Dev commands
```

## Quick Start

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux

# Install in editable mode with dev dependencies
make install

# Run tests
make test

# Lint & format
make lint
make format

# Type check
make typecheck
```

## Adding a New Solution

1. Create the solution file in `src/leetcodepy/solutions/`:

```python
# src/leetcodepy/solutions/two_sum.py

class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
```

2. Add a corresponding test in `tests/solutions/`:

```python
# tests/solutions/test_two_sum.py

from leetcodepy.solutions.two_sum import Solution

class TestTwoSum:
    def setup_method(self) -> None:
        self.sol = Solution()

    def test_basic(self) -> None:
        assert self.sol.two_sum([2, 7, 11, 15], 9) == [0, 1]
```

3. Run the test:

```bash
make test
```

## Available Commands

| Command          | Description                          |
|------------------|--------------------------------------|
| `make install`   | Install project with dev dependencies|
| `make test`      | Run all tests                        |
| `make test-cov`  | Run tests with coverage report       |
| `make lint`      | Check code with ruff                 |
| `make format`    | Auto-format code with ruff           |
| `make typecheck` | Run mypy type checker                |
| `make clean`     | Remove build artifacts & caches      |

## License

MIT
