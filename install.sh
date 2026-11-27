#!/usr/bin/env bash
# Cai skill thiet ke cau duong bo VN cho Claude Code / Codex / Gemini / OpenCode.
# Mac dinh: symlink TOAN BO thu muc skills/* vao moi dich trong TARGETS.
#   ./install.sh                            -> cai moi skill
#   ./install.sh cau-11823 duong-4054       -> cai co ban nay (tuong lai co nhieu mang)
#   ./install.sh --list                     -> liet ke skill co trong repo
#   ./install.sh --uninstall [ten...]       -> go lien ket (khong ten = go het; repo giu nguyen)
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGETS=("$HOME/.claude/skills" "$HOME/.agents/skills")

UNINSTALL=0
LIST=0
SELECTED=()
for arg in "$@"; do
  case "$arg" in
    --uninstall|-u) UNINSTALL=1 ;;
    --list|-l)      LIST=1 ;;
    -*) echo "Lenh khong ro: $arg (xem ./install.sh --help qua doc README)" >&2; exit 1 ;;
    *)  SELECTED+=("$arg") ;;
  esac
done

list_skills() { local s; for s in "$REPO_DIR"/skills/*/; do [ -d "$s" ] && basename "$s"; done; }

if [ "$LIST" = 1 ]; then
  echo "Skill co trong repo:"
  list_skills | sed 's/^/  /'
  exit 0
fi

# Khong chi ten = ca bo; chi ten = kiem ton tai truoc khi tao lien ket
SKILLS=()
if [ "${#SELECTED[@]}" -eq 0 ]; then
  while IFS= read -r n; do SKILLS+=("$n"); done < <(list_skills)
else
  for n in "${SELECTED[@]}"; do
    if [ ! -d "$REPO_DIR/skills/$n" ]; then
      echo "Khong thay skills/$n. Skill co trong repo:" >&2
      list_skills | sed 's/^/  /' >&2
      exit 1
    fi
    SKILLS+=("$n")
  done
fi

for target in "${TARGETS[@]}"; do
  if [ "$UNINSTALL" = 1 ]; then
    for name in "${SKILLS[@]}"; do
      if [ -L "$target/$name" ]; then
        rm "$target/$name"
        echo "Unlinked $name <- $target/$name"
      fi
    done
    continue
  fi
  mkdir -p "$target"
  for name in "${SKILLS[@]}"; do
    skill="$REPO_DIR/skills/$name"
    if [ -e "$target/$name" ] && [ ! -L "$target/$name" ]; then
      echo "BO QUA $name -> $target/$name (ton tai ban khac symlink; tu tay xoa neu muon ghi de)"
      continue
    fi
    ln -sfn "$skill" "$target/$name"
    echo "Linked $name -> $target/$name"
  done
done

if [ "$UNINSTALL" = 1 ]; then
  echo "Xong. Chi xoa lien ket, repo va noi dung giu nguyen."
  exit 0
fi

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
