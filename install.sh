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
# Kiem tra Python 3.10+ - skill chay scripts/bridge_calc.py
PY="$(command -v python3 || command -v python || true)"
if [ -n "$PY" ] && "$PY" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
  echo "Python: $("$PY" --version 2>&1)"
else
  echo "CAN Python 3.10+ de chay bridge_calc.py (tim thay: ${PY:-khong co})." >&2
  echo "  Linux/WSL: sudo apt install python3 | macOS: brew install python" >&2
  echo "  Windows:   winget install Python.Python.3.12 (mo lai Terminal sau khi cai)" >&2
fi

echo "Xong. Mo lai session agent de no nhan skill moi."
