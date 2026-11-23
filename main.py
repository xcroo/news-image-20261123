"""news-image-20261123 — front-page image for "The Global Herald".

Date: Monday, November 23, 2026.

Lead stories:
  * COP31 ends without a climate pact in Antalya.
  * Pentagon limits military ties with Canada.
  * Iran strikes widen across the Gulf; Bahrain demands UN action.
  * A magnitude 6.7 earthquake shakes Peru's Andes.
  * Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'.

Small items:
  * Indonesia factory fire: 3 dead, 36 missing.
  * South Korea education chief quits over AI cheating scandal.

The program copies the bundled entry.png (the front page artwork)
into the output directory, verifying the result byte-for-byte.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print("error: %s" % message, file=sys.stderr)
    sys.exit(1)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        fail("source image not found: %s" % source)

    size = os.path.getsize(source)
    if size == 0:
        fail("source image is empty: %s" % source)

    with open(source, "rb") as handle:
        magic = handle.read(8)
    is_jpeg = magic[:3] == b"\xff\xd8\xff"
    is_png = magic[:8] == b"\x89PNG\r\n\x1a\n"
    if not (is_jpeg or is_png):
        fail("source image is neither JPEG nor PNG: %s" % source)
    kind = "JPEG" if is_jpeg else "PNG"

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, SOURCE_NAME)

    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        fail("copy failed (%s -> %s): %s" % (source, destination, exc))

    if not os.path.isfile(destination):
        fail("output missing after copy: %s" % destination)
    copied = os.path.getsize(destination)
    if copied == 0:
        fail("output is empty: %s" % destination)
    if copied != size:
        fail(
            "output size %d differs from source size %d" % (copied, size)
        )

    print("wrote %s (%d bytes, %s)" % (destination, copied, kind))


if __name__ == "__main__":
    main()
