"""Review saved results and observe ledger appends without granting authority."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import agent_flow_outcome as viewer
import bootstrap_learning as learning
import learning_review as review
import outcome_review as outcome

TEMP_ROOT = Path(tempfile.gettempdir()).resolve(strict=True)


class ObservableLearningScenarios(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.policy = learning.policy_at(learning.ROOT / 'templates/learning')
        self.baseline, self.candidate = learning.demo(self.policy)
        self.paths = [self.root / name for name in ('policy.json', 'baseline.json', 'candidate.json')]
        self.write_inputs()
        self.ledger = self.root / 'events.jsonl'
        contract = learning.read(learning.ROOT / 'templates/harness/outcome-contract.json')
        contract['goal'] = 'PRIVATE_GOAL_SENTINEL'
        self.head = outcome.append(self.ledger, contract=contract)['sha256']

    def write_inputs(self):
        for path, value in zip(self.paths, (self.policy, self.baseline, self.candidate)):
            path.write_text(json.dumps(value), encoding='utf-8')

    def event(self):
        return {'type': 'GATE_FAILED', 'actor': 'PRIVATE_ACTOR_SENTINEL',
                'summary': 'PRIVATE_SUMMARY_SENTINEL', 'next_action': 'PRIVATE_ACTION_SENTINEL',
                'failed_gates': ['PRIVATE_GATE_SENTINEL'], 'evidence': ['PRIVATE_PATH_SENTINEL']}

    def test_report_reuses_comparator_and_contains_exact_receipts(self):
        report = review.inspect(*self.paths)
        self.assertEqual(learning.compare(self.policy, self.baseline, self.candidate), report['comparison'])
        self.assertFalse(report['comparison']['activated'])
        self.assertEqual(2, len(report['rows']))
        self.assertEqual('SAVED_OUTPUT_COMPARISON', report['mode'])
        self.assertEqual(hashlib.sha256(self.paths[0].read_bytes()).hexdigest(), report['sources']['policy']['sha256'])
        outcome.validate_event(report['event'])
        saved = outcome.append(self.ledger, event=report['event'], expected_head=self.head)
        self.assertEqual(saved, outcome.history(self.ledger)[-1])

    def test_regression_cannot_be_hidden_by_html_or_outcome_event(self):
        self.candidate['cases'][0]['scores']['usefulness']['value'] = 2
        self.write_inputs()
        report = review.inspect(*self.paths)
        self.assertEqual('REJECT', report['comparison']['verdict'])
        self.assertIn('numerical-comparison', report['event']['failed_gates'])
        self.assertIn('REJECT', review.render(report))
        self.candidate['cases'][0]['scores']['usefulness']['value'] = 4
        self.write_inputs()
        self.assertEqual('NUMERICALLY_ELIGIBLE', review.inspect(*self.paths)['comparison']['verdict'])

    def test_malformed_policy_and_duplicate_keys_fail_closed(self):
        self.policy['gates']['grounded']['pass'] = 'Changed after runs were produced'
        self.write_inputs()
        with self.assertRaisesRegex(ValueError, 'digest'):
            review.inspect(*self.paths)
        self.paths[0].write_text('{"version":2,"version":2}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            review.inspect(*self.paths)

    def test_source_content_is_escaped_and_never_auto_fetched(self):
        for run in (self.baseline, self.candidate):
            run['cases'][0]['id'] = '<script>fetch("https://example.invalid")</script>'
        self.write_inputs()
        rendered = review.render(review.inspect(*self.paths))
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertIn("default-src 'none'", rendered)

    def test_live_metadata_advances_without_copying_private_fields(self):
        source = viewer.OutcomeSource(self.ledger)
        before = source.refresh()
        outcome.append(self.ledger, event=self.event(), expected_head=self.head)
        after = source.refresh()
        self.assertEqual(before['record_count'] + 1, after['record_count'])
        self.assertNotEqual(before['source_sha256'], after['source_sha256'])
        self.assertEqual(1, after['records'][-1]['failed_gate_count'])
        self.assertEqual('GATE_FAILED', after['records'][-1]['type'])
        self.assertNotIn('PRIVATE_', json.dumps(after) + json.dumps(viewer.events(after)))
        self.assertFalse(after['activation_authority'])
        self.assertEqual('NOT_OBSERVED', after['host_execution'])

    def test_source_receipt_and_parser_use_one_identical_byte_snapshot(self):
        captured = self.ledger.read_bytes()
        with patch.object(viewer, 'read_regular_file_bounded', return_value=captured) as reader:
            snapshot = viewer.OutcomeSource(self.ledger).refresh()
        self.assertEqual(2, reader.call_count)  # construction and one explicit refresh
        self.assertEqual(hashlib.sha256(captured).hexdigest(), snapshot['source_sha256'])
        self.assertEqual(outcome.history_bytes(captured)[-1]['sha256'], snapshot['head'])

    def test_modified_generated_assets_fail_at_the_correct_git_revision(self):
        with patch.object(viewer.subprocess, 'run') as git, patch.object(viewer, 'read_regular_file_bounded', return_value=b'modified asset'):
            git.return_value.stdout = viewer.UPSTREAM_REVISION + '\n'
            with self.assertRaisesRegex(ValueError, 'build hash'):
                viewer.assets_at(self.root)
            git.return_value.stdout = '0' * 40 + '\n'
            with self.assertRaisesRegex(ValueError, 'revision'):
                viewer.assets_at(self.root)

    def test_rehashed_history_rewrite_still_fails_prefix_guard(self):
        source = viewer.OutcomeSource(self.ledger)
        contract = outcome.history(self.ledger)[0]['body']['contract']
        changed = self.root / 'rewritten.jsonl'
        outcome.append(changed, contract=contract)
        original = self.ledger.read_bytes()
        self.ledger.write_bytes(changed.read_bytes())
        with self.assertRaisesRegex(ValueError, 'prefix'):
            source.refresh()
        self.ledger.write_bytes(original)
        self.assertEqual(1, source.refresh()['record_count'])
        self.ledger.write_bytes(original + b'{')
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            source.refresh()

    def test_symlink_and_oversized_inputs_fail_without_directory_discovery(self):
        alias = self.root / 'alias.jsonl'
        try:
            alias.symlink_to(self.ledger)
        except OSError as error:
            self.skipTest(f'Platform does not permit test symlink: {error}')
        with self.assertRaisesRegex(ValueError, 'linked'):
            viewer.OutcomeSource(alias)
        self.paths[0].write_bytes(b' ' * 2_000_001)
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            review.inspect(*self.paths)

    def test_http_receipt_refuses_paths_writes_and_mutated_source(self):
        source = viewer.OutcomeSource(self.ledger)
        server = ThreadingHTTPServer(('127.0.0.1', 0), viewer.handler_for(source, {'/index.js': b'', '/index.css': b''}))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        url = f'http://127.0.0.1:{server.server_port}'
        with urllib.request.urlopen(url + '/receipt') as response:
            self.assertEqual(1, json.load(response)['record_count'])
            self.assertIn("connect-src 'self'", response.headers['Content-Security-Policy'])
        for path, method, status in [('/../../etc/passwd', 'GET', 404), ('/receipt', 'POST', 501)]:
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(urllib.request.Request(url + path, method=method))
            self.assertEqual(status, caught.exception.code)
            caught.exception.close()
        self.ledger.write_text('{}\n', encoding='utf-8')
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(url + '/receipt')
        self.assertEqual(409, caught.exception.code)
        caught.exception.close()


if __name__ == '__main__':
    unittest.main()
