#!/usr/bin/env python3
"""Generate the first 20 Fibonacci numbers and save them to fibonacci.txt."""

from pathlib import Path


def fibonacci(n: int) -> list[int]:
    """Return a list containing the first ``n`` Fibonacci numbers.

    The sequence starts with 0 and 1: 0, 1, 1, 2, 3, 5, ...
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence


def save_to_file(numbers: list[int], filename: str = "fibonacci.txt") -> Path:
    """Write each number on its own line to ``filename`` and return the path."""
    path = Path(filename)
    path.write_text("\n".join(map(str, numbers)) + "\n", encoding="utf-8")
    return path


def main() -> None:
    numbers = fibonacci(20)
    path = save_to_file(numbers)
    print(f"Saved {len(numbers)} Fibonacci numbers to {path.resolve()}")


if __name__ == "__main__":
    main()
