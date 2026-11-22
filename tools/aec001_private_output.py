#!/usr/bin/env python3
"""Private atomic output for local Company read-only audit evidence.

No network access, source execution or organizational authority.
"""
import os
from pathlib import Path
import tempfile


def _git_checkout_parent(path):
    for parent in (path.parent,*path.parents):
        marker=parent/".git"
        if marker.exists() or marker.is_symlink():
            return True
    return False


def write_private_output(path,payload):
    """Reject Git/symlink targets and atomically write text with mode 0600.

    This protects against accidental Git publication, not hostile concurrent
    filesystem actors with access to output parent directories.
    """
    if not isinstance(payload,str):
        raise TypeError("private output payload must be text")
    target=Path(path).expanduser()
    if not target.is_absolute():
        target=Path.cwd()/target
    if target.is_symlink():
        raise ValueError("private output destination symlink forbidden")
    if _git_checkout_parent(target):
        raise ValueError("private output inside Git checkout forbidden")
    target=target.resolve(strict=False)
    if _git_checkout_parent(target):
        raise ValueError("private output inside Git checkout forbidden")
    target.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    temp=None
    try:
        with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",delete=False,
                                         dir=str(target.parent),
                                         prefix=".aec001-private-") as handle:
            temp=Path(handle.name)
            os.chmod(temp,0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp,target)
        temp=None
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)
