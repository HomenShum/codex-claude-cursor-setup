#!/usr/bin/env python3
"""Validate the public setup kit without requiring third-party packages."""

from __future__ import annotations

import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import sys
import tomllib
from typing import Callable, Iterable
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
MAX_EXTERNAL_URLS = 200
MAX_WORKERS = 4
MAX_RESPONSE_BYTES = 65_536
TIMEOUT_SECONDS = 10
MAX_PUBLIC_FILES = 2_000
MAX_PUBLIC_FILE_BYTES = 1_048_576
MAX_VALIDATION_ERRORS = 500
ALLOWED_EXTERNAL_HOSTS = frozenset(
    {"github.com", "learn.chatgpt.com", "code.claude.com"}
)
REQUIRED_PATHS = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "SECURITY.md",
    "THIRD_PARTY.md",
    "LICENSE",
    "docs/setup.md",
    "docs/mcp-and-agent-bridges.md",
    "docs/proof-workflow.md",
    "docs/skills-plugins-hooks.md",
    "docs/security.md",
    "docs/external-projects.md",
    "docs/provenance.md",
    "docs/troubleshooting.md",
    "sources/external-projects.json",
    "sources/official-docs.json",
    "templates/project/AGENTS.md",
    "templates/project/CLAUDE.md",
    "templates/project/.mcp.json",
)
SECRET_PATTERNS = (
    ("OpenAI-style token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub-style token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[A-Z0-9]{16}\b")),
    ("Slack-style token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    (
        "credential-bearing database URL",
        re.compile(r"(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^:/\s]+:[^@/\s]+@", re.I),
    ),
)
PERSONAL_PATH_PATTERNS = (
    re.compile(r"[A-Za-z]:\\Users\\(?!USERNAME(?:\\|\b))[^\\\s]+", re.I),
    re.compile(r"/(?:Users|home)/(?!USERNAME(?:/|\b))[^/\s]+"),
)
FORBIDDEN_FILENAMES = frozenset(
    {"auth.json", "credentials.json", "history.jsonl", "session.sqlite", "state.sqlite"}
)
FORBIDDEN_MARKER_HASHES = ((31, "eb4ac26dcbf5019d8f29065b1ba9e5646c68bb5026fcb4361f0f278da8f0fe6c"),)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
GITHUB_URL = re.compile(
    r"https://github\.com/([^/\s)\"'\]}>]+/[^/\s)#?,\"'\]}>]+)", re.I
)
VENDOR_DOC_URL = re.compile(
    r"https://(?:learn\.chatgpt\.com|code\.claude\.com)/[^\s)>\]\"']+", re.I
)
ACTION_USE = re.compile(
    r"(?m)^\s*-\s*uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
    r"(?:/[^\s@]+)?@[^\s#]+"
)
SERVICE_REPOSITORY_MARKERS = (
    (
        "https://" + "json.schemastore.org/",
        "https://github.com/SchemaStore/schemastore",
    ),
)


class BoundedErrors(list[str]):
    """Collect deterministic diagnostics without allowing adversarial growth."""

    _cap_message = f"validation error cap reached: {MAX_VALIDATION_ERRORS}"

    def append(self, item: str) -> None:
        if len(self) < MAX_VALIDATION_ERRORS - 1:
            super().append(item)
        elif len(self) == MAX_VALIDATION_ERRORS - 1:
            super().append(self._cap_message)

    def extend(self, items: Iterable[str]) -> None:
        for item in items:
            self.append(item)


