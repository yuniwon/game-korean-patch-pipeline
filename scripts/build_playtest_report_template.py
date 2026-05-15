#!/usr/bin/env python3
"""Build a TSV playtest report template for translated game builds."""

from __future__ import annotations

import argparse
from pathlib import Path


COLUMNS = [
    "issue_id",
    "severity",
    "area",
    "location",
    "source_text",
    "current_ko",
    "issue_type",
    "symptom",
    "reproduction",
    "suggested_fix",
    "status",
    "notes",
]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic TSV template for Korean localization playtesting."
    )
    parser.add_argument("--out", required=True, help="Output TSV path.")
    parser.add_argument("--seed-id", default="PT-001", help="Example first issue id (default: PT-001).")
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()
    lines = [
        "\t".join(COLUMNS),
        "\t".join(
            [
                args.seed_id,
                "medium",
                "UI",
                "Main Menu",
                "Start Game",
                "Game Start",
                "wording",
                "Awkward phrasing during playtest",
                "Open the title screen",
                "Use a natural Korean label",
                "open",
                "",
            ]
        ),
    ]
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
