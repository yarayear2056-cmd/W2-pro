from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Paths:
    root: Path
    raw: Path
    processed: Path
    external: Path
    cache: Path
    reports: Path 


def make_paths(root: Path) -> Paths:
    data = root / "data"
    return Paths(
        root=root,
        raw=data / "raw",
        cache=data / "cache",
        processed=data / "processed",
        external=data / "external",
        reports=root / "reports",
    )