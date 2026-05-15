#!/usr/bin/env python3
"""Detect a probable game engine from a local game directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ENGINE_RULES = {
    "unity": {
        "markers": {
            "UnityPlayer.dll": 35,
            "GameAssembly.dll": 25,
            "_Data": 20,
            "globalgamemanagers": 15,
            "resources.assets": 15,
            "StreamingAssets": 15,
        },
        "adapter": "adapter-unity.md",
    },
    "unreal": {
        "markers": {
            ".uproject": 35,
            ".pak": 20,
            ".utoc": 20,
            ".ucas": 20,
            ".locres": 20,
            "Content": 15,
            "Localization": 15,
        },
        "adapter": "adapter-unreal.md",
    },
    "renpy": {
        "markers": {
            "renpy": 40,
            ".rpa": 25,
            "game": 10,
            "script.rpy": 30,
        },
        "adapter": "adapter-table-files.md",
    },
    "rpg-maker": {
        "markers": {
            "www": 25,
            "data": 15,
            "js": 15,
            "System.json": 25,
            "MapInfos.json": 25,
        },
        "adapter": "adapter-table-files.md",
    },
    "nwjs": {
        "markers": {
            "nw.pak": 35,
            "package.nw": 35,
            "package.json": 10,
            "www": 10,
        },
        "adapter": "adapter-table-files.md",
    },
    "godot": {
        "markers": {
            ".pck": 25,
            "project.godot": 40,
        },
        "adapter": "adapter-table-files.md",
    },
    "gamemaker": {
        "markers": {
            "data.win": 40,
            ".yy": 20,
        },
        "adapter": "adapter-table-files.md",
    },
}

TEXT_EXTENSIONS = {".json", ".csv", ".tsv", ".xml", ".po", ".txt", ".yml", ".yaml"}


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect a probable game engine and patching risk from a local workspace."
    )
    parser.add_argument("root", help="Game root directory to inspect.")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum directory depth to scan below the root (default: 3).",
    )
    parser.add_argument("--out", help="Optional output path. Prints JSON to stdout if omitted.")
    return parser


def iter_paths(root: Path, max_depth: int) -> list[Path]:
    results: list[Path] = []
    for path in root.rglob("*"):
        try:
            depth = len(path.relative_to(root).parts)
        except ValueError:
            continue
        if depth <= max_depth:
            results.append(path)
    return sorted(results, key=lambda item: str(item).lower())


def collect_evidence(root: Path, max_depth: int) -> dict[str, object]:
    scan_paths = iter_paths(root, max_depth)
    scores = {engine: 0 for engine in ENGINE_RULES}
    clues: dict[str, list[dict[str, object]]] = {engine: [] for engine in ENGINE_RULES}
    structured_files = 0

    for path in scan_paths:
        relative = path.relative_to(root).as_posix()
        basename = path.name
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            structured_files += 1
        for engine, rule in ENGINE_RULES.items():
            for marker, weight in rule["markers"].items():
                if marker.startswith("."):
                    matched = path.is_file() and path.suffix.lower() == marker.lower()
                else:
                    matched = marker.lower() == basename.lower() or marker.lower() in relative.lower()
                if matched:
                    scores[engine] += int(weight)
                    clues[engine].append(
                        {
                            "path": relative,
                            "marker": marker,
                            "weight": weight,
                        }
                    )

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    detected_engine, best_score = ranked[0]
    confidence = "low"
    if best_score >= 60:
        confidence = "high"
    elif best_score >= 30:
        confidence = "medium"
    if best_score == 0:
        detected_engine = "unknown"

    risk = "high"
    if structured_files and confidence in {"medium", "high"}:
        risk = "medium"
    if structured_files >= 5 and detected_engine in {"unknown", "renpy", "rpg-maker", "nwjs", "godot"}:
        risk = "low"

    return {
        "root": str(root),
        "detected_engine": detected_engine,
        "confidence": confidence,
        "score": best_score,
        "structured_text_files_seen": structured_files,
        "suggested_adapter": ENGINE_RULES.get(detected_engine, {}).get("adapter", "adapter-table-files.md"),
        "patching_risk": risk,
        "ranked_candidates": [
            {"engine": engine, "score": score} for engine, score in ranked if score > 0
        ],
        "evidence": clues.get(detected_engine, []),
    }


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"Root directory does not exist: {root}")
    report = collect_evidence(root, args.max_depth)
    output = json.dumps(report, indent=2, ensure_ascii=True)
    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
