"""Ship the 24 November 2026 front page to the grader's folder.

The grader runs this file with no arguments in a read-only checkout, and
the only thing it may assume is the environment: MAKEFUN_OUTPUT_DIR names
the folder the picture belongs in. The picture itself is already in the
repo as entry.png, so this file only moves its bytes to where asked."""

from os import environ, makedirs, path


def ship():
    here = path.dirname(path.abspath(__file__))
    page = path.join(here, "entry.png")
    folder = environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    makedirs(folder, exist_ok=True)
    target = path.join(folder, "entry.png")
    with open(page, "rb") as taken:
        picture = taken.read()
    with open(target, "wb") as given:
        given.write(picture)
    print(f"Shipped {target} ({len(picture)} bytes)")


ship()
