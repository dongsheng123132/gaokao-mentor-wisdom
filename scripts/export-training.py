#!/usr/bin/env python3
"""Export quote data to AI training formats (RAG chunks, fine-tuning pairs)."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
EXPORT_DIR = ROOT / "exports"


def load_all_quotes() -> list[dict]:
    """Load all quotes from all mentor directories."""
    quotes = []
    for mentor_dir in DATA_DIR.iterdir():
        if mentor_dir.is_dir() and mentor_dir.name not in ("_template",):
            for qf in sorted(mentor_dir.glob("*.json")):
                with open(qf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                mentor = data.get("mentor", mentor_dir.name)
                category = data.get("category", qf.stem)
                for q in data.get("quotes", []):
                    q["_mentor"] = mentor
                    q["_category"] = category
                    quotes.append(q)
    return quotes


def load_mentors() -> dict:
    with open(DATA_DIR / "mentors.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {m["id"]: m for m in data["mentors"]}


def load_categories() -> dict:
    with open(DATA_DIR / "categories.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["id"]: c for c in data["categories"]}


def export_rag(quotes: list[dict], mentors: dict, categories: dict):
    """Export as RAG-friendly JSONL chunks."""
    EXPORT_DIR.mkdir(exist_ok=True)
    output = EXPORT_DIR / "rag_chunks.jsonl"

    with open(output, "w", encoding="utf-8") as f:
        for q in quotes:
            mentor = mentors.get(q["_mentor"], {})
            cat = categories.get(q["_category"], {})
            mentor_name = mentor.get("name_zh", q["_mentor"])
            cat_name = cat.get("name_zh", q["_category"])

            # Build rich text chunk
            text_parts = [
                f"【{mentor_name}·{cat_name}】",
                q["text"],
            ]
            if q.get("context"):
                text_parts.append(f"（背景：{q['context']}）")
            if q.get("related_majors"):
                text_parts.append(f"相关专业：{'、'.join(q['related_majors'])}")

            chunk = {
                "id": q["id"],
                "text": " ".join(text_parts),
                "metadata": {
                    "mentor": mentor_name,
                    "category": cat_name,
                    "tags": q.get("tags", []),
                    "sentiment": q.get("sentiment", ""),
                    "confidence": q.get("confidence", ""),
                    "target_audience": q.get("target_audience", []),
                },
            }
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Exported {len(quotes)} RAG chunks to {output}")


def export_finetune(quotes: list[dict], mentors: dict, categories: dict):
    """Export as fine-tuning Q&A pairs."""
    EXPORT_DIR.mkdir(exist_ok=True)
    output = EXPORT_DIR / "fine_tune.jsonl"

    with open(output, "w", encoding="utf-8") as f:
        for q in quotes:
            mentor = mentors.get(q["_mentor"], {})
            cat = categories.get(q["_category"], {})
            mentor_name = mentor.get("name_zh", q["_mentor"])

            # Generate a natural question
            tags_str = "、".join(q.get("tags", [])[:3])
            question = f"关于{tags_str}，{mentor_name}老师怎么说？"

            answer_parts = [q["text"]]
            if q.get("context"):
                answer_parts.append(f"（{q['context']}）")

            pair = {
                "messages": [
                    {
                        "role": "system",
                        "content": f"你是一个高考志愿填报助手，基于{mentor_name}老师的建议回答问题。",
                    },
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": " ".join(answer_parts)},
                ]
            }
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"Exported {len(quotes)} fine-tuning pairs to {output}")


def main():
    parser = argparse.ArgumentParser(description="Export quotes for AI training")
    parser.add_argument(
        "--format",
        choices=["rag", "fine-tune", "both"],
        default="both",
        help="Export format (default: both)",
    )
    args = parser.parse_args()

    quotes = load_all_quotes()
    mentors = load_mentors()
    categories = load_categories()

    print(f"Loaded {len(quotes)} quotes")

    if args.format in ("rag", "both"):
        export_rag(quotes, mentors, categories)
    if args.format in ("fine-tune", "both"):
        export_finetune(quotes, mentors, categories)

    print("Done!")


if __name__ == "__main__":
    main()
