#!/usr/bin/env python3
"""Claude Code UserPromptSubmit 훅: 프롬프트에 주민·외국인등록번호나 카드번호가 있으면 막거나 경고한다.

환경변수 LEGAL_PII_GUARD
  block (기본) : 프롬프트 전송을 막고 사용자에게 이유를 보여 준다 (exit 2)
  warn         : 전송은 하되 Claude에게 "값을 다시 쓰지 말 것"이라는 맥락을 붙인다
  off          : 아무것도 하지 않는다
감지한 값은 어디에도 출력하지 않는다(종류와 개수만).
"""
import json
import os
import re
import sys

RRN = re.compile(r"(?<!\d)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\s?[-–]?\s?[1-8]\d{6}(?!\d)")
CARD = re.compile(r"(?<!\d)(\d{4})[- ]?(\d{4})[- ]?(\d{4})[- ]?(\d{4})(?!\d)")


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def findings(text: str) -> dict:
    found = {}
    n = len(RRN.findall(text))
    if n:
        found["주민·외국인등록번호"] = n
    cards = [m for m in CARD.finditer(text) if luhn_ok("".join(m.groups()))]
    if cards:
        found["카드번호"] = len(cards)
    return found


def main():
    mode = os.environ.get("LEGAL_PII_GUARD", "block").lower()
    if mode == "off":
        return 0
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # 입력을 못 읽으면 막지 않는다
    found = findings(data.get("prompt", "") or "")
    if not found:
        return 0
    summary = ", ".join(f"{k} {v}건" for k, v in found.items())
    if mode == "warn":
        print(f"[korean-legal-desk] 사용자 입력에 민감번호({summary})가 있습니다. 답변·파일에 그 값을 다시 쓰지 말고 자리표시자로 처리하세요.")
        return 0
    sys.stderr.write(
        f"[korean-legal-desk] 입력에 민감번호({summary})가 있어 전송을 막았습니다.\n"
        "값을 [주민등록번호] 같은 자리표시자로 바꾸거나, 파일이면 스킬의 scripts/pii_mask.py로 가린 뒤 다시 보내세요.\n"
        "의도적으로 보내야 하면 LEGAL_PII_GUARD=warn 으로 설정하세요.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
