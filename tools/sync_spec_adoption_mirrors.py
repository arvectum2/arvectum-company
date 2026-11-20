#!/usr/bin/env python3
"""Only two owner-directed main refs; no force, prune, tags or branch deletion."""
import argparse
import os
import subprocess
import tempfile
from pathlib import Path

PINS = (
    ("creative-test-agent", "aeae858fae079ed681eedfc4e35462747e5ea412", "161e27f0d42877af75c68b683753ca031f47fc99"),
    ("doors_parser", "ae0dbcf2cb062ffa5c986db0f313e3fb2ba4f7c0", "48d7cf1dd9b0040087a77793c5126164194c3ac1"),
)
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0")
REF = "refs/heads/main"

def run(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV, text=True).strip()

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def remote_sha(root, url):
    rows = run(root, "ls-remote", "--exit-code", url, REF).splitlines()
    require(len(rows) == 1 and rows[0].split()[1] == REF, "unexpected ref response")
    return rows[0].split()[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="spec-mirror-fastforward-") as tmp:
        planned = []
        for name, old, new in PINS:
            root = Path(tmp) / name
            root.mkdir()
            run(root, "init", "-q")
            gh = "https://github.com/arvectum2/" + name + ".git"
            gv = "https://gitverse.ru/arvectum/" + name + ".git"
            require(remote_sha(root, gh) == new, name + ": canonical changed")
            current = remote_sha(root, gv)
            require(current in (old, new), name + ": mirror changed; stop")
            if current == old:
                run(root, "fetch", "--no-tags", "--depth=16", gh, REF)
                require(run(root, "rev-parse", "FETCH_HEAD") == new, name + ": fetch pin")
                run(root, "merge-base", "--is-ancestor", old, new)
            planned.append((name, root, gh, gv, current, new))
            print(name, "fast-forward" if current != new else "already synced", current, "->", new, flush=True)
        if not args.apply:
            return
        # Recheck exact refs after all preparation, before either push.
        for name, root, gh, gv, current, new in planned:
            require(remote_sha(root, gh) == new and remote_sha(root, gv) == current, name + ": ref changed")
        for name, root, gh, gv, current, new in planned:
            if current != new:
                # Normal fast-forward-only push. No other refs, no force/prune.
                run(root, "push", "--porcelain", gv, new + ":" + REF)
            require(remote_sha(root, gv) == new and remote_sha(root, gh) == new, name + ": final ref verification")
            print(name, "PASS", new, flush=True)

if __name__ == "__main__":
    main()