def collect_public_files(root: Path, errors: BoundedErrors) -> list[Path]:
    """Walk deterministically and stop after one honest publication-cap error."""

    public_files: list[Path] = []
    entries_seen = 0
    for current, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_directories: list[str] = []
        for name in sorted(directory_names):
            if name in {".git", "__pycache__"}:
                continue
            candidate = current_path / name
            if candidate.is_symlink():
                entries_seen += 1
                if entries_seen > MAX_PUBLIC_FILES:
                    errors.append(f"public file cap exceeded: more than {MAX_PUBLIC_FILES}")
                    return public_files
                errors.append(
                    f"symlink is not portable publication input: {candidate.relative_to(root)}"
                )
                continue
            kept_directories.append(name)
        directory_names[:] = kept_directories

        for name in sorted(file_names):
            path = current_path / name
            entries_seen += 1
            if entries_seen > MAX_PUBLIC_FILES:
                errors.append(f"public file cap exceeded: more than {MAX_PUBLIC_FILES}")
                return public_files
            if path.is_symlink():
                errors.append(f"symlink is not portable publication input: {path.relative_to(root)}")
                continue
            try:
                size = path.stat().st_size
            except OSError as exc:
                errors.append(f"cannot stat public file {path.relative_to(root)}: {exc}")
                continue
            if size > MAX_PUBLIC_FILE_BYTES:
                errors.append(
                    f"public file exceeds {MAX_PUBLIC_FILE_BYTES}-byte scan cap: "
                    f"{path.relative_to(root)}"
                )
                continue
            public_files.append(path)
    return public_files


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_repo_url(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.netloc.lower() != "github.com" or len(parts) < 2:
        raise ValueError(f"not a GitHub repository URL: {url}")
    return f"https://github.com/{parts[0]}/{parts[1].removesuffix('.git')}"


def normalize_doc_url(url: str) -> str:
    parsed = urlparse(url.rstrip(".,;"))
    return parsed._replace(fragment="").geturl()


def validate_repo(root: Path = ROOT) -> list[str]:
    errors = BoundedErrors()
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    public_files = collect_public_files(root, errors)
    for path in public_files:
        if path.name.lower() in FORBIDDEN_FILENAMES:
            errors.append(f"forbidden state file: {path.relative_to(root)}")
        if (
            path.name == ".env"
            or (path.name.startswith(".env.") and path.name != ".env.example")
            or path.suffix.lower() in {".sqlite", ".sqlite3", ".db"}
        ):
            errors.append(f"forbidden local-data file: {path.relative_to(root)}")

    texts: dict[Path, str] = {}
    for path in public_files:
        try:
            content = read_text(path)
        except OSError as exc:
            errors.append(f"cannot read public file {path.relative_to(root)}: {exc}")
            continue
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 or binary publication file: {path.relative_to(root)}")
            continue
        texts[path] = content
        relative = path.relative_to(root)
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"possible {label}: {relative}")
        for pattern in PERSONAL_PATH_PATTERNS:
            if pattern.search(content):
                errors.append(f"possible personal absolute path: {relative}")
        lowered = content.lower()
        for width, digest in FORBIDDEN_MARKER_HASHES:
            if any(
                hashlib.sha256(lowered[index:index + width].encode("utf-8")).hexdigest() == digest
                for index in range(max(0, len(lowered) - width + 1))
            ):
                errors.append(f"private-source marker present: {relative}")

    for path, content in texts.items():
        if path.suffix.lower() != ".json":
            continue
        try:
            json.loads(content)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON {path.relative_to(root)}: {exc}")

    for path, content in texts.items():
        if path.suffix.lower() != ".toml":
            continue
        try:
            tomllib.loads(content)
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"invalid TOML {path.relative_to(root)}: {exc}")

    for path, content in texts.items():
        if path.suffix.lower() != ".md":
            continue
        for raw_target in MARKDOWN_LINK.findall(content):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or urlparse(target).scheme or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"local link escapes repository: {path.relative_to(root)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {path.relative_to(root)} -> {target}")

    external_path = root / "sources/external-projects.json"
    official_path = root / "sources/official-docs.json"
    catalog_repos: set[str] = set()
    if external_path in texts:
        try:
            payload = json.loads(texts[external_path])
            projects = payload.get("projects", [])
            for index, project in enumerate(projects):
                missing = sorted(
                    {"name", "repository", "relationship", "license", "accessed"} - project.keys()
                )
                if missing:
                    errors.append(f"external project {index} missing: {', '.join(missing)}")
                    continue
                if not isinstance(project.get("check", True), bool):
                    errors.append(f"external project {index} has non-boolean check flag")
                if project.get("check") is False and not project.get("notes"):
                    errors.append(f"external project {index} skips checks without a note")
                normalized = normalize_repo_url(project["repository"])
                if normalized.lower() in {value.lower() for value in catalog_repos}:
                    errors.append(f"duplicate external repository: {normalized}")
                catalog_repos.add(normalized)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid external project catalog: {exc}")

    cited_repos: set[str] = set()
    for content in texts.values():
        for path_part in GITHUB_URL.findall(content):
            normalized = normalize_repo_url(f"https://github.com/{path_part}")
            if normalized.lower() != "https://github.com/homenshum/codex-claude-code-setup":
                cited_repos.add(normalized)
        for action in ACTION_USE.findall(content):
            cited_repos.add(normalize_repo_url(f"https://github.com/{action}"))
        for marker, repository in SERVICE_REPOSITORY_MARKERS:
            if marker in content:
                cited_repos.add(repository)
    missing_repos = sorted(
        repo for repo in cited_repos if repo.lower() not in {value.lower() for value in catalog_repos}
    )
    errors.extend(f"uncatalogued GitHub repository: {repo}" for repo in missing_repos)

    human_ledger = texts.get(root / "docs/external-projects.md", "")
    human_repos = {
        normalize_repo_url(f"https://github.com/{path_part}").lower()
        for path_part in GITHUB_URL.findall(human_ledger)
    }
    errors.extend(
        f"external repository missing from human ledger: {repo}"
        for repo in sorted(catalog_repos)
        if repo.lower() not in human_repos
    )

    catalog_docs: set[str] = set()
    if official_path in texts:
        try:
            payload = json.loads(texts[official_path])
            for index, source in enumerate(payload.get("sources", [])):
                missing = sorted({"vendor", "topic", "url"} - source.keys())
                if missing:
                    errors.append(f"official source {index} missing: {', '.join(missing)}")
                    continue
                catalog_docs.add(normalize_doc_url(source["url"]))
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid official document catalog: {exc}")
    cited_docs = {
        normalize_doc_url(match.group(0))
        for content in texts.values()
        for match in VENDOR_DOC_URL.finditer(content)
    }
    errors.extend(
        f"uncatalogued official document: {url}" for url in sorted(cited_docs - catalog_docs)
    )

    return sorted(set(errors))


