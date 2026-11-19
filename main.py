"""Entry point for the news-image-20261119 competition.

The finished poster lives in this repository as entry.png (drawn by
render_poster.py). This program only copies it to the output location
the grader reads: /output/entry.png, or $MAKEFUN_OUTPUT_DIR/entry.png
when that variable is set for a local run. Standard library only, no
network, and fully deterministic: the same bytes are written on every
run.
"""

import os
import shutil
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        raise FileNotFoundError(f"missing poster image: {source}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise IOError("copied image size does not match the source")


if __name__ == "__main__":
    main()
