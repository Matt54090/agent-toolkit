#!/usr/bin/env bash
# agent-toolkit의 모든 스킬을 Codex·Gemini CLI 공용 스킬 폴더로 복사한다.
# 사용: 저장소 폴더에서  bash scripts/sync-skills.sh [--target <경로>] [--force] [--only 이름1,이름2]
# 기본 대상: ~/.agents/skills  (Codex는 이 폴더를, Gemini CLI는 ~/.gemini/skills와 함께 이 폴더도 읽는다)
# 같은 이름 폴더가 이미 있으면 건너뛴다. 덮어쓰려면 --force (기존 폴더는 .backup-<시각>으로 옮겨 둔다).
set -euo pipefail
target="$HOME/.agents/skills"; force=0; only=""
while [ $# -gt 0 ]; do
  case "$1" in
    --target) target="$2"; shift 2 ;;
    --force) force=1; shift ;;
    --only) only=",$2,"; shift 2 ;;
    *) echo "알 수 없는 옵션: $1" >&2; exit 1 ;;
  esac
done
repo="$(cd "$(dirname "$0")/.." && pwd)"
stamp="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$target"
for dir in "$repo"/plugins/*/skills/*/; do
  [ -f "$dir/SKILL.md" ] || continue
  name="$(basename "$dir")"
  if [ -n "$only" ] && [[ "$only" != *",$name,"* ]]; then continue; fi
  dest="$target/$name"
  if [ -e "$dest" ]; then
    if [ "$force" -ne 1 ]; then echo "건너뜀(이미 있음): $name  -> 덮어쓰려면 --force"; continue; fi
    mkdir -p "$target/.backup-$stamp" && mv "$dest" "$target/.backup-$stamp/$name"
    echo "기존 폴더 백업: $target/.backup-$stamp/$name"
  fi
  cp -R "$dir" "$dest"
  echo "복사: $name -> $dest"
done
echo "완료. Codex·Gemini CLI를 다시 시작하면 새 스킬이 잡힙니다."
