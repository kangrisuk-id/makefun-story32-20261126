"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes a single Wi-Fi network name (at most 32 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback: /output, then this script's directory).

The name is a fixed, tournament-winning string chosen before the build:
48 candidates were scored against the judge brief (joke first, then story,
freshness, tightness), the top 8 went through a knockout bracket, and the
winner beat both runners-up in a self-pairwise check. See candidates.md.

Pure standard library. No clock, no randomness, no network, no environment
reads beyond the output directory. Deterministic: every run writes the exact
same bytes.
"""

import os
import sys

# Tournament winner: "The WiFi died with the marriage" — 31 characters, 23/25.
ENTRY = "The WiFi died with the marriage"


def output_dir():
    """Resolve the output directory, in the order the kit specifies."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def main():
    # Gate check, done by the program itself: 1-32 characters, not blank.
    # len() counts Unicode code points, matching the gate's character count;
    # the entry is pure ASCII, so characters == bytes == 31.
    if not (1 <= len(ENTRY) <= 32):
        sys.stderr.write("entry must be 1-32 characters\n")
        return 1
    if not ENTRY.strip():
        sys.stderr.write("entry must not be only whitespace\n")
        return 1

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file must hold exactly the 31-character name.
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Read back and verify the bytes we just wrote decode to the entry.
    with open(path, "rb") as fh:
        if fh.read().decode("utf-8") != ENTRY:
            sys.stderr.write("round-trip verification failed\n")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
