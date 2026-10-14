"""Cross-host builders preserve frozen goals and failed work through handoffs."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import outcome_review as outcome

# Test-owned fixtures use physical paths; the production link guard stays strict.
TEMP_ROOT = Path(tempfile.gettempdir()).resolve(strict=True)


class OutcomeScenarios(unittest.TestCase):
    def setUp(self):
        self.contract = outcome.read(Path(__file__).resolve().parents[1] / "templates/harness/outcome-contract.json")

    def event(self, kind, **fields):
        return {"type": kind, "actor": "codex", "summary": "Keep the user request intact.",
                "next_action": "Inspect the next receipt", "failed_gates": [], "evidence": [], **fields}

    def request(self, request_id="agent", owner="codex"):
        return self.event("REQUEST_RECORDED", request_id=request_id, owner=owner,
                          source_ref="requests/accepted-brief.md", scope=["Agent cancellation"],
                          acceptance=["No new tool or graph write after cancellation"])

    def append_event(self, ledger, event):
        return outcome.append(ledger, event=event, expected_head=outcome.history(ledger)[-1]["sha256"])

    def change(self, ledger, request_id="agent", change_id="cancel-v1", actor="codex"):
        baseline = self.append_event(ledger, self.event("BASELINE_CAPTURED", request_id=request_id,
                                    evidence=["before/cancel.json"], summary="Cancellation still writes graph state."))
        return self.append_event(ledger, self.event("CHANGE_RECORDED", request_id=request_id,
                                 actor=actor, change_id=change_id, before=baseline["sha256"],
                                 after={"summary": "Cancellation produces no later graph writes.", "evidence": ["after/cancel.json"]}))

    def approval(self, ledger, request_id="agent", change_ids=None, actor="independent-reviewer"):
        return self.append_event(ledger, self.event("REVIEW_RECORDED", request_id=request_id,
                                 change_ids=change_ids or ["cancel-v1"], actor=actor, verdict="PASS",
                                 evidence=["review/replay.json"]))

    def test_two_owners_resume_requests_without_losing_before_after_or_failed_gate(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            self.append_event(ledger, self.request("visual", "claude"))
            decision = self.event("DECISION_RECORDED", request_id="agent", decision_id="D1",
                                  supersedes=None, before="One worker held both scopes.",
                                  after="Codex owns agent behavior; Claude owns visuals.", evidence=["requests/ownership.md"])
            self.append_event(ledger, decision)
            self.change(ledger)
            self.append_event(ledger, self.event("GATE_FAILED", failed_gates=["cancellation"], evidence=["before/cancel.json"]))
            self.append_event(ledger, self.event("HOST_SWITCH", actor="next-host"))
            review = self.approval(ledger)
            completion = self.event("REQUEST_COMPLETED", request_id="agent", review_sha256=review["sha256"])
            with self.assertRaisesRegex(ValueError, "unresolved"):
                self.append_event(ledger, completion)
            self.append_event(ledger, self.event("GATE_PASSED", failed_gates=["cancellation"], evidence=["after/cancel.json"]))
            self.append_event(ledger, completion)
            report = outcome.review(outcome.history(ledger))
            self.assertIn("agent: COMPLETION_RECORDED", report)
            self.assertIn("visual: OPEN", report)
            self.assertIn("before/cancel.json", report)
            self.assertIn("after/cancel.json", report)
            self.assertIn("Codex owns agent behavior", report)
            with self.assertRaisesRegex(ValueError, "completed"):
                self.append_event(ledger, decision)

    def test_reviewer_cannot_close_wrong_case_or_stale_revision(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            self.append_event(ledger, self.request("visual", "claude"))
            baseline = self.append_event(ledger, self.event("BASELINE_CAPTURED", request_id="visual", evidence=["visual/before.png"]))
            before = ledger.read_bytes()
            invalid = [self.request(), self.event("REQUEST_COMPLETED", request_id="missing", review_sha256="0" * 64),
                       self.event("CHANGE_RECORDED", request_id="agent", change_id="wrong", before=baseline["sha256"],
                                  after={"summary": "Claims a repair", "evidence": ["after.json"]}),
                       self.event("CHANGE_RECORDED", request_id="agent", change_id="empty", before=baseline["sha256"],
                                  after={"summary": "Claims a repair", "evidence": []}),
                       self.event("CONTEXT_REFRESHED", request_id="agent")]
            for event in invalid:
                with self.subTest(event=event["type"]), self.assertRaises(ValueError):
                    self.append_event(ledger, event)
                self.assertEqual(before, ledger.read_bytes())
            self.change(ledger)
            for actor in ("codex",):
                with self.assertRaisesRegex(ValueError, "independent"):
                    self.approval(ledger, actor=actor)
            review = self.approval(ledger)
            decision = self.event("DECISION_RECORDED", request_id="agent", decision_id="D1", supersedes=None,
                                  before="Unclear retry policy", after="Retry within the existing attempt cap", evidence=["decision.md"])
            self.append_event(ledger, decision)
            with self.assertRaisesRegex(ValueError, "current"):
                self.append_event(ledger, self.event("REQUEST_COMPLETED", request_id="agent", review_sha256=review["sha256"]))
            self.append_event(ledger, {**decision, "decision_id": "D2", "supersedes": "D1", "after": "Preserve cap on host switch too"})
            self.change(ledger, change_id="cancel-v2")
            with self.assertRaisesRegex(ValueError, "all current"):
                self.approval(ledger)
            review = self.approval(ledger, change_ids=["cancel-v1", "cancel-v2"])
            self.append_event(ledger, self.event("REQUEST_COMPLETED", request_id="agent", review_sha256=review["sha256"]))
            self.assertEqual(2, sum(r["body"].get("event", {}).get("type") == "DECISION_RECORDED" for r in outcome.history(ledger)))

    def test_concurrent_hosts_and_sustained_history_never_overwrite_requests(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            first = outcome.append(ledger, contract=self.contract)
            def writer(number):
                try:
                    outcome.append(ledger, event=self.request(f"request-{number}"), expected_head=first["sha256"])
                    return True
                except (ValueError, OSError):
                    return False
            with ThreadPoolExecutor(max_workers=8) as workers:
                self.assertEqual(1, sum(workers.map(writer, range(8))))
            head = outcome.history(ledger)[-1]["sha256"]
            for number in range(2, outcome.MAX_EVENTS):
                head = outcome.append(ledger, event=self.event("HOST_SWITCH", actor=f"host-{number}"), expected_head=head)["sha256"]
            before = ledger.read_bytes()
            with self.assertRaisesRegex(ValueError, "full"):
                outcome.append(ledger, event=self.event("HOST_SWITCH"), expected_head=head)
            self.assertEqual(before, ledger.read_bytes())
            self.assertEqual(outcome.MAX_EVENTS, len(outcome.history(ledger)))

    def test_replayed_semantics_reject_rehashed_wrong_request_evidence(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            self.append_event(ledger, self.request("visual", "claude"))
            self.change(ledger)
            records = outcome.history(ledger)
            records[-1]["body"]["event"]["request_id"] = "visual"
            records[-1]["sha256"] = outcome.digest(records[-1]["body"])
            ledger.write_bytes(b"".join(outcome.encoded(record) + b"\n" for record in records))
            with self.assertRaisesRegex(ValueError, "wrong-request baseline"):
                outcome.history(ledger)

    def test_new_host_and_request_do_not_reset_candidate_budget(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            for number in range(self.contract["max_attempts"]):
                self.append_event(ledger, self.event("CANDIDATE_CREATED", summary=f"Candidate {number}"))
                self.append_event(ledger, self.event("HOST_SWITCH", actor="next-host"))
            self.append_event(ledger, self.request("follow-up"))
            before = ledger.read_bytes()
            with self.assertRaisesRegex(ValueError, "budget exhausted"):
                self.append_event(ledger, self.event("CANDIDATE_CREATED"))
            self.assertEqual(before, ledger.read_bytes())

    def test_long_running_request_can_review_all_changes_within_ledger_cap(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            baseline = self.append_event(ledger, self.event("BASELINE_CAPTURED", request_id="agent", evidence=["before.json"]))
            change_ids = [f"case-repair-{number}" for number in range(101)]
            for change_id in change_ids:
                self.append_event(ledger, self.event("CHANGE_RECORDED", request_id="agent", change_id=change_id,
                    before=baseline["sha256"], after={"summary": "One observed case repaired", "evidence": [f"after/{change_id}.json"]}))
            review = self.approval(ledger, change_ids=change_ids)
            self.append_event(ledger, self.event("REQUEST_COMPLETED", request_id="agent", review_sha256=review["sha256"]))
            self.assertIn("agent: COMPLETION_RECORDED", outcome.review(outcome.history(ledger)))

    def test_oversized_change_ids_cannot_strand_future_review_on_append_or_replay(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            self.change(ledger, change_id="x" * 62)
            records = outcome.history(ledger)
            for bad_id in ("x" * 63, "x" * 4000, "\u754c" * 11):
                event = {**records[-1]["body"]["event"], "change_id": bad_id}
                before = ledger.read_bytes()
                with self.assertRaisesRegex(ValueError, "64 bytes"):
                    self.append_event(ledger, event)
                self.assertEqual(before, ledger.read_bytes())
                forged = copy.deepcopy(records)
                forged[-1]["body"]["event"] = event
                forged[-1]["sha256"] = outcome.digest(forged[-1]["body"])
                ledger.write_bytes(b"".join(outcome.encoded(record) + b"\n" for record in forged))
                with self.assertRaisesRegex(ValueError, "64 bytes"):
                    outcome.history(ledger)
                ledger.write_bytes(before)
            review = self.approval(ledger, change_ids=["x" * 62])
            self.append_event(ledger, self.event("REQUEST_COMPLETED", request_id="agent", review_sha256=review["sha256"]))

    def test_next_host_sees_review_verdict_identity_and_exact_reference(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            outcome.append(ledger, contract=self.contract)
            self.append_event(ledger, self.request())
            self.change(ledger)
            rejected = self.append_event(ledger, self.event("REVIEW_RECORDED", request_id="agent", actor="judge",
                change_ids=["cancel-v1"], verdict="REVISE", evidence=["review/revise.json"]))
            self.append_event(ledger, self.event("HOST_SWITCH"))
            report = outcome.review(outcome.history(ledger))
            for signal in ("Request: agent; actor: judge", "Verdict: REVISE; reviewed changes: cancel-v1", rejected["sha256"]):
                self.assertIn(signal, report)
            approved = self.approval(ledger)
            self.append_event(ledger, self.event("HOST_SWITCH"))
            report = outcome.review(outcome.history(ledger))
            self.assertIn("Verdict: PASS; reviewed changes: cancel-v1", report)
            self.assertIn(f"Current review: {approved['sha256']}", report)

    def test_builder_cannot_upgrade_unknown_baseline_to_ready(self):
        self.assertEqual("DISCOVERY", outcome.validate_contract(self.contract)["status"])
        self.contract["state"] = "READY"
        with self.assertRaises(ValueError):
            outcome.validate_contract(self.contract)

    def test_failed_gate_survives_host_switch_and_stale_writer_is_refused(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            first = outcome.append(ledger, contract=self.contract)
            failure = {"type": "GATE_FAILED", "actor": "worker", "summary": "A source claim lacks its receipt.", "next_action": "Inspect the source", "failed_gates": ["citation-support"], "evidence": ["run-1/failure.json"]}
            second = outcome.append(ledger, event=failure, expected_head=first["sha256"])
            with self.assertRaises(ValueError):
                outcome.append(ledger, event=failure, expected_head=first["sha256"])
            switch = {**failure, "type": "HOST_SWITCH", "actor": "next-host", "failed_gates": [], "summary": "Resume the same work."}
            outcome.append(ledger, event=switch, expected_head=second["sha256"])
            report = outcome.review(outcome.history(ledger))
            self.assertIn("Open failures: citation-support", report)
            self.assertIn("NOT AUTHORIZED", report)
            before = ledger.read_bytes()
            with self.assertRaises(ValueError):
                outcome.append(ledger, event={**failure, "type": "GATE_PASSED", "evidence": []}, expected_head=outcome.history(ledger)[-1]["sha256"])
            self.assertEqual(before, ledger.read_bytes())
            self.assertIn("Open failures: citation-support", outcome.review(outcome.history(ledger)))
            with self.assertRaises(ValueError):
                outcome.append(ledger, contract=self.contract)

    def test_sustained_append_bounds_history_and_detects_corruption(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            ledger = Path(directory) / "events.jsonl"
            head = outcome.append(ledger, contract=self.contract)["sha256"]
            event = {"type": "CONTEXT_REFRESHED", "actor": "builder", "summary": "No new source yet", "next_action": "Review remaining authorized source", "failed_gates": [], "evidence": []}
            for _ in range(30):
                head = outcome.append(ledger, event=event, expected_head=head)["sha256"]
            self.assertEqual(31, len(outcome.history(ledger)))
            original = ledger.read_bytes()
            ledger.write_bytes(original.replace(b"No new source yet", b"All sources found", 1))
            with self.assertRaises(ValueError):
                outcome.history(ledger)

    def test_search_ablation_measures_exact_repetition_not_semantic_quality(self):
        item = {"query": "programmable display", "query_origin": "USER", "retriever": "keyword-v1", "corpus_snapshot": "sources-v1", "trace": "run/search", "stop_reason": "continue", "complete": True, "document_ids": ["doc-a"]}
        result = outcome.trajectory({"positive_document_ids": ["doc-a", "doc-b"], "rounds": [item, copy.deepcopy(item)]})
        self.assertEqual(1, result["repeated_exact_queries"])
        self.assertEqual(0.5, result["positive_document_recall"])
        self.assertEqual("REQUIRES_REVIEW", result["source_support"])


if __name__ == "__main__":
    unittest.main()
