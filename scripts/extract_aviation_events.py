#!/usr/bin/env python3
"""Extract the U.S. aviation-terrorism subset from the START GTD 2018 snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

SOURCE_URL = "https://archive.org/download/globalterrorismdb_0718dist/globalterrorismdb_0718dist.csv"
SOURCE_SHA256 = "a60070ab13f72f87d0c4e96f45752fa7ed8a13f5449a01f8b293cdf135fa5a27"
START_DATASET_URL = "https://www.start.umd.edu/gtd-download"
KAGGLE_SNAPSHOT_URL = "https://www.kaggle.com/START-UMD/gtd/metadata"

AVIATION_TARGET_TYPES = {"Airports & Aircraft", "Airports & Airlines"}
AVIATION_WORDS = {
    "airline",
    "airlines",
    "airways",
    "aircraft",
    "airliner",
    "flight",
    "plane",
    "jet",
    "boeing",
    "airport",
}

OUTPUT_FIELDS = [
    "eventid",
    "year",
    "month",
    "day",
    "state",
    "city",
    "attack_types",
    "target_types",
    "target",
    "organization",
    "gtd_nkill",
    "filter_reason",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def joined(row: dict[str, str], prefix: str) -> str:
    values = []
    for index in (1, 2, 3):
        value = (row.get(f"{prefix}{index}_txt") or "").strip()
        if value and value != "." and value not in values:
            values.append(value)
    return " | ".join(values)


def aviation_hijacking(row: dict[str, str], attack_types: list[str]) -> bool:
    if "Hijacking" not in attack_types:
        return False
    text = " ".join(
        (row.get(key) or "")
        for key in (
            "corp1",
            "target1",
            "summary",
            "corp2",
            "target2",
            "corp3",
            "target3",
        )
    ).lower()
    return any(word in text for word in AVIATION_WORDS)


def selected_row(row: dict[str, str]) -> dict[str, str] | None:
    year = int(row["iyear"])
    if row["country_txt"] != "United States" or not (1970 <= year <= 2001):
        return None

    target_types = [
        (row.get(f"targtype{index}_txt") or "").strip()
        for index in (1, 2, 3)
    ]
    attack_types = [
        (row.get(f"attacktype{index}_txt") or "").strip()
        for index in (1, 2, 3)
        if (row.get(f"attacktype{index}_txt") or "").strip()
    ]

    aviation_target = any(value in AVIATION_TARGET_TYPES for value in target_types)
    hijacking = aviation_hijacking(row, attack_types)
    if not (aviation_target or hijacking):
        return None

    reason = "airport_or_aircraft_target" if aviation_target else "aviation_hijacking"
    return {
        "eventid": row["eventid"],
        "year": row["iyear"],
        "month": row["imonth"],
        "day": row["iday"],
        "state": row["provstate"],
        "city": row["city"],
        "attack_types": joined(row, "attacktype"),
        "target_types": joined(row, "targtype"),
        "target": row["target1"],
        "organization": row["corp1"],
        "gtd_nkill": row["nkill"],
        "filter_reason": reason,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("gtd_csv", type=Path)
    args = parser.parse_args()

    actual_hash = sha256(args.gtd_csv)
    if actual_hash != SOURCE_SHA256:
        raise SystemExit(
            f"unexpected GTD snapshot sha256: {actual_hash}; expected {SOURCE_SHA256}"
        )

    writer = csv.DictWriter(sys.stdout, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
    writer.writeheader()
    with args.gtd_csv.open(newline="", encoding="latin1", errors="replace") as handle:
        for row in csv.DictReader(handle):
            selected = selected_row(row)
            if selected is not None:
                writer.writerow(selected)


if __name__ == "__main__":
    main()
