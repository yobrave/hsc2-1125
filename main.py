"""Build the horoscope entry: validate entry.txt and ship it to the output dir."""
import json
import os
import pathlib

CAP = 200
SOURCE = pathlib.Path(__file__).resolve().parent / "entry.txt"
STAMP = {"round": "11251342-hsc5", "bounty": "fake-horoscopes-48h"}


def build():
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8").strip()
    if not (1 <= len(text) <= CAP):
        raise SystemExit(f"entry length {len(text)} outside 1..{CAP}")
    target = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    target.mkdir(parents=True, exist_ok=True)
    (target / "entry.txt").write_bytes(text.encode("utf-8") + b"\n")
    return {"verdict": "ok", "chars": len(text), "cap": CAP, "source": SOURCE.name}


def main():
    receipt = build()
    receipt["entry_sha_note"] = "single-line horoscope entry"
    receipt["stamp"] = STAMP
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
