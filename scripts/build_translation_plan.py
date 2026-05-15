#!/usr/bin/env python3
"""Build a markdown translation plan from an asset inventory."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ORDER = ["UI", "System", "Tutorial", "Item", "Quest", "Dialogue", "Other"]
RISK_RANK = {"low": 1, "medium": 2, "high": 3}


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a category-based translation plan from an asset inventory."
    )
    parser.add_argument("--inventory", required=True, help="Input inventory file in JSON or TSV format.")
    parser.add_argument("--game-title", default="", help="Optional game title for the plan header.")
    parser.add_argument("--out", help="Optional markdown output path. Prints to stdout if omitted.")
    return parser


def load_inventory(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("assets", [])
        return [{key: str(value) for key, value in item.items()} for item in data]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: str(value) for key, value in row.items()} for row in reader]


def summarize(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    grouped: dict[str, dict[str, object]] = defaultdict(
        lambda: {"count": 0, "paths": [], "risk": "low", "kinds": set()}
    )
    for row in rows:
        category = row.get("category_guess", "Other") or "Other"
        bucket = grouped[category]
        bucket["count"] = int(bucket["count"]) + 1
        bucket["paths"].append(row.get("path", ""))
        risk = row.get("risk_level", "low")
        if RISK_RANK.get(risk, 1) > RISK_RANK.get(str(bucket["risk"]), 1):
            bucket["risk"] = risk
        bucket["kinds"].add(row.get("kind", "unknown"))
    return grouped


def recommended_order(categories: list[str]) -> list[str]:
    seen = set(categories)
    ordered = [category for category in ORDER if category in seen]
    ordered.extend(sorted(seen - set(ORDER)))
    return ordered


def render_markdown(game_title: str, rows: list[dict[str, str]]) -> str:
    grouped = summarize(rows)
    ordered = recommended_order(list(grouped))
    lines = [
        "# Translation Plan",
        "",
        f"- Game: {game_title or 'unknown'}",
        f"- Source assets: {len(rows)}",
        "- Human role: tester-first",
        "",
        "## Category Summary",
        "",
        "| Category | Assets | Highest risk | Dominant kinds |",
        "|---|---:|---|---|",
    ]
    for category in ordered:
        bucket = grouped[category]
        kinds = ", ".join(sorted(str(kind) for kind in bucket["kinds"]))
        lines.append(f"| {category} | {bucket['count']} | {bucket['risk']} | {kinds} |")

    lines.extend(
        [
            "",
            "## Recommended Execution Order",
            "",
        ]
    )
    for index, category in enumerate(ordered, start=1):
        lines.append(f"{index}. {category}")

    lines.extend(
        [
            "",
            "## Batch Notes",
            "",
            "- Keep categories separate unless the inventory is too small to justify dedicated batches.",
            "- Treat Dialogue and Quest as high-risk domains that need stronger glossary and lore context.",
            "- Reuse duplicate strings within the same category before translating unique rows.",
            "- Do not package original game assets until structural QA passes.",
            "",
            "## Category Details",
            "",
        ]
    )
    for category in ordered:
        bucket = grouped[category]
        sample_paths = sorted(str(path) for path in bucket["paths"])[:5]
        lines.extend([f"### {category}", "", f"- Asset count: {bucket['count']}", f"- Highest risk: {bucket['risk']}", "- Sample paths:"])
        for sample_path in sample_paths:
            lines.append(f"  - {sample_path}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()
    inventory_path = Path(args.inventory).expanduser().resolve()
    if not inventory_path.exists():
        parser.error(f"Inventory file does not exist: {inventory_path}")
    rows = load_inventory(inventory_path)
    output = render_markdown(args.game_title, rows)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
