"""Integrity-check helpers for per-task generators."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, Union

PathLike = Union[str, Path]


def fingerprint(path: PathLike) -> str:
    """Return the SHA-256 hex digest of `path`.

    The student notebook prints this fingerprint at startup; the tutor CLI
    prints the canonical fingerprint. A mismatch indicates the student
    modified or replaced the generator module.
    """
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint_many(paths: Iterable[PathLike]) -> str:
    """Combine the digests of multiple files into a single fingerprint.

    Useful when a task depends on more than one generator file (e.g. a
    `task_instances.py` plus a `helpers.py`).
    """
    h = hashlib.sha256()
    for p in sorted(str(x) for x in paths):
        h.update(p.encode("utf-8"))
        h.update(b"\n")
        h.update(Path(p).read_bytes())
        h.update(b"\n")
    return h.hexdigest()
