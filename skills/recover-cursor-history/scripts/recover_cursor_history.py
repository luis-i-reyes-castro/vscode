#!/usr/bin/env python3
"""Inspect and safely restore files from Cursor's local history."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname


def standard_history_roots() -> list[Path]:
    home = Path.home()
    roots = [
        home / ".config/Cursor/User/History",
        home / "Library/Application Support/Cursor/User/History",
    ]
    appdata = os.environ.get("APPDATA")
    if appdata:
        roots.append(Path(appdata) / "Cursor/User/History")
    return roots


def resource_path(resource: str) -> Path | None:
    parsed = urlparse(resource)
    if parsed.scheme != "file":
        return None
    raw_path = url2pathname(parsed.path)
    if parsed.netloc and parsed.netloc not in ("", "localhost"):
        raw_path = f"//{parsed.netloc}{raw_path}"
    if os.name == "nt" and raw_path.startswith("/") and len(raw_path) > 2:
        if raw_path[2] == ":":
            raw_path = raw_path[1:]
    return Path(raw_path).expanduser().absolute()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_count(path: Path) -> int:
    count = 0
    last = b""
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            count += chunk.count(b"\n")
            last = chunk[-1:] or last
    return count + (1 if last and last != b"\n" else 0)


def local_time(milliseconds: object) -> str:
    if milliseconds is None:
        return "unknown"
    try:
        moment = dt.datetime.fromtimestamp(
            float(milliseconds) / 1000, tz=dt.timezone.utc
        )
    except (TypeError, ValueError, OverflowError, OSError):
        return "unknown"
    return moment.astimezone().isoformat(timespec="seconds")


def timestamp_value(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0


def matching_entries(target: Path, roots: list[Path]) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for root in roots:
        if not root.is_dir():
            continue
        for index in root.glob("*/entries.json"):
            try:
                payload = json.loads(index.read_text(encoding="utf-8"))
                indexed_path = resource_path(str(payload.get("resource", "")))
            except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError):
                continue
            if indexed_path != target:
                continue
            entries = payload.get("entries", [])
            if not isinstance(entries, list):
                continue
            for item in entries:
                if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                    continue
                snapshot_id = item["id"]
                if Path(snapshot_id).name != snapshot_id:
                    continue
                snapshot = index.parent / snapshot_id
                if not snapshot.is_file():
                    continue
                matches.append(
                    {
                        "id": snapshot_id,
                        "timestamp": item.get("timestamp"),
                        "snapshot": snapshot,
                    }
                )
    matches.sort(
        key=lambda item: (timestamp_value(item["timestamp"]), str(item["snapshot"]))
    )
    return matches


def parse_mode(value: str) -> int:
    try:
        mode = int(value, 8)
    except ValueError as error:
        raise argparse.ArgumentTypeError("mode must be octal, such as 0600") from error
    if not 0 <= mode <= 0o777:
        raise argparse.ArgumentTypeError("mode must be between 0000 and 0777")
    return mode


def unique_backup_path(target: Path) -> Path:
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    candidate = target.with_name(f"{target.name}.pre-cursor-restore-{stamp}")
    counter = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = target.with_name(
            f"{target.name}.pre-cursor-restore-{stamp}-{counter}"
        )
        counter += 1
    return candidate


def atomic_restore(
    snapshot: Path, target: Path, mode: int, overwrite: bool
) -> tuple[str, Path | None]:
    if target.is_symlink():
        raise RuntimeError("refusing to restore through a symlink destination")
    if not target.parent.is_dir():
        raise RuntimeError(f"destination parent does not exist: {target.parent}")
    if target.exists() and not target.is_file():
        raise RuntimeError("destination exists and is not a regular file")
    if target.exists() and not overwrite:
        raise RuntimeError("destination exists; inspect it or use --overwrite explicitly")

    backup: Path | None = None
    if target.exists():
        backup = unique_backup_path(target)
        shutil.copy2(target, backup, follow_symlinks=False)

    fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as destination, snapshot.open("rb") as source:
            shutil.copyfileobj(source, destination)
            destination.flush()
            os.fsync(destination.fileno())
        os.chmod(temporary, mode)
        if overwrite:
            os.replace(temporary, target)
        else:
            try:
                os.link(temporary, target)
            except FileExistsError as error:
                raise RuntimeError("destination appeared during restore; refusing overwrite") from error
            temporary.unlink()
        restored_hash = sha256(target)
        snapshot_hash = sha256(snapshot)
        if restored_hash != snapshot_hash:
            raise RuntimeError("post-restore SHA-256 mismatch")
        return restored_hash, backup
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and safely restore a file from Cursor User/History."
    )
    parser.add_argument("target", help="absolute or relative path originally edited in Cursor")
    parser.add_argument(
        "--history-root",
        action="append",
        type=Path,
        help="Cursor User/History directory; repeat to search multiple roots",
    )
    parser.add_argument(
        "--restore",
        metavar="ID",
        help="restore a listed snapshot ID, or 'latest'; omitted means inspect only",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing regular file after making a sibling backup",
    )
    parser.add_argument(
        "--mode",
        type=parse_mode,
        default=0o600,
        help="permissions for restored file in octal (default: 0600)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = Path(args.target).expanduser().absolute()
    roots = (
        [root.expanduser().absolute() for root in args.history_root]
        if args.history_root
        else standard_history_roots()
    )
    matches = matching_entries(target, roots)

    print(f"target={target}")
    print(f"matches={len(matches)}")
    for item in matches:
        snapshot = item["snapshot"]
        assert isinstance(snapshot, Path)
        print(
            "snapshot="
            f"{item['id']} timestamp={local_time(item['timestamp'])} "
            f"bytes={snapshot.stat().st_size} lines={line_count(snapshot)} "
            f"sha256={sha256(snapshot)}"
        )

    if not args.restore:
        return 0 if matches else 2
    if not matches:
        print("error=no matching Cursor history snapshots", file=sys.stderr)
        return 2

    if args.restore == "latest":
        selected = matches[-1]
    else:
        candidates = [item for item in matches if item["id"] == args.restore]
        if len(candidates) != 1:
            print("error=snapshot ID is missing or ambiguous", file=sys.stderr)
            return 2
        selected = candidates[0]

    snapshot = selected["snapshot"]
    assert isinstance(snapshot, Path)
    try:
        digest, backup = atomic_restore(snapshot, target, args.mode, args.overwrite)
    except (OSError, RuntimeError) as error:
        print(f"error={error}", file=sys.stderr)
        return 1

    print(f"restored={target}")
    print(f"selected={selected['id']} timestamp={local_time(selected['timestamp'])}")
    print(f"mode={stat.S_IMODE(target.stat().st_mode):04o}")
    print(f"verified_sha256={digest}")
    if backup:
        print(f"backup={backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
