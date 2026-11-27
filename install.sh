#!/usr/bin/env bash
# Cai dat skill cau duong bo VN cho Claude Code / Codex / Gemini / OpenCode.
# Symlink toan bo thu muc skills/* vao moi dich trong TARGETS.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGETS=("$HOME/.claude/skills" "$HOME/.agents/skills")

# Chay: ./install.sh --uninstall  de go lien ket
if [ "${1:-}" = "--uninstall" ]; then
  for target in "${TARGETS[@]}"; do
    for skill in "$REPO_DIR"/skills/*/; do
      name="$(basename "$skill")"
      [ -L "$target/$name" ] && rm "$target/$name" && echo "Unlinked $name <- $target/$name"
    done
  done
  exit 0
fi

for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  for skill in "$REPO_DIR"/skills/*/; do
    [ -d "$skill" ] || continue
    name="$(basename "$skill")"
    if [ -e "$target/$name" ] && [ ! -L "$target/$name" ]; then
      echo "BO QUA $name -> $target/$name (ton tai ban khac symlink; tu tay xoa neu muon ghi de)"
      continue
    fi
    ln -sfn "$skill" "$target/$name"
    echo "Linked $name -> $target/$name"
  done
done
echo "Xong. Mo lai session agent de no nhan skill moi."
