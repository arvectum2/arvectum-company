#!/usr/bin/env python3
"""Compare OFFLINE real-client mock HTTP probe outcomes; no live requests.

One probe executes the Tender-installed Python SDK, the other the Site-bundled
JavaScript SDK. An OK is limited to these named scenarios and no other behavior.
"""
import argparse
import json
from pathlib import Path
import sys

EXPECTED = (
    "health", "contract_v1", "contract_v2_rejected", "exists_200", "exists_404",
    "stats_503", "stats_401", "search_identity", "ensure_404_create",
    "transport_failure",
)
OUTCOMES = {
    "health": "ok",
    "contract_v1": "ok",
    "contract_v2_rejected": "incompatible_contract",
    "exists_200": "present",
    "exists_404": "absent",
    "stats_503": "http_503",
    "stats_401": "http_401",
    "search_identity": "hits_empty",
    "ensure_404_create": "created",
    "transport_failure": "transport_error",
}
SCHEMA = "aec001-two-consumer-contract-v1"

def compare(py, js):
    def valid(item, language):
        return (isinstance(item, dict) and item.get("schema") == SCHEMA and
                item.get("language") == language and
                isinstance(item.get("scenarios"), dict))
    if not valid(py, "Python") or not valid(js, "JavaScript"):
        return {"status": "INCOMPLETE_INVALID_EVIDENCE", "case_count": 0, "matched": 0,
                "failure_cases": [], "real_service_used": False}
    left, right = py["scenarios"], js["scenarios"]
    cases = sorted(set(EXPECTED) | set(left) | set(right))
    failures = [
        c for c in cases
        if c not in OUTCOMES or left.get(c) != OUTCOMES.get(c) or
        right.get(c) != OUTCOMES.get(c) or left.get(c) != right.get(c)
    ]
    return {
        "schema": "aec001-two-consumer-comparison-v1",
        "status": "SCOPED_EQUIVALENCE" if not failures else "DIVERGENCE",
        "case_count": len(EXPECTED),
        "matched": len(EXPECTED) - len([c for c in failures if c in EXPECTED]),
        "failure_cases": failures,
        "real_service_used": False,
        "live_product_behavior_or_memory_proven": False,
        "transport_semantics_verified": "named cases only",
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--python-result", type=Path, required=True)
    p.add_argument("--javascript-result", type=Path, required=True)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    try:
        py = json.loads(a.python_result.read_text(encoding="utf-8"))
        js = json.loads(a.javascript_result.read_text(encoding="utf-8"))
        result = compare(py, js)
    except (OSError, ValueError, UnicodeDecodeError):
        result = {"status": "INCOMPLETE_UNREADABLE_EVIDENCE", "matched": 0,
                  "case_count": len(EXPECTED), "failure_cases": [], "real_service_used": False}
    body = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")
    print(result["status"], file=sys.stderr)
    return 0 if result["status"] == "SCOPED_EQUIVALENCE" else 2

if __name__ == "__main__":
    sys.exit(main())
