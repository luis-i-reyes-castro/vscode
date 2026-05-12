#!/usr/bin/env bash

set -euo pipefail

UNTRACKED_FILES=(
  ".git-credentials"
  "vscode/nacho.code-workspace"
  "vscode/.cursor/rules.mdc"
  "da-assistant/.env"
  "customer-loyalty/.env"
  "aitrol/.env"
  "ieced/.env"
)

# Detect source OS and target OS
cd ~
OS_NAME="$(uname -s)"
if [[ "$OS_NAME" == "Linux" ]]; then
  SOURCE="linux"
  TARGET="macbook"
elif [[ "$OS_NAME" == "Darwin" ]]; then
  SOURCE="mac"
  TARGET="ubuntu"
else
  echo "Incompatible OS: $OS_NAME"
  exit 1
fi

echo_sep() { 
  echo "$(printf -- "${2:-=}%.0s" $(seq 1 "${1:-92}"))"
}

echo_sep
echo "DIFF BETWEEN UNTRACKED FILES"
echo "Source: $SOURCE"
echo "Target: $TARGET"

for file in "${UNTRACKED_FILES[@]}"; do
  local_file="$HOME/$file"
  remote_file="~/$file"

  echo_sep
  echo "FILE: ~/$file"

  if [[ ! -f "$local_file" ]]; then
    echo "Local file missing: $local_file"
    continue
  fi

  if ! remote_contents="$(ssh "$TARGET" "cat $remote_file" 2>&1)"; then
    echo "Could not read remote file: $remote_file on $TARGET"
    echo "$remote_contents"
    continue
  fi

  if command -v colordiff >/dev/null 2>&1; then
    # diff exits with 1 when files differ; do not stop the script.
    printf '%s\n' "$remote_contents" | colordiff -u - "$local_file" || true
  else
    printf '%s\n' "$remote_contents" | diff -u - "$local_file" || true
  fi
done

echo "---"
exit 0
