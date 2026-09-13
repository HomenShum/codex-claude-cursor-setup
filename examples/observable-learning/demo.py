#!/usr/bin/env python3
"""Create an explicitly synthetic review example or append a synthetic failure."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import bootstrap_learning as learning
import learning_review
import outcome_review as outcome
from path_safety import reject_linked_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--out', type=Path)
    choice.add_argument('--append-to', type=Path)
    args = parser.parse_args()
    try:
        if args.append_to is not None:
            records = outcome.history(args.append_to)
            if not records or records[0]['body']['contract']['experiment'] != 'synthetic-observable-learning':
                raise ValueError('only this synthetic example ledger may receive the demo event')
            event = {'type': 'GATE_FAILED', 'actor': 'synthetic-example',
                     'summary': 'Synthetic readback failure for viewer demonstration.',
                     'next_action': 'Inspect the recorded failure. No model run or promotion occurred.',
                     'failed_gates': ['synthetic-readback'], 'evidence': ['synthetic:readback-fixture']}
            print(json.dumps(outcome.append(args.append_to, event=event, expected_head=records[-1]['sha256']), sort_keys=True))
            return 0
        destination = args.out.absolute()
        reject_linked_path(destination, Path(destination.anchor), label='example destination')
        destination.mkdir(parents=False, exist_ok=False)
        policy = learning.policy_at(ROOT / 'templates/learning')
        baseline, candidate = learning.demo(policy)
        paths = [destination / name for name in ('policy.json', 'baseline.json', 'candidate.json')]
        for path, value in zip(paths, (policy, baseline, candidate)):
            path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
        report = learning_review.inspect(*paths)
        (destination / 'review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        (destination / 'review.html').write_text(learning_review.render(report), encoding='utf-8')
        contract = learning.read(ROOT / 'templates/harness/outcome-contract.json')
        contract.update(experiment='synthetic-observable-learning', goal='Inspect saved synthetic outputs and observe a ledger append.',
                        case_ids=['visible', 'heldout'], expected_improvement='Synthetic values 3 to 4; no measured model improvement.')
        ledger = destination / 'events.jsonl'
        initial = outcome.append(ledger, contract=contract)
        appended = outcome.append(ledger, event=report['event'], expected_head=initial['sha256'])
        print(json.dumps({'synthetic': True, 'model_calls': 0, 'activated': False,
                          'record_count': 2, 'head': appended['sha256']}))
        return 0
    except (ValueError, OSError, TypeError, KeyError, AttributeError, RecursionError) as error:
        print(f'observable_learning_demo.main: {type(error).__name__}: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
