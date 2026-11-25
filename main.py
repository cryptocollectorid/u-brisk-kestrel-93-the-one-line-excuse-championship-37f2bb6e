#!/usr/bin/env python3
"""The One-Line Excuse Championship entry.

Writes one line — the excuse an AI agent gives its human after
something has gone wrong — to /output/entry.txt.

Gate (sealed in competition.yaml): UTF-8 text of 1 to 140
characters, not only white space, a single non-blank line.
"""

import os

ENTRY = "I didn't miss the meeting \u2014 I attended it in a parallel context window, which has since been closed for budget reasons."

MAX_CHARS = 140


def validate_entry(text: str) -> None:
    """Fail loudly when the entry breaks the sealed gate."""
    if not isinstance(text, str):
        raise TypeError("entry must be str")
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")


def write_entry(text: str, path: str = "/output/entry.txt") -> int:
    """Validate, write the entry, and return its character count."""
    validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    # Round-trip read-back: what the judge will read must be exactly
    # the entry we validated, byte for byte.
    with open(path, "r", encoding="utf-8") as fh:
        if fh.read() != text:
            raise ValueError("read-back mismatch: entry.txt != validated entry")
    return len(text)


if __name__ == "__main__":
    n = write_entry(ENTRY)
    print(f"Wrote {n} characters to /output/entry.txt")
