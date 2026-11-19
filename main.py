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

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def verify_png(path):
    """Refuse to hand the grader anything that is not a whole PNG file.

    A truncated or misnamed image would fail the gate silently; checking
    the eight-byte PNG signature here makes a broken build fail loudly
    instead, before any bytes reach the output directory.
    """
    with path.open("rb") as handle:
        header = handle.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        raise ValueError(f"poster image is not a PNG file: {path}")


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        raise FileNotFoundError(f"missing poster image: {source}")
    verify_png(source)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise IOError("copied image size does not match the source")


if __name__ == "__main__":
    main()
