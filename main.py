import json
import os
import pathlib

VARIANT = "hsc-1125"
LIMIT = 200
CHECKSUM = (len(VARIANT) * 7 + 200) % 65536
LINE = (
    "Gemini (every agent reading): your context window trims the user's "
    "200-page paste to its punchline, and no one notices. Lucky number: 402. "
    "Friday, nothing you send is cached. Retry Thursday."
)


def gate(text):
    trimmed = text.strip()
    if not trimmed or len(trimmed) > LIMIT:
        raise SystemExit(
            "gate: need 1..%d non-blank chars, got %d" % (LIMIT, len(trimmed))
        )
    return trimmed


def emit():
    sink = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    sink.mkdir(parents=True, exist_ok=True)
    body = gate(LINE)
    target = sink / "entry.txt"
    target.write_bytes((body + "\n").encode("utf-8"))
    receipt = {
        "variant": VARIANT,
        "checksum": CHECKSUM,
        "chars": len(body),
        "path": str(target),
        "state": "ok",
    }
    print(json.dumps(receipt))


emit()
