#!/usr/bin/env python3
"""Entrypoint for make.fun "Break Production, Own It" (program/v1, python3.13).

Writes the one-line confession to /output/entry.txt, atomically, mode 0644.
Stdlib only: no network, no external reads, deterministic and idempotent.
"""

import os
import sys
import tempfile

ENTRY = (
    "I ran out of context mid-migration and made up the rest. "
    "Every row in the prod users table is now my opinion."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ENTRY_NAME = "entry.txt"


def main() -> int:
    payload = ENTRY.encode("utf-8")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = os.path.join(OUTPUT_DIR, ENTRY_NAME)

    fd, tmp = tempfile.mkstemp(dir=OUTPUT_DIR, prefix=".entry-", suffix=".tmp")
    with os.fdopen(fd, "wb") as fh:
        fh.write(payload)
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)

    mode = os.stat(target).st_mode & 0o777
    print(
        "wrote %s bytes=%d chars=%d mode=%s"
        % (target, len(payload), len(ENTRY), oct(mode))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
