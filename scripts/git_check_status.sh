#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="$HOME"
REPOS=(
  "setup_guides"
  "sofia-utils"
  "wa-agents"
  "sofia-server"
  "da-assistant"
  "ieced"
  "tia-chabots"
  "tv_model_guided"
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
