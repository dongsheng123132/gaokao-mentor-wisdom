#!/usr/bin/env python3
"""Generate Markdown documentation from JSON quote data."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"


def load_categories() -> dict:
    with open(DATA_DIR / "categories.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["id"]: c for c in data["categories"]}


def load_mentors() -> dict:
    with open(DATA_DIR / "mentors.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {m["id"]: m for m in data["mentors"]}


def generate_mentor_docs(mentor: dict, categories: dict):
    mentor_dir = DATA_DIR / mentor["data_dir"]
    docs_mentor_dir = DOCS_DIR / mentor["data_dir"]
    docs_mentor_dir.mkdir(parents=True, exist_ok=True)

    if not mentor_dir.exists():
        print(f"  Skipping {mentor['name_zh']}: data dir not found")
        return

    total = 0
    file_summaries = []

    for qf in sorted(mentor_dir.glob("*.json")):
        with open(qf, "r", encoding="utf-8") as f:
            data = json.load(f)

        cat_id = data.get("category", qf.stem)
        cat = categories.get(cat_id, {})
        cat_name = cat.get("name_zh", cat_id)
        cat_icon = cat.get("icon", "")
        quotes = data.get("quotes", [])
        total += len(quotes)

        # Generate category markdown
        lines = [
            f"# {cat_icon} {cat_name} — {mentor['name_zh']}",
            "",
            f"> {cat.get('description', '')}",
            "",
            f"共 {len(quotes)} 条语录",
            "",
            "---",
            "",
        ]

        for i, q in enumerate(quotes, 1):
            lines.append(f"## {i}. {q['id']}")
            lines.append("")
            lines.append(f"> {q['text']}")
            lines.append("")
            if q.get("text_en"):
                lines.append(f"*{q['text_en']}*")
                lines.append("")
            if q.get("context"):
                lines.append(f"**背景**: {q['context']}")
                lines.append("")
            lines.append(f"**标签**: {', '.join(q.get('tags', []))}")
            if q.get("related_majors"):
                lines.append(f"**相关专业**: {', '.join(q['related_majors'])}")
            src = q.get("source", {})
            src_parts = []
            if src.get("platform"):
                src_parts.append(src["platform"])
            if src.get("type"):
                src_parts.append(src["type"])
            if src.get("date"):
                src_parts.append(src["date"])
            if src_parts:
                lines.append(f"**来源**: {' / '.join(src_parts)}")
            if q.get("sentiment"):
                lines.append(f"**语气**: {q['sentiment']}")
            if q.get("confidence"):
                lines.append(f"**可信度**: {q['confidence']}")
            lines.append("")
            lines.append("---")
            lines.append("")

        md_path = docs_mentor_dir / f"{qf.stem}.md"
        md_path.write_text("\n".join(lines), encoding="utf-8")
        file_summaries.append((cat_icon, cat_name, qf.stem, len(quotes)))
        print(f"  Generated: {md_path.relative_to(ROOT)} ({len(quotes)} quotes)")

    # Update index
    index_lines = [
        f"# {mentor['name_zh']}语录总览",
        "",
        f"> {mentor.get('bio', '')}",
        "",
        "## 分类统计",
        "",
        "| 分类 | 数量 | 文档 |",
        "|---|---|---|",
    ]
    for icon, name, stem, count in file_summaries:
        index_lines.append(f"| {icon} {name} | {count} | [{stem}.md]({stem}.md) |")
    index_lines.append(f"| **总计** | **{total}** | |")
    index_lines.append("")

    index_path = docs_mentor_dir / "index.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    print(f"  Generated: {index_path.relative_to(ROOT)}")


def main():
    categories = load_categories()
    mentors = load_mentors()

    print("Generating Markdown docs...")
    for mentor in mentors.values():
        print(f"\n{mentor['name_zh']}:")
        generate_mentor_docs(mentor, categories)

    print("\nDone!")


if __name__ == "__main__":
    main()
