#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <source-skill-dir>" >&2
  exit 1
fi

src="${1%/}"

if [[ ! -d "$src" ]]; then
  echo "Source directory not found: $src" >&2
  exit 1
fi

if [[ ! -f "$src/SKILL.md" ]]; then
  echo "Source skill is missing SKILL.md: $src" >&2
  exit 1
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_name="$(basename "$src")"
dest="$repo_root/codex-skills/$skill_name"

if [[ -e "$dest" ]]; then
  echo "Destination already exists: $dest" >&2
  exit 1
fi

mkdir -p "$(dirname "$dest")"
cp -a "$src" "$dest"

echo "Imported Codex skill:"
echo "  source: $src"
echo "  target: $dest"
