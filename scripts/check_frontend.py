#!/usr/bin/env python3
"""Dependency-free validation for EventHub's inline browser JavaScript."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ("index.html", "eventhub-preview.html")

class ScriptExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "script":
            return
        attrs = dict(attrs)
        src = attrs.get("src")
        kind = (attrs.get("type") or "").strip().lower()
        if src or kind in {"application/json", "application/ld+json", "importmap"}:
            self.current = None
        else:
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.current is not None:
            self.parts.append("".join(self.current))
            self.current = None

def main():
    contents = {}
    for name in FILES:
        path = ROOT / name
        if not path.is_file():
            raise SystemExit(f"FAIL: required frontend file missing: {name}")
        contents[name] = path.read_text(encoding="utf-8")

    if contents[FILES[0]] != contents[FILES[1]]:
        raise SystemExit("FAIL: index.html and eventhub-preview.html differ")

    # Fail fast if critical event-day safety controls disappear in a later UI edit.
    source = contents[FILES[0]]
    required_contracts = {
        "one-guest camera lock": "beginGuestScanLock(scanned,'camera')",
        "manual scan lock": "beginGuestScanLock(code,'manual')",
        "pre/post save verification": "fetchFreshGuest(passCode)",
        "proof-gated release": "state.scanProofPending",
        "visible save failure dialog": "SAVE NOT CONFIRMED",
        "retry / status recovery": "RETRY / CHECK STATUS",
        "checkpoint assignment preflight": "checkpointAccessBlocked",
        "admin checkpoint name picker": "Assign volunteer by name",
        "sticky volunteer action controls": "position:sticky;bottom:calc(env(safe-area-inset-bottom) + 4px)",
        "guest mode hides nonessential camera controls": ".scanner-mode.scanner-has-guest .scanner-screen .manual-pass-entry",
        "checkpoint access retry path": "RETRY ACCESS CHECK",
        "checkpoint preflight fail closed": "STATION ACCESS UNAVAILABLE",
    }
    missing = [label for label, fragment in required_contracts.items() if fragment not in source]
    if missing:
        raise SystemExit("FAIL: missing event-day safety/UI contracts: " + ", ".join(missing))

    total = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, source in contents.items():
            parser = ScriptExtractor()
            parser.feed(source)
            parser.close()
            for index, js in enumerate(parser.parts, start=1):
                if not js.strip():
                    continue
                check_file = Path(tmp) / f"{Path(name).stem}-{index}.js"
                check_file.write_text(js, encoding="utf-8")
                result = subprocess.run(
                    ["node", "--check", str(check_file)],
                    text=True, capture_output=True
                )
                if result.returncode:
                    print(result.stdout, end="")
                    print(result.stderr, end="")
                    raise SystemExit(f"FAIL: JavaScript syntax error in {name}, inline script {index}")
                total += 1

    print(f"PASS: both frontend files are byte-identical; Node parsed {total} inline JavaScript blocks.")

if __name__ == "__main__":
    main()