def validate_public_destination(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_EXTERNAL_HOSTS:
        raise ValueError(f"external URL is not on the HTTPS allowlist: {url}")
    addresses = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses:
        raise ValueError(f"external host did not resolve: {parsed.hostname}")
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if any((ip.is_private, ip.is_loopback, ip.is_link_local, ip.is_multicast, ip.is_reserved, ip.is_unspecified)):
            raise ValueError(f"external host resolved to a non-public address: {parsed.hostname}")


class SafeRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        target = urljoin(req.full_url, newurl)
        validate_public_destination(target)
        return super().redirect_request(req, fp, code, msg, headers, target)


def fetch_external(url: str) -> tuple[bool, str]:
    try:
        validate_public_destination(url)
        headers = {"User-Agent": "codex-claude-setup-validator/1.0"}
        github_token = os.environ.get("SETUP_LINKCHECK_GITHUB_TOKEN")
        if github_token and urlparse(url).hostname == "github.com":
            headers["Authorization"] = f"Bearer {github_token}"
        request = Request(url, headers=headers)
        with build_opener(SafeRedirectHandler()).open(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                body = body[:MAX_RESPONSE_BYTES]
            status = getattr(response, "status", 200)
            if status < 200 or status >= 400:
                return False, f"HTTP {status}"
            return True, f"HTTP {status}; sampled {len(body)} bytes"
    except Exception as exc:  # one URL must not abort the remaining bounded checks
        return False, f"{type(exc).__name__}: {exc}"


def check_external_urls(
    urls: Iterable[str],
    fetcher: Callable[[str], tuple[bool, str]] = fetch_external,
) -> list[tuple[str, bool, str]]:
    bounded = sorted(set(urls))
    if len(bounded) > MAX_EXTERNAL_URLS:
        raise ValueError(f"external URL cap exceeded: {len(bounded)} > {MAX_EXTERNAL_URLS}")
    results: list[tuple[str, bool, str]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        future_urls = {pool.submit(fetcher, url): url for url in bounded}
        for future in as_completed(future_urls):
            url = future_urls[future]
            try:
                ok, detail = future.result()
            except Exception as exc:
                ok, detail = False, f"{type(exc).__name__}: {exc}"
            results.append((url, ok, detail))
    return sorted(results)


def catalog_urls(root: Path = ROOT) -> list[str]:
    external = json.loads(read_text(root / "sources/external-projects.json"))
    official = json.loads(read_text(root / "sources/official-docs.json"))
    return [
        project["repository"]
        for project in external["projects"]
        if project.get("check", True)
    ] + [
        source["url"] for source in official["sources"]
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-external", action="store_true", help="perform bounded live URL checks")
    args = parser.parse_args()

    errors = validate_repo()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: offline repository validation")

    if args.check_external:
        try:
            urls = catalog_urls()
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            print(f"ERROR: cannot load external catalogs — {type(exc).__name__}: {exc}")
            return 1
        results = check_external_urls(urls)
        for url, ok, detail in results:
            print(f"{'PASS' if ok else 'ERROR'}: {url} — {detail}")
        if any(not ok for _, ok, _ in results):
            return 1
        print(f"PASS: {len(results)} bounded external URL checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
