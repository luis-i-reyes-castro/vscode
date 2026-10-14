---
name: recover-cursor-history
description: Find and safely restore recently deleted, overwritten, renamed, or damaged local files from Cursor's User/History indexes and snapshots. Use when a user lost an untracked or ignored file, Git cannot recover it, Cursor may have edited it previously, or the missing file may contain secrets that must not be printed during recovery.
---

# Recover Cursor History

Recover a file from Cursor local history while minimizing writes and avoiding secret exposure. Prefer the bundled helper because it matches history entries by their indexed resource URI and validates snapshots without displaying their contents.

## Safety rules

- Start read-only. Do not recreate, overwrite, source, execute, or print the missing file while searching.
- Treat all snapshots as potentially sensitive. Report metadata, hashes, timestamps, line counts, and structural checks—not contents or values.
- Resolve the intended absolute path and likely spelling variants before restoring.
- Do not overwrite an existing destination without explicit user authorization. If authorized, preserve a sibling backup first.
- Restore secrets with mode `0600`. Use the helper's secure default unless the user needs another mode.
- Never source a recovered `.env` file for validation. Use a non-executing parser or a syntax-only check such as `bash -n` only when its format is shell-compatible.
- Keep Cursor's history snapshots intact after recovery.

## Workflow

### 1. Resolve the target

Confirm the exact absolute target path. Check likely directory spelling variants and whether the target currently exists. If it exists, determine whether the request is recovery of an older version rather than deletion.

Before focusing on Cursor, make quick read-only checks when useful: Git history/status, ignore rules, desktop Trash metadata, editor backups, and open deleted handles (`lsof +L1`). Do not let these checks expose secret values.

### 2. Inspect Cursor history

Run:

```bash
python3 scripts/recover_cursor_history.py /absolute/path/to/file
```

Run it from this skill directory, or use the script's absolute path. It searches standard Cursor history locations and lists matching snapshots from oldest to newest. Supply a nonstandard root when needed:

```bash
python3 scripts/recover_cursor_history.py /absolute/path/to/file \
  --history-root /path/to/Cursor/User/History
```

If no exact match appears, search `entries.json` files by target basename or a distinctive parent-directory fragment. Inspect only index metadata:

```bash
rg -l -uu -F 'lost-file-name' ~/.config/Cursor/User/History
```

Cursor history entries generally contain a `resource` file URI plus snapshot IDs and millisecond timestamps. Decode the resource URI rather than guessing which hashed directory belongs to the target.

### 3. Choose a snapshot

Prefer the newest valid snapshot unless the user wants an older state. Compare safe indicators across candidates:

- timestamp and byte size
- SHA-256 digest
- line count
- format-specific structural counts, such as assignment names without values

Do not assume the largest snapshot is correct. A newer snapshot may intentionally remove data, and a truncated snapshot may still parse.

### 4. Restore safely

For a missing destination, restore the newest snapshot:

```bash
python3 scripts/recover_cursor_history.py /absolute/path/to/file --restore latest
```

Or select a listed snapshot ID:

```bash
python3 scripts/recover_cursor_history.py /absolute/path/to/file --restore SNAPSHOT_ID
```

The helper writes atomically, defaults to mode `0600`, verifies the resulting hash, and refuses symlink destinations. To recover an older version over an existing regular file, obtain explicit authorization and use `--overwrite`; the helper first creates a timestamped sibling backup:

```bash
python3 scripts/recover_cursor_history.py /absolute/path/to/file \
  --restore SNAPSHOT_ID --overwrite
```

Use `--mode 0644` or another mode only when appropriate for the recovered file.

### 5. Validate without executing

Verify that the restored digest equals the selected snapshot digest, permissions are appropriate, ownership is expected, and parsing succeeds. Never reveal recovered secrets in the response. Report the source snapshot timestamp, verification result, destination, mode, and whether a pre-restore backup was made.

## Failure handling

If Cursor history has no match, continue with other non-destructive sources: VS Code/Cursor backup directories, Trash, shell history that may identify a rename, filesystem snapshots, cloud-sync version history, or open file descriptors. For ext4 block-level undelete, stop writes to the filesystem and explain that unmounting or imaging the volume is usually required; do not attempt invasive recovery on a mounted live filesystem without explicit approval.
