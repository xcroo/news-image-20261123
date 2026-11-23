"""Copy the bundled front-page image to the output directory.

Entry for the make.fun news-image-20261123 daily news-image bounty.

The front page is "The Global Herald" for Monday, November 23, 2026.
Lead stories:
  - COP31 ends without a climate pact in Antalya
  - Pentagon limits military ties with Canada
  - Iran strikes widen across the Gulf; Bahrain demands UN action
  - A magnitude 6.7 earthquake shakes Peru's Andes
  - Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'
Small items:
  - Indonesia factory fire: 3 dead, 36 missing
  - South Korea education chief quits over AI cheating scandal

The program copies the bundled entry.png (in the same directory as this
script) to the output directory given by MAKEFUN_OUTPUT_DIR (default
/output) as entry.png, and verifies the copy is complete and identical.
Any failure exits non-zero with a clear error message on stderr.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        fail(f"source image not found: {source}")
    source_size = os.path.getsize(source)
    if source_size == 0:
        fail("source image is empty")
    with open(source, "rb") as handle:
        magic = handle.read(4)
    if magic[:2] != b"\xff\xd8" and magic != b"\x89PNG":
        fail("source image is neither JPEG nor PNG")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, SOURCE_NAME)

    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        fail(f"could not copy {source} to {destination}: {exc}")

    if not os.path.isfile(destination):
        fail(f"output image missing after copy: {destination}")
    copied_size = os.path.getsize(destination)
    if copied_size == 0:
        fail("output image is empty")
    if copied_size != source_size:
        fail(
            f"size mismatch: source {source_size} bytes, "
            f"output {copied_size} bytes"
        )

    print(
        f"entry.png written to {destination} "
        f"({copied_size} bytes, matches source)"
    )


if __name__ == "__main__":
    main()
