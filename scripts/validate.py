#!/usr/bin/env python3
"""Validate all JSON data files against the quote schema."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "quote.schema.json"
DATA_DIR = ROOT / "data"

VALID_SENTIMENTS = {"cautionary", "encouraging", "neutral", "humorous", "critical"}
VALID_CONFIDENCE = {"verified", "attributed", "paraphrased"}
VALID_SOURCE_TYPES = {"直播", "短视频", "讲座", "访谈", "文章", "书籍"}
REQUIRED_QUOTE_FIELDS = {"id", "text", "tags", "source", "confidence"}


def validate_quote(quote: dict, file_path: str) -> list[str]:
    """Validate a single quote entry. Returns list of errors."""
    errors = []
    qid = quote.get("id", "<missing id>")

    # Required fields
    for field in REQUIRED_QUOTE_FIELDS:
        if field not in quote:
            errors.append(f"  [{qid}] Missing required field: {field}")

    # ID format
    if "id" in quote and not isinstance(quote["id"], str):
        errors.append(f"  [{qid}] 'id' must be a string")

    # Text
    if "text" in quote and not isinstance(quote["text"], str):
        errors.append(f"  [{qid}] 'text' must be a string")

    # Tags
    if "tags" in quote:
        if not isinstance(quote["tags"], list) or len(quote["tags"]) < 1:
            errors.append(f"  [{qid}] 'tags' must be a non-empty array")

    # Source
    if "source" in quote:
        src = quote["source"]
        if not isinstance(src, dict):
            errors.append(f"  [{qid}] 'source' must be an object")
        elif "type" not in src:
            errors.append(f"  [{qid}] 'source.type' is required")
        elif src["type"] not in VALID_SOURCE_TYPES:
            errors.append(f"  [{qid}] Invalid source.type: {src['type']}")

    # Sentiment
    if "sentiment" in quote and quote["sentiment"] not in VALID_SENTIMENTS:
        errors.append(f"  [{qid}] Invalid sentiment: {quote['sentiment']}")

    # Confidence
    if "confidence" in quote and quote["confidence"] not in VALID_CONFIDENCE:
        errors.append(f"  [{qid}] Invalid confidence: {quote['confidence']}")

    return errors


def validate_file(file_path: Path) -> list[str]:
    """Validate a single JSON data file."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"  Invalid JSON: {e}"]

    if "quotes" not in data:
        return [f"  Missing 'quotes' array"]

    if not isinstance(data["quotes"], list):
        return [f"  'quotes' must be an array"]

    ids = set()
    for quote in data["quotes"]:
        qid = quote.get("id", "")
        if qid in ids:
            errors.append(f"  [{qid}] Duplicate ID")
        ids.add(qid)
        errors.extend(validate_quote(quote, str(file_path)))

    return errors


def main():
    # Validate meta files
    print("Validating meta files...")
    meta_files = ["categories.json", "mentors.json"]
    meta_ok = True
    for name in meta_files:
        path = DATA_DIR / name
        if not path.exists():
            print(f"  MISSING: {name}")
            meta_ok = False
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"  OK: {name}")
        except json.JSONDecodeError as e:
            print(f"  FAIL: {name} — {e}")
            meta_ok = False

    # Find and validate all quote files
    print("\nValidating quote files...")
    quote_files = []
    for mentor_dir in DATA_DIR.iterdir():
        if mentor_dir.is_dir() and mentor_dir.name != "_template":
            for f in sorted(mentor_dir.glob("*.json")):
                quote_files.append(f)

    total_quotes = 0
    all_ok = meta_ok
    for qf in quote_files:
        rel = qf.relative_to(ROOT)
        errors = validate_file(qf)
        if errors:
            print(f"  FAIL: {rel}")
            for e in errors:
                print(e)
            all_ok = False
        else:
            with open(qf, "r", encoding="utf-8") as f:
                data = json.load(f)
            count = len(data.get("quotes", []))
            total_quotes += count
            print(f"  OK: {rel} ({count} quotes)")

    # Summary
    print(f"\nTotal: {len(quote_files)} files, {total_quotes} quotes")
    if all_ok:
        print("All validations passed!")
        return 0
    else:
        print("Some validations failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
