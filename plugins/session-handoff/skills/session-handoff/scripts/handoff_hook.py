#!/usr/bin/env python3
"""SessionStart hook for Claude Code and Codex CLI.

If .handoff/HANDOFF.md (in the session's cwd or any parent) has
`status: pending` and is recent, print it to stdout so the new session
receives it as context, then mark it `status: consumed`.
Prints nothing (exit 0) in every other case, so it never blocks a session.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

MAX_AGE_DAYS = 7
MAX_CHARS = 12000
INJECT_SOURCES = {"startup", "clear", ""}  # skip resume / compact


def find_handoff(start: Path):
    for d in [start, *start.parents]:
        p = d / ".handoff" / "HANDOFF.md"
        if p.is_file():
            return p
    return None


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}
    if str(payload.get("source", "")) not in INJECT_SOURCES:
        return
    cwd = Path(payload.get("cwd") or Path.cwd())
    path = find_handoff(cwd)
    if not path:
        return
    text = path.read_text(encoding="utf-8")
    if not re.search(r"^status:\s*pending\s*$", text, re.M):
        return
    m = re.search(r"^created:\s*(\S+)", text, re.M)
    if m:
        try:
            created = datetime.fromisoformat(m.group(1)[:19])
            if (datetime.now() - created).days > MAX_AGE_DAYS:
                return
        except ValueError:
            pass

    body = text if len(text) <= MAX_CHARS else (
        text[:MAX_CHARS] + f"\n\n[...잘림. 전체는 {path} 를 읽을 것]"
    )
    out = (
        "=== 이전 세션 인수인계 (HANDOFF) ===\n"
        f"파일: {path}\n"
        "새 세션의 첫 응답에서: (1) 아래 내용을 바탕으로 목표·현재 상태·다음 할 일을 "
        "3줄로 요약하고, (2) 사용자 확인을 받은 뒤 '다음에 할 일'의 첫 항목부터 이어서 진행한다. "
        "사용자의 첫 메시지가 다른 요청이면 그 요청을 우선한다.\n\n"
        + body
    )
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(out)

    stamp = datetime.now().isoformat(timespec="seconds")
    new = re.sub(r"^status:\s*pending\s*$",
                 f"status: consumed\nconsumed: {stamp}", text, count=1, flags=re.M)
    path.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # never break session start
    sys.exit(0)
