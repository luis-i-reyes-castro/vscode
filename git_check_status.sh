#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="$HOME"
REPOS=(
  "sofia-utils"
  "wa-agents"
  "da-assistant"
  "customer-loyalty"
  "aitrol"
  "ieced"
  "S3_storage"
  "setup_guides"
)

cd ~
for repo in "${REPOS[@]}"; do
  repo_path="$BASE_DIR/$repo"
  if [[ ! -d "$repo_path" ]]; then
    echo "Directory not found: $repo_path" >&2
    continue
  fi
  echo "===== $repo ====="
  (
    cd "$repo_path"
    git status
  )
  echo
done
