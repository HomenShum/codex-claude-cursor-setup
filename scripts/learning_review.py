#!/usr/bin/env python3
"""Inspect saved learning outputs with the existing comparator; never activate."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import sys

from bootstrap_learning import compare, pairs
from path_safety import read_regular_file_bounded


def load_input(path):
    raw = read_regular_file_bounded(path, 2_000_000, boundary=Path(path).absolute().anchor)
    value = json.loads(raw, object_pairs_hook=pairs,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
    return value, {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def inspect(policy_path, baseline_path, candidate_path):
    inputs = [load_input(p) for p in (policy_path, baseline_path, candidate_path)]
    policy, baseline, candidate = [value for value, _ in inputs]
    result = compare(policy, baseline, candidate)
    right = {case["id"]: case for case in candidate["cases"]}
    rows = []
    for case in baseline["cases"]:
        other = right[case["id"]]
        rows.append({"case": case["id"], "split": case["split"],
                     "gates": {key: [grade["value"], other["gates"][key]["value"]]
                               for key, grade in case["gates"].items()},
                     "scores": {key: [grade["value"], other["scores"][key]["value"]]
                                for key, grade in case["scores"].items()}})
    sources = dict(zip(("policy", "baseline", "candidate"), [receipt for _, receipt in inputs]))
    event = {"type": "EVAL_COMPLETED", "actor": "saved-output-comparator",
             "summary": f"Saved-output comparison: {result['verdict']}; {len(rows)} cases; synthetic={result['synthetic']}. No activation.",
             "next_action": "Independently verify source authenticity, calibration, heldout isolation and human acceptance.",
             "failed_gates": ["numerical-comparison"] if result["verdict"] == "REJECT" else [],
             "evidence": [f"{name}:sha256:{receipt['sha256']}" for name, receipt in sources.items()]}
    return {"schema_version": 1, "kind": "learning-review", "mode": "SAVED_OUTPUT_COMPARISON",
            "comparison": result, "sources": sources, "rows": rows, "event": event,
            "model_calls_by_this_command": 0, "input_run_cost": "UNMEASURED"}


def render(report):
    escape = lambda value: html.escape(str(value))
    result = report["comparison"]
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">',
             '<title>Saved-output learning review</title><style>',
             'body{font:16px/1.5 system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#182430;background:#f6f8fb}',
             'table{border-collapse:collapse;width:100%;table-layout:fixed;background:white}th,td{padding:.65rem;border:1px solid #cbd5e1;text-align:left;overflow-wrap:anywhere}',
             'code{overflow-wrap:anywhere}h1{font-size:1.8rem}.verdict{font-weight:700;font-size:1.3rem}.notice{border-left:4px solid #546ba8;padding:1rem;background:#e8edf7}',
             '</style><h1>Saved-output learning review</h1>',
             f'<p class="verdict">{escape(result["verdict"])}</p>',
             '<p class="notice">No activation authority. This compares saved outputs; it does not execute or improve a model. Numerical eligibility still requires independent acceptance.</p>',
             f'<p>Synthetic inputs: <strong>{str(result["synthetic"]).lower()}</strong>. Model calls by this command: 0. Input-run cost: UNMEASURED.</p>',
             '<h2>Per-case comparison</h2><p>Each value shows baseline → candidate. Any score decrease or failed candidate gate rejects the candidate.</p>',
             '<table><thead><tr><th>Case / split</th><th>Boolean gates</th><th>Ordinal scores</th></tr></thead><tbody>']
    for row in report["rows"]:
        def cells(field):
            return '<br>'.join(escape(key) + ': ' + escape(values[0]) + ' → ' + escape(values[1])
                              for key, values in row[field].items())
        parts.append(f'<tr><td>{escape(row["case"])}<br>{escape(row["split"])}</td><td>{cells("gates")}</td><td>{cells("scores")}</td></tr>')
    parts.extend(['</tbody></table><h2>Exact input receipts</h2>'])
    for name, receipt in report["sources"].items():
        parts.append(f'<p>{escape(name)}: {receipt["bytes"]} bytes<br><code>sha256:{receipt["sha256"]}</code></p>')
    parts.append('<h2>Still requires independent review</h2><p>' + escape(', '.join(result['unverified'])) + '</p></html>')
    rendered = ''.join(parts)
    if len(rendered.encode()) > 8_000_000:
        raise ValueError("rendered review exceeds byte cap")
    return rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--format', choices=('json', 'html', 'event'), default='json')
    args = parser.parse_args()
    try:
        report = inspect(args.policy, args.baseline, args.candidate)
        print(render(report) if args.format == 'html' else json.dumps(report['event'] if args.format == 'event' else report, sort_keys=True))
        return 1 if report['comparison']['verdict'] == 'REJECT' else 0
    except (ValueError, OSError, TypeError, KeyError, AttributeError, RecursionError) as error:
        print(f'learning_review.main: {type(error).__name__}: {error}', file=sys.stderr)
        print(json.dumps({'status': 'NO_GATE', 'activated': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
