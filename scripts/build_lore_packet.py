#!/usr/bin/env python3
"""Build a markdown lore packet from structured facts and glossary inputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


SECTION_ORDER = [
    "summary",
    "setting",
    "factions",
    "characters",
    "locations",
    "systems",
    "open_questions",
]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a lore packet markdown file from facts and optional glossary input."
    )
    parser.add_argument("--game-title", required=True, help="Game title.")
    parser.add_argument("--genre", default="", help="Optional genre.")
    parser.add_argument("--tone", default="", help="Optional tone description.")
    parser.add_argument(
        "--facts-json",
        help="Optional JSON file containing a list of facts with section/name/summary/evidence/confidence.",
    )
    parser.add_argument(
        "--glossary-tsv",
        help="Optional glossary TSV with source_term and preferred_ko columns.",
    )
    parser.add_argument("--out", help="Optional output markdown path. Prints to stdout if omitted.")
    return parser


def load_facts(path: str | None) -> list[dict[str, str]]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("facts", [])
    if not isinstance(data, list):
        raise ValueError("Facts JSON must contain a list or an object with a 'facts' list.")
    facts: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        facts.append({key: str(value) for key, value in item.items()})
    return facts


def load_glossary(path: str | None) -> list[dict[str, str]]:
    if not path:
        return []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: str(value) for key, value in row.items()} for row in reader]


def render_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["| Name | Summary | Evidence | Confidence |", "|---|---|---|---|", "|  |  |  |  |"]
    lines = ["| Name | Summary | Evidence | Confidence |", "|---|---|---|---|"]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("\n", " ").strip() for cell in row) + " |")
    return lines


def build_markdown(title: str, genre: str, tone: str, facts: list[dict[str, str]], glossary: list[dict[str, str]]) -> str:
    grouped: dict[str, list[list[str]]] = defaultdict(list)
    for fact in facts:
        section = fact.get("section", "setting").strip().lower().replace(" ", "_")
        grouped[section].append(
            [
                fact.get("name", ""),
                fact.get("summary", ""),
                fact.get("evidence", ""),
                fact.get("confidence", ""),
            ]
        )

    lines = [
        "# Lore Packet",
        "",
        "## Game Summary",
        "",
        f"- Title: {title}",
        f"- Genre: {genre or 'unknown'}",
        f"- Tone: {tone or 'unknown'}",
        "",
        "## Setting",
        "",
    ]
    setting_rows = grouped.get("setting") or grouped.get("summary")
    if setting_rows:
        lines.extend(render_table(setting_rows))
    else:
        lines.append("- Add the world premise, era, and core conflict here.")

    headings = {
        "factions": "Factions",
        "characters": "Characters",
        "locations": "Locations",
        "systems": "Systems And Item Families",
        "open_questions": "Open Questions",
    }
    for key in SECTION_ORDER:
        if key not in headings:
            continue
        lines.extend(["", f"## {headings[key]}", ""])
        if key == "open_questions":
            if grouped.get(key):
                for row in grouped[key]:
                    lines.append(f"- {row[1] or row[0]}")
            else:
                lines.append("- Record unresolved naming, lore, and tone questions.")
            continue
        lines.extend(render_table(grouped.get(key, [])))

    lines.extend(["", "## Glossary Seeds", ""])
    if glossary:
        lines.append("| Source | Preferred Korean | Status | Notes |")
        lines.append("|---|---|---|---|")
        for row in glossary[:20]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        row.get("source_term", ""),
                        row.get("preferred_ko", ""),
                        row.get("status", ""),
                        row.get("notes", ""),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| Source | Preferred Korean | Status | Notes |")
        lines.append("|---|---|---|---|")
        lines.append("|  |  |  |  |")

    return "\n".join(lines)


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()
    facts = load_facts(args.facts_json)
    glossary = load_glossary(args.glossary_tsv)
    output = build_markdown(args.game_title, args.genre, args.tone, facts, glossary)
    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
