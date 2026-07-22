#!/usr/bin/env python3
"""Normalize an eval run's output into a failures-only JSONL file for triage.

Reads a JSONL/JSON/CSV file of eval records, auto-detects the input,
prediction, gold-label, and pass/score columns from common naming
conventions, and writes only the FAILING rows (normalized to a common
shape) as JSONL. Stdlib only — no dependencies required.

Usage:
    python3 normalize_eval.py results.jsonl -o failures.jsonl
    python3 normalize_eval.py results.csv --score-field score --score-threshold 0.5 -o failures.jsonl
    python3 normalize_eval.py results.json --pass-field passed -o failures.jsonl
"""
import argparse
import csv
import json
import sys
from pathlib import Path

INPUT_KEYS = ["input", "prompt", "query", "question", "text"]
PREDICTION_KEYS = ["prediction", "output", "response", "actual", "answer", "generated"]
GOLD_KEYS = ["gold", "expected", "label", "ground_truth", "reference", "target"]
PASS_KEYS = ["pass", "passed", "correct", "success", "is_correct"]
SCORE_KEYS = ["score", "similarity", "confidence"]
ID_KEYS = ["id", "row_id", "index", "idx"]


def load_records(path):
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        with path.open() as f:
            return [json.loads(line) for line in f if line.strip()]
    if suffix == ".json":
        data = json.loads(path.read_text())
        if isinstance(data, list):
            return data
        for key in ("results", "records", "rows", "data"):
            if isinstance(data.get(key), list):
                return data[key]
        raise ValueError("Could not find a list of records in this JSON file's top level or under results/records/rows/data.")
    if suffix == ".csv":
        with path.open(newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported file type: {suffix} (expected .jsonl, .json, or .csv)")


def find_key(record, candidates, override=None):
    if override:
        return override if override in record else None
    for key in candidates:
        if key in record:
            return key
    return None


def is_failure(record, pass_key, score_key, threshold):
    if pass_key:
        val = record[pass_key]
        if isinstance(val, str):
            val = val.strip().lower() in ("true", "1", "yes", "pass")
        return not bool(val)
    if score_key:
        try:
            return float(record[score_key]) < threshold
        except (TypeError, ValueError):
            return False
    return None  # unknown — caller decides how to proceed


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--pass-field", help="Field name holding a boolean pass/fail result")
    parser.add_argument("--score-field", help="Field name holding a numeric score")
    parser.add_argument("--score-threshold", type=float, default=1.0, help="Rows scoring below this are failures (default: 1.0)")
    parser.add_argument("--input-field", help="Override auto-detected input field")
    parser.add_argument("--prediction-field", help="Override auto-detected prediction field")
    parser.add_argument("--gold-field", help="Override auto-detected gold-label field")
    args = parser.parse_args()

    records = load_records(args.input_path)
    if not records:
        print("No records found in input file.", file=sys.stderr)
        sys.exit(1)

    sample = records[0]
    input_key = find_key(sample, INPUT_KEYS, args.input_field)
    pred_key = find_key(sample, PREDICTION_KEYS, args.prediction_field)
    gold_key = find_key(sample, GOLD_KEYS, args.gold_field)
    pass_key = find_key(sample, PASS_KEYS, args.pass_field)
    score_key = find_key(sample, SCORE_KEYS, args.score_field)
    id_key = find_key(sample, ID_KEYS)

    if not pass_key and not score_key:
        print(
            "No pass/fail or score field detected or specified.\n"
            "Available fields: " + ", ".join(sample.keys()) + "\n"
            "Pass --pass-field NAME or --score-field NAME (with --score-threshold) to tell this script how to identify failures.",
            file=sys.stderr,
        )
        sys.exit(2)

    failures = []
    for i, record in enumerate(records):
        failed = is_failure(record, pass_key, score_key, args.score_threshold)
        if failed:
            failures.append({
                "id": record.get(id_key, i) if id_key else i,
                "input": record.get(input_key) if input_key else None,
                "prediction": record.get(pred_key) if pred_key else None,
                "gold": record.get(gold_key) if gold_key else None,
                "score": record.get(score_key) if score_key else None,
                "raw": record,
            })

    args.output.write_text("\n".join(json.dumps(f) for f in failures) + ("\n" if failures else ""))
    print(
        f"{len(failures)}/{len(records)} rows failed "
        f"(input={input_key!r} prediction={pred_key!r} gold={gold_key!r} "
        f"pass={pass_key!r} score={score_key!r}) -> {args.output}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
