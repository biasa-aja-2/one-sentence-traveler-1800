#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800 -- make.fun entry.

Writes a single sentence to /output/entry.txt explaining the modern
internet to someone arriving from the year 1800. Pure standard library
only.

The sentence: the internet is one road joining houses across the earth
to a single vast library and post office, where any letter you write
arrives before the ink is dry. Every noun in it -- road, house, library,
post office, letter, ink -- is something a person from 1800 already
knows, and the one image that sticks is a letter arriving before its
ink has dried.
"""

import os
import sys

ENTRY = "It is one road joining houses across the earth to a single vast library and post office, where any letter you write arrives before the ink is dry."

MIN_CHARS = 1
MAX_CHARS = 200


def check_gates(text):
    """Refuse to write unless every kit gate passes. Returns a list of failures."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("entry is not valid UTF-8")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append(
            "entry is %d characters, outside the 1-200 gate" % len(text)
        )
    if text.strip() == "":
        failures.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        failures.append("entry is not one line")
    if text.count(".") != 1 or "!" in text or "?" in text:
        failures.append("entry is not exactly one sentence")
    if not text.endswith("."):
        failures.append("entry does not end with a full stop")
    return failures


def main():
    failures = check_gates(ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAILED: %s" % failure, file=sys.stderr)
        return 1

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    os.chmod(out_path, 0o644)

    # Read it back and verify what is on disk, byte for byte.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        print("GATE FAILED: read-back differs from the entry", file=sys.stderr)
        return 1
    if check_gates(written):
        print("GATE FAILED: written file fails the gates", file=sys.stderr)
        return 1

    print("OK: wrote %s (%d characters, 1 line)" % (out_path, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
