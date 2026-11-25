#!/usr/bin/env python3
"""Copy entry.png to the grader's output directory.

Reads the entry.png sitting beside this file and writes an identical
copy to MAKEFUN_OUTPUT_DIR when set, otherwise /output. Deterministic:
a plain byte copy, so two runs produce identical output.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"Wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
