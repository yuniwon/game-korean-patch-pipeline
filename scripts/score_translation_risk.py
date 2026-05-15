#!/usr/bin/env python3
"""Score translation rows for playtest and review risk."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"%\w|\{[^}]+\}")
TAG_RE = re.compile(r"<[^>]+>")
TITLE_CASE_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Assign heuristic risk scores to translation rows from TSV or JSON input."
    )
    parser.add_argument("--input", required=True, help="Input TSV or JSON file.")
    parser.add_argument(
        "--text-column",
        default="source_text",
        help="Column containing the source text (default: source_text).",
    )
    parser.add_argument(
        "--path-column",
        default="path",
        help="Column containing the source path or category hint (default: path).",
    )
    parser.add_argument(
        "--format",
        choices=("tsv", "json"),
        default="tsv",
        help="Output format (default: tsv).",
    )
    parser.add_argument("--out", help="Optional output file. Prints to stdout if omitted.")
    return parser


def load_rows(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("rows", [])
        return [{key: str(value) for key, value in item.items()} for item in data]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: str(value) for key, value in row.items()} for row in reader]


def score_row(row: dict[str, str], text_column: str, path_column: str) -> tuple[int, str]:
    text = row.get(text_column, "")
    path_hint = row.get(path_column, "").lower()
    score = 0
    reasons: list[str] = []
    ui_hint = any(token in path_hint for token in ("ui", "menu", "hud", "setting", "button", "option"))

    if PLACEHOLDER_RE.search(text):
        score += 25
        reasons.append("placeholders")
    if TAG_RE.search(text):
        score += 20
        reasons.append("rich-text-tags")
    if "\n" in text or "\\n" in text:
        score += 10
        reasons.append("line-breaks")
    if len(text) >= 120:
        score += 10
        reasons.append("long-text")
    if len(text.strip()) <= 12 and ui_hint:
        score += 8
        reasons.append("short-ui-like")
    if TITLE_CASE_RE.search(text):
        score += 12
        reasons.append("proper-nouns")
    if any(token in path_hint for token in ("dialog", "quest", "subtitle")):
        score += 18
        reasons.append("narrative-domain")
    if any(token in path_hint for token in ("item", "recipe", "craft")):
        score += 10
        reasons.append("item-domain")
    if ui_hint:
        score += 6
        reasons.append("ui-domain")

    if score >= 50:
        level = "high"
    elif score >= 20:
        level = "medium"
    else:
        level = "low"
    return score, ",".join(reasons)


def render_json(rows: list[dict[str, str]]) -> str:
    payload = {"rows": rows}
    return json.dumps(payload, indent=2, ensure_ascii=True)


def render_tsv(rows: list[dict[str, str]]) -> str:
    fieldnames = list(rows[0]) if rows else []
    lines = ["\t".join(fieldnames)]
    for row in rows:
        lines.append("\t".join(row.get(name, "").replace("\t", " ").replace("\n", "\\n") for name in fieldnames))
    return "\n".join(lines)


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()
    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        parser.error(f"Input file does not exist: {input_path}")

    rows = load_rows(input_path)
    enriched: list[dict[str, str]] = []
    for row in rows:
        score, reasons = score_row(row, args.text_column, args.path_column)
        enriched_row = dict(row)
        enriched_row["risk_score"] = str(score)
        enriched_row["risk_level"] = "high" if score >= 50 else "medium" if score >= 20 else "low"
        enriched_row["risk_reasons"] = reasons
        enriched.append(enriched_row)

    output = render_json(enriched) if args.format == "json" else render_tsv(enriched)
    if args.out:
        Path(args.out).write_text(output + ("\n" if not output.endswith("\n") else ""), encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
