#!/usr/bin/env python3
"""Validate a point-in-time derived Company queue; no writes, network, or execution."""
import argparse
import collections
import json
from pathlib import Path

ROUTE = {
    "delegated_candidate": "prepare_within_existing_envelope",
    "reconciliation_required": "read_only_reconciliation",
    "blocked_dependency": "blocked",
    "waiting_external": "watch",
    "deferred": "hold",
}
SECTIONS = ["protect_now", "owner_action_required", "delegated_work",
            "cash_commitments", "portfolio_review_triggers", "reference_implementation_evidence"]


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def validate(source, projection):
    require(projection["derived"] is True and all(
        projection[k] is False for k in ("canonical_authority", "organizational_authority_provided",
        "execution_authorized", "complete_company_coverage")), "derived boundary")
    expected = {}
    for c in source["cards"]:
        for a in c["next"]:
            key = (c["label"], a["ref"])
            require(key not in expected, "duplicate source action")
            expected[key] = (c, a)
    observed = {}
    controls = set(x for domain in ("control", "decision", "risk")
                   for x in projection["private_source_observation"][domain]["record_refs"])
    for item in projection["items"]:
        key = tuple(item["source_key"])
        require(key in expected and key not in observed, "missing/duplicate/unknown source key")
        c, a = expected[key]
        require(item["project"] == c["label"] and item["action"] == a["action"]
                and item["source_queue"] == a["queue"] and item["queue"] == ROUTE[a["queue"]]
                and item["source_refs"] == c["sources"]
                and item["project_due_or_trigger"] == c["due_or_trigger"]
                and item["unknowns"] == c["unknowns"], "source drift")
        require(all(item[k] is False for k in ("execution_authorized", "actual_acceptance_verified",
                                               "owner_decision_ready")), "implicit authorization/acceptance")
        require(set(item["related_control_refs"]) <= controls, "unknown control reference")
        observed[key] = item
    require(set(observed) == set(expected), "lost source action")
    require(set(projection["project_details"]) == {c["label"] for c in source["cards"]}, "lost project")
    for c in source["cards"]:
        p = projection["project_details"][c["label"]]
        require(p["source_refs"] == c["sources"] and p["subviews"] == c.get("subviews",[])
                and p["stage"] == c["stage"], "lost project detail/subview")
    require([s["key"] for s in projection["sections"]] == SECTIONS, "section structure")
    for section in projection["sections"]:
        for entry in section["entries"]:
            require(all(tuple(k) in observed for k in entry.get("action_keys", [])), "unknown action link")
            require(set(entry.get("record_refs", [])) <= controls, "unknown section control")
            require(entry.get("execution_authorized", False) is False, "section authorizes effect")
    owner = projection["sections"][1]
    require(not owner["entries"] and projection["counts"]["decision_ready_owner_items"] == 0,
            "owner approval not established in bounded snapshot")
    require(set(owner.get("preparation_refs", [])) <= controls, "unknown preparing decision")
    require(projection["counts"]["actions"] == len(expected)
            and projection["counts"]["projects"] == len(source["cards"]), "bad source counts")
    counts = collections.Counter(i["queue"] for i in observed.values())
    require(dict(counts) == projection["counts"]["queues"], "bad queue counts")
    require(projection["sections"][3]["financial_visibility"]["available_cash"] == "unknown"
            and projection["sections"][3]["financial_visibility"]["payment_authority"] is False,
            "invented finance or payment authority")
    return {"projects": len(source["cards"]), "actions": len(expected), "queues": dict(counts)}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("projection", type=Path)
    a = p.parse_args()
    print(json.dumps(validate(json.loads(a.source.read_text()), json.loads(a.projection.read_text())),
                     ensure_ascii=False))
