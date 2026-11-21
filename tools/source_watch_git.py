"""Git-first public evidence for Company source watch, REST only as fallback.

Only the approved snapshot's canonical references are addressable. Private bare
caches are non-canonical; no shell, token, browser session or working clone.
"""
import fcntl
import os
from pathlib import Path
import re
import stat
import subprocess

SHA = re.compile(r"[0-9a-f]{40}")
ROUTE = re.compile(r"/repos/arvectum2/([A-Za-z0-9_.-]{1,96})/(branches/main|compare/([a-f0-9]{40})\.\.\.([a-f0-9]{40}))")


class GitUnavailable(Exception):
    pass


class GitPublicEvidence:
    def __init__(self, root, baseline, fallback, *, unavailable=GitUnavailable):
        self.root = Path(root)
        self.fallback = fallback
        self.unavailable = unavailable
        self.refs = {}
        self.heads = {}
        for entry in baseline["project_details"].values():
            for source in entry["source_refs"]:
                if source["scope"] == "canonical_commit":
                    self.refs.setdefault(source["repo"], set()).add(source["ref"])
        if not self.root.is_absolute() or self.root.resolve() != self.root:
            raise ValueError("Git evidence cache path invalid")

    def _private(self, path):
        if path.is_symlink():
            raise ValueError("symlink in evidence cache")
        path.mkdir(mode=0o700, exist_ok=True)
        s = path.lstat()
        if not stat.S_ISDIR(s.st_mode) or s.st_uid != os.getuid() or s.st_mode & 0o077:
            raise ValueError("evidence cache permissions invalid")

    def _git(self, *argv, allow_failure=False):
        args = ["/usr/bin/git", "-c", "credential.helper=", "-c", "core.hooksPath=/dev/null",
                "-c", "protocol.file.allow=never", "-c", "protocol.ssh.allow=never", *argv]
        env = {"PATH": "/usr/bin:/bin", "HOME": str(self.root), "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_TERMINAL_PROMPT": "0",
               "GIT_ASKPASS": "/usr/bin/false", "GIT_SSH_COMMAND": "/usr/bin/false", "LC_ALL": "C"}
        try:
            p = subprocess.run(args, env=env, capture_output=True, timeout=25, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise GitUnavailable("git_transport_unavailable") from exc
        if p.returncode and not allow_failure:
            err = p.stderr.decode("utf-8", "replace").lower()
            if "could not read username" in err or "repository not found" in err or "authentication failed" in err:
                raise GitUnavailable("not_public_or_not_found")
            raise GitUnavailable("git_transport_unavailable")
        if len(p.stdout) > 8*1024*1024:
            raise GitUnavailable("git_output_over_limit")
        return p

    def _url(self, repo):
        return f"https://github.com/arvectum2/{repo}.git"

    def fetch(self, route):
        m = ROUTE.fullmatch(route)
        if not m or m[1] not in self.refs:
            raise ValueError("source route not admitted")
        repo = m[1]
        if m[2] == "branches/main":
            try:
                raw = self._git("ls-remote", self._url(repo), "refs/heads/main").stdout
                parts = raw.decode("ascii", "strict").split()
                if len(parts) != 2 or not SHA.fullmatch(parts[0]) or parts[1] != "refs/heads/main":
                    raise GitUnavailable("git_main_unavailable")
                self.heads[repo] = parts[0]
                return {"commit": {"sha": parts[0]}}
            except GitUnavailable as exc:
                if str(exc) == "not_public_or_not_found":
                    raise self.unavailable("not_public_or_not_found") from None
                return self.fallback(route)
            except UnicodeError:
                return self.fallback(route)
        prior, target = m[3], m[4]
        if prior not in self.refs[repo] or target != self.heads.get(repo):
            raise ValueError("unverified comparison request")
        try:
            return self._compare(repo, prior, target)
        except GitUnavailable:
            return self.fallback(route)

    def _compare(self, repo_name, prior, target):
        self._private(self.root)
        repo = self.root / (repo_name + ".git")
        lock = self.root / (repo_name + ".lock")
        flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(lock, flags, 0o600)
        try:
            s = os.fstat(fd)
            if not stat.S_ISREG(s.st_mode) or s.st_uid != os.getuid() or s.st_mode & 0o077:
                raise ValueError("evidence lock not private")
            fcntl.flock(fd, fcntl.LOCK_EX)
            if not repo.exists():
                self._private(repo)
                self._git("init", "--bare", "--quiet", str(repo))
                self._git("-C", str(repo), "remote", "add", "origin", self._url(repo_name))
            else:
                self._private(repo)
            remote = self._git("-C", str(repo), "remote", "get-url", "origin").stdout.decode("utf-8", "strict").strip()
            if remote != self._url(repo_name):
                raise ValueError("source cache points at different repository")
            observed = self._git("-C", str(repo), "rev-parse", "--verify", "refs/remotes/origin/main", allow_failure=True)
            old_present = self._git("-C", str(repo), "cat-file", "-e", prior + "^{commit}", allow_failure=True)
            if observed.returncode or observed.stdout.strip() != target.encode() or old_present.returncode:
                self._git("-C", str(repo), "fetch", "--quiet", "--no-tags", "--filter=blob:none",
                          "--depth=512", "origin", "+refs/heads/main:refs/remotes/origin/main")
            head = self._git("-C", str(repo), "rev-parse", "--verify", "refs/remotes/origin/main").stdout.strip().decode("ascii")
            if head != target:
                raise GitUnavailable("git_main_changed_during_scan")
            if self._git("-C", str(repo), "cat-file", "-e", prior+"^{commit}", allow_failure=True).returncode:
                raise GitUnavailable("git_baseline_outside_bounded_history")
            ancestry = self._git("-C", str(repo), "merge-base", "--is-ancestor", prior, target, allow_failure=True)
            if ancestry.returncode == 1:
                return {"status": "diverged", "files": []}
            if ancestry.returncode:
                raise GitUnavailable("git_ancestry_unavailable")
            ahead = self._git("-C", str(repo), "rev-list", "--count", prior+".."+target).stdout
            files_raw = self._git("-C", str(repo), "diff", "--name-status", "-z", "-M", prior, target).stdout
            fields = files_raw.split(b"\0")
            if fields[-1] == b"":
                fields.pop()
            files = []
            i = 0
            while i < len(fields):
                code = fields[i].decode("ascii", "strict"); i += 1
                if code.startswith("R") or code.startswith("C"):
                    old = fields[i].decode("utf-8", "strict"); new = fields[i+1].decode("utf-8", "strict"); i += 2
                    files.append({"filename": new, "previous_filename": old, "status": "renamed"})
                else:
                    path = fields[i].decode("utf-8", "strict"); i += 1
                    kind = {"A": "added", "D": "removed", "M": "modified", "T": "changed"}.get(code[:1], "modified")
                    files.append({"filename": path, "status": kind})
                if len(files) >= 300:
                    raise GitUnavailable("git_comparison_too_large")
            return {"status": "identical" if prior == target else "ahead", "ahead_by": int(ahead), "files": files}
        finally:
            os.close(fd)
