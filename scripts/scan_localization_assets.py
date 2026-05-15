#!/usr/bin/env python3
"""Scan a game directory for candidate localization assets."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STRUCTURED_EXTENSIONS = {
    ".json",
    ".csv",
    ".tsv",
    ".xml",
    ".txt",
    ".po",
    ".ini",
    ".yml",
    ".yaml",
}
SPREADSHEET_EXTENSIONS = {".xlsx"}
BINARY_EXTENSIONS = {".locres", ".uasset", ".bundle", ".assets", ".bytes", ".pak", ".utoc", ".ucas"}
NON_ASSET_EXTENSIONS = {
    ".py",
    ".pyc",
    ".ps1",
    ".bat",
    ".cmd",
    ".md",
    ".rst",
    ".log",
    ".dll",
    ".exe",
    ".so",
    ".dylib",
}
KEYWORDS = [
    "local",
    "lang",
    "string",
    "text",
    "dialog",
    "dialogue",
    "quest",
    "ui",
    "item",
    "tutorial",
    "subtitle",
    "translate",
]
EXCLUDE_NAME_KEYWORDS = {
    "audit",
    "report",
    "log",
    "cache",
    "manifest",
    "progress",
    "catalog",
    "dashboard",
    "metric",
    "metrics",
    "snapshot",
    "backup",
    "freeze",
    "verify",
    "quality",
    "gate",
}
IGNORE_DIR_NAMES = {
    "__pycache__",
    ".git",
    ".hg",
    ".svn",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    ".codex",
    ".claude",
    ".sisyphus",
    ".bkit",
    "node_modules",
    "docs",
    "tests",
    "logs",
    "_tmp",
    "tmp",
    "temp",
}
IGNORE_DIR_PREFIXES = ("archive", "backup", "release", "history", "report", "prompt")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory likely localization assets and output JSON or TSV."
    )
    parser.add_argument("root", help="Game root directory to scan.")
    parser.add_argument(
        "--format",
        choices=("json", "tsv"),
        default="json",
        help="Output format (default: json).",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=6,
        help="Maximum directory depth below the root to scan (default: 6).",
    )
    parser.add_argument("--out", help="Optional output file. Prints to stdout if omitted.")
    return parser


def category_from_path(relative_path: str) -> str:
    lowered = relative_path.lower()
    if any(token in lowered for token in ("dialog", "subtitle", "voice")):
        return "Dialogue"
    if any(token in lowered for token in ("quest", "mission")):
        return "Quest"
    if any(token in lowered for token in ("item", "recipe", "inventory", "craft")):
        return "Item"
    if any(token in lowered for token in ("tutorial", "help", "guide")):
        return "Tutorial"
    if any(token in lowered for token in ("ui", "menu", "hud", "setting")):
        return "UI"
    if any(token in lowered for token in ("system", "error", "notice", "message")):
        return "System"
    return "Other"


def risk_for_file(extension: str, category: str) -> str:
    if extension in BINARY_EXTENSIONS:
        return "high"
    if category in {"Dialogue", "Quest"}:
        return "high"
    if category in {"Item", "Tutorial"}:
        return "medium"
    return "low"


def kind_for_extension(extension: str) -> str:
    if extension in STRUCTURED_EXTENSIONS:
        return "structured-text"
    if extension in SPREADSHEET_EXTENSIONS:
        return "spreadsheet"
    if extension in BINARY_EXTENSIONS:
        return "binary-asset"
    return "other"


def iter_files(root: Path, max_depth: int) -> list[Path]:
    results: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(
            part in IGNORE_DIR_NAMES
            or part.startswith(".")
            or part.lower().startswith(IGNORE_DIR_PREFIXES)
            for part in relative_parts[:-1]
        ):
            continue
        depth = len(relative_parts)
        if depth <= max_depth:
            results.append(path)
    return sorted(results, key=lambda item: str(item).lower())


def is_candidate(relative_path: str, extension: str) -> bool:
    lowered = relative_path.lower()
    basename = Path(relative_path).name.lower()
    if extension in NON_ASSET_EXTENSIONS:
        return False
    if any(keyword in basename for keyword in EXCLUDE_NAME_KEYWORDS):
        return False
    return (
        extension in STRUCTURED_EXTENSIONS
        or extension in SPREADSHEET_EXTENSIONS
        or extension in BINARY_EXTENSIONS
        or any(keyword in lowered for keyword in KEYWORDS)
    )


def summarize_head(path: Path) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return handle.readline().strip()[:120]
    except OSError:
        return ""


def scan(root: Path, max_depth: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in iter_files(root, max_depth):
        relative = path.relative_to(root).as_posix()
        extension = path.suffix.lower()
        if not is_candidate(relative, extension):
            continue
        category = category_from_path(relative)
        reasons = []
        if extension:
            reasons.append(f"extension={extension}")
        for keyword in KEYWORDS:
            if keyword in relative.lower():
                reasons.append(f"keyword={keyword}")
        rows.append(
            {
                "path": relative,
                "extension": extension or "<none>",
                "kind": kind_for_extension(extension),
                "category_guess": category,
                "risk_level": risk_for_file(extension, category),
                "head_sample": summarize_head(path),
                "reasons": ";".join(sorted(set(reasons))),
            }
        )
    return rows


def render_json(root: Path, rows: list[dict[str, str]]) -> str:
    payload = {
        "root": str(root),
        "asset_count": len(rows),
        "assets": rows,
    }
    return json.dumps(payload, indent=2, ensure_ascii=True)


def render_tsv(rows: list[dict[str, str]]) -> str:
    fieldnames = ["path", "extension", "kind", "category_guess", "risk_level", "head_sample", "reasons"]
    lines = ["\t".join(fieldnames)]
    for row in rows:
        lines.append("\t".join(row[name].replace("\t", " ").replace("\n", " ") for name in fieldnames))
    return "\n".join(lines)


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"Root directory does not exist: {root}")
    rows = scan(root, args.max_depth)
    output = render_json(root, rows) if args.format == "json" else render_tsv(rows)
    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
