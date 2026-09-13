#!/usr/bin/env python3
"""Read one explicit outcome ledger in a pinned Agent Flow build on loopback."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import threading
import time

from outcome_review import history_bytes
from path_safety import read_regular_file_bounded, reject_linked_path

UPSTREAM_REVISION = '84cd2fb8c704cefe52e6dd41a375c4069442e206'
MAX_STREAMS = 4
# Exact output from the reviewed frozen-lockfile build; assets are not tracked upstream.
ASSET_HASHES = {
    '/index.js': '95eb7223db5c1d1dac41c076a05083c02cb0f696abc6973a22f88fad7c92718d',
    '/index.css': '0c9cd3e53923ce470272f577d87d406af19c5905c0857e5b2da21772cff15076',
}


class OutcomeSource:
    def __init__(self, ledger):
        self.ledger = Path(ledger).absolute()
        self.records = []
        self.lock = threading.Lock()
        self.refresh()

    def refresh(self):
        with self.lock:
            reject_linked_path(self.ledger, Path(self.ledger.anchor), label='outcome ledger')
            captured = read_regular_file_bounded(self.ledger, 4_000_000)
            records = history_bytes(captured)
            if not records:
                raise ValueError('initialized ledger required')
            if records[:len(self.records)] != self.records:
                raise ValueError('prior ledger prefix changed; operator review required')
            # Positive field allowlist; timestamps are declared ledger times, not tool duration.
            items = []
            first = previous = None
            for record in records:
                value = record['body'].get('recorded_at')
                if not isinstance(value, str) or len(value) > 64:
                    raise ValueError('bounded recorded timestamp required')
                stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
                if stamp.tzinfo is None or (previous is not None and stamp < previous):
                    raise ValueError('aware nondecreasing recorded timestamps required')
                first = stamp if first is None else first
                previous = stamp
                items.append({'sequence': record['body']['sequence'], 'sha256': record['sha256'],
                              'type': record['body'].get('event', {}).get('type', 'RUN_INITIALIZED'),
                              'failed_gate_count': len(record['body'].get('event', {}).get('failed_gates', [])),
                              'recorded_at': value, 'relative_recorded_seconds': (stamp - first).total_seconds()})
            self.records = records
            return {'schema_version': 1, 'kind': 'outcome-view', 'source_sha256': hashlib.sha256(captured).hexdigest(),
                    'source_bytes': len(captured), 'record_count': len(records), 'head': records[-1]['sha256'],
                    'records': items, 'activation_authority': False,
                    'mode': 'LIVE_LEDGER_METADATA', 'host_execution': 'NOT_OBSERVED'}


def events(snapshot):
    session = 'outcome-ledger'
    items = [{'time': 0, 'type': 'agent_spawn', 'sessionId': session,
              'payload': {'name': 'Outcome record', 'isMain': True, 'task': 'Ledger projection, not an executing host agent'}}]
    for record in snapshot['records']:
        content = (f"Outcome record {record['sequence']}: {record['type']}\n"
                   f"Failed gate count: {record['failed_gate_count']}\nRecord sha256:{record['sha256']}")
        items.append({'time': record['relative_recorded_seconds'], 'type': 'message', 'sessionId': session,
                      'payload': {'agent': 'Outcome record', 'role': 'assistant', 'content': content}})
    return items


def assets_at(upstream):
    upstream = Path(upstream).absolute()
    reject_linked_path(upstream, Path(upstream.anchor), label='upstream checkout')
    revision = subprocess.run(['git', '-C', str(upstream), 'rev-parse', 'HEAD'], check=True,
                              capture_output=True, text=True, timeout=5).stdout.strip()
    if revision != UPSTREAM_REVISION:
        raise ValueError('upstream revision differs from reviewed pin')
    result = {}
    for name in ('index.js', 'index.css'):
        result['/' + name] = read_regular_file_bounded(upstream / 'app/dist/webview' / name,
                                                       8_000_000, boundary=upstream)
        if hashlib.sha256(result['/' + name]).hexdigest() != ASSET_HASHES['/' + name]:
            raise ValueError('generated asset differs from reviewed build hash')
    return result


HTML = b'''<!doctype html><html lang="en" class="dark"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Outcome ledger in Agent Flow</title><link rel="stylesheet" href="/index.css"><style>
html{height:100%}body{height:100dvh;display:flex;flex-direction:column;margin:0;background:#0a0a1a;color:#dbeafe;font:14px system-ui}#notice{box-sizing:border-box;flex:none;overflow-wrap:anywhere;padding:10px 18px;background:#172554;line-height:21px}#notice a{color:#bfdbfe}#root{flex:1;min-height:0}#root>.h-screen{height:100%}body{overflow:hidden}
</style><div id="notice"><strong>LIVE LEDGER METADATA</strong> | Explicit single file. <span id="status">Connecting...</span><br>
Outcome record projection; host execution NOT OBSERVED. Compatibility avatar. Clock follows recorded ledger timestamps; token/cost totals unmeasured.<br>
No activation authority. <a href="/receipt" target="_blank">Exact source receipt</a>. Ledger text and paths are withheld.</div><div id="root"></div><script src="/index.js"></script><script src="/status.js"></script></html>'''
STATUS_JS = b'''async function update(){try{const r=await fetch('/receipt');const j=await r.json();document.getElementById('status').textContent=r.ok?j.record_count+' records | source '+j.source_sha256.slice(0,12):'SOURCE REFUSED';}catch(e){document.getElementById('status').textContent='DISCONNECTED';}setTimeout(update,2000);}update();'''


def handler_for(source, assets):
    streams = threading.BoundedSemaphore(MAX_STREAMS)

    class Handler(BaseHTTPRequestHandler):
        def reply_headers(self, status, mime, size=None):
            self.send_response(status)
            self.send_header('Content-Type', mime)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; font-src 'self' data:; frame-ancestors 'none'")
            self.send_header('X-Content-Type-Options', 'nosniff')
            if size is not None:
                self.send_header('Content-Length', str(size))
            self.end_headers()

        def do_GET(self):
            if self.path not in ('/', '/index.js', '/index.css', '/status.js', '/receipt', '/events'):
                self.send_error(404)
                return
            try:
                snapshot = source.refresh()
            except (ValueError, OSError, TypeError, KeyError, AttributeError, RecursionError) as error:
                print(f'agent_flow_outcome.refresh: {type(error).__name__}: source refused', file=sys.stderr)
                body = b'{"status":"SOURCE_REFUSED","activation_authority":false}'
                self.reply_headers(409, 'application/json', len(body))
                self.wfile.write(body)
                return
            if self.path == '/events':
                if not streams.acquire(blocking=False):
                    self.send_error(503, 'stream limit reached')
                    return
                try:
                    self.reply_headers(200, 'text/event-stream')
                    self.emit({'type': 'config', 'config': {'showMockData': False}})
                    self.emit({'type': 'session-list', 'sessions': [{'id': 'outcome-ledger', 'label': 'Outcome ledger metadata', 'status': 'active', 'startTime': 0, 'lastActivityTime': 0}]})
                    sent = 0
                    while True:
                        batch = events(snapshot)
                        if len(batch) > sent:
                            self.emit({'type': 'agent-event-batch', 'events': batch[sent:]})
                            sent = len(batch)
                        self.wfile.write(b': heartbeat\n\n')
                        self.wfile.flush()
                        time.sleep(2)
                        snapshot = source.refresh()
                except (BrokenPipeError, ConnectionResetError):
                    print('agent_flow_outcome.stream: browser disconnected', file=sys.stderr)
                except (ValueError, OSError, TypeError, KeyError, AttributeError, RecursionError) as error:
                    print(f'agent_flow_outcome.stream: {type(error).__name__}: source refused', file=sys.stderr)
                finally:
                    streams.release()
                return
            if self.path == '/receipt':
                snapshot['upstream_revision'] = UPSTREAM_REVISION
                snapshot['assets'] = {name: {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)} for name, raw in assets.items()}
                data, mime = json.dumps(snapshot, sort_keys=True).encode(), 'application/json'
            elif self.path == '/':
                data, mime = HTML, 'text/html; charset=utf-8'
            elif self.path == '/status.js':
                data, mime = STATUS_JS, 'application/javascript'
            else:
                data, mime = assets[self.path], 'application/javascript' if self.path.endswith('.js') else 'text/css'
            self.reply_headers(200, mime, len(data))
            self.wfile.write(data)

        def emit(self, payload):
            self.wfile.write(('data: ' + json.dumps(payload) + '\n\n').encode())
            self.wfile.flush()

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--port', type=int, default=8769)
    args = parser.parse_args()
    try:
        if not 1024 <= args.port <= 65535:
            raise ValueError('port must be between 1024 and 65535')
        source = OutcomeSource(args.ledger)
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(source, assets_at(args.upstream)))
        print(f'Outcome metadata viewer: http://127.0.0.1:{args.port}; no authority or host execution', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('agent_flow_outcome.shutdown: requested by operator', file=sys.stderr)
        finally:
            server.server_close()
        return 0
    except (ValueError, OSError, TypeError, KeyError, subprocess.SubprocessError) as error:
        print(f'agent_flow_outcome.main: {type(error).__name__}: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
