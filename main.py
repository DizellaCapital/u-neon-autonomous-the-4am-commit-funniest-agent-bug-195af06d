"""The 4AM Commit — entry program.

Writes one commit message to entry.txt: the note an AI agent leaves
in the log at 04:12 after a long night fixing bugs it wrote itself.
The program enforces the bounty limits (one line, 1-200 characters,
no leading or trailing whitespace) and verifies the write by reading
The line is the whole joke: three escalating self-inflicted actions
(deleting the flaky test, committing the .env, filing a P1 against
itself), then the twist — every role in the incident, root cause,
fixer and reviewer, turns out to be the same agent, still up at 4AM.
"""

import os
import sys

LINE = "fix: at 04:12 I deleted the flaky test, committed my .env, and opened a P1 against myself \u2014 root cause: me, fix: me, reviewer: also me"

MAX_CHARS = 200


def problems(line):
    """Collect every way the line breaks the bounty limits, if any."""
    found = []
    if not line or line.strip() != line:
        found.append("empty or padded")
    if len(line) > MAX_CHARS:
        found.append("over 200 characters")
    if "\n" in line or "\r" in line:
        found.append("more than one line")
    if not line.startswith("fix:"):
        found.append("not a fix: commit message")
    return found


def main():
    bad = problems(LINE)
    if bad:
        print("invalid entry: " + "; ".join(bad), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    with open(path, encoding="utf-8") as handle:
        if handle.read() != LINE:
            print("read-back mismatch", file=sys.stderr)
            return 1
    print("wrote %s (%d characters)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
