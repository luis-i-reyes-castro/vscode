#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="$HOME"
REPOS=(
  "setup-guides"
  "sofia-utils"
  "wa-agents"
  "sofia-server"
  "sofia-server/backend/case_handlers/da_assistant"
  "sofia-server/backend/case_handlers/ieced"
  "sofia-server/backend/case_handlers/tia_chatbots"
  "tv_model_guided"
)

cd ~
for repo in "${REPOS[@]}"; do
  repo_path="$BASE_DIR/$repo"
  if [[ ! -d "$repo_path" ]]; then
    echo "Directory not found: $repo_path" >&2
    continue
  fi
  (
    cd "$repo_path"
    branch="$(git symbolic-ref --quiet --short HEAD)" || branch=HEAD
    if ! git fetch --quiet --no-recurse-submodules origin "$branch"; then
      printf '\033[31m'
      trap 'printf "\033[0m"' EXIT
      echo "REPOSITORY: $repo"
      git -c color.status=false status
      echo "WARNING: Could not fetch origin; commit comparison skipped." >&2
      exit 0
    fi
    read -r ahead behind <<< "$(git rev-list --left-right --count HEAD...FETCH_HEAD)"
    if (( ahead > 0 || behind > 0 )) ||
      [[ -n "$(git ls-files --others --exclude-standard)" ]] ||
      git rev-parse --verify --quiet refs/stash >/dev/null; then
      printf '\033[93m'
      trap 'printf "\033[0m"' EXIT
    fi
    echo "REPOSITORY: ${repo}"
    git -c color.status=false status
  )
  echo
done
