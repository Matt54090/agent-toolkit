#!/usr/bin/env python3
"""계약서·법률문서의 민감정보를 로컬에서 가리고(mask) 되돌린다(restore).

사용법:
  python3 pii_mask.py mask <파일(.txt|.md|.docx)> [--names "홍길동,가나다 주식회사"] [--terms "서울시 ○○로 12"]
      -> <이름>.masked.txt, <이름>.pii-map.json 생성 (map 파일에는 원래 값이 들어 있으니 공유 금지)
  python3 pii_mask.py restore <가린 상태로 수정된 파일> <이름>.pii-map.json [-o 출력경로]
      -> 토큰을 원래 값으로 되돌린 파일 생성

AI에게는 .masked.txt만 읽게 한다. 표준 라이브러리만 쓰며, .docx 읽기에만 python-docx가 필요하다.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

TOKEN_FMT = "{{{{PII:{kind}_{n}}}}}"  # -> {{PII:RRN_1}}
TOKEN_RE = re.compile(r"\{\{PII:([A-Z]+)_(\d+)\}\}")

# (종류, 정규식, 값이 들어 있는 그룹 번호)
PATTERNS = [
    # 주민등록번호·외국인등록번호: YYMMDD-[1-8]XXXXXX, 월·일 범위 확인
    ("RRN", re.compile(r"(?<!\d)(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\s?[-–]?\s?[1-8]\d{6})(?!\d)"), 1),
    # 카드번호 16자리(구분자 허용)
    ("CARD", re.compile(r"(?<!\d)(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})(?!\d)"), 1),
    # 여권번호(구형 M12345678, 신형 M123A4567)
    ("PASSPORT", re.compile(r"(?<![A-Za-z0-9])([MSRODG]\d{8}|[MSRODG]\d{3}[A-Z]\d{4})(?![A-Za-z0-9])"), 1),
    # 계좌번호: '계좌/입금/account' 뒤 20자 안에 나오는 숫자열
    ("ACCOUNT", re.compile(r"(?:계좌|입금|account)[^\n\d]{0,20}(\d[\d-]{8,18}\d)", re.IGNORECASE), 1),
    # 사업자등록번호
    ("BIZNO", re.compile(r"(?<!\d)(\d{3}-\d{2}-\d{5})(?!\d)"), 1),
    # 전화번호
    ("PHONE", re.compile(r"(?<!\d)(0\d{1,2}[- .]?\d{3,4}[- .]?\d{4})(?!\d)"), 1),
    # 이메일
    ("EMAIL", re.compile(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"), 1),
]


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        try:
            from docx import Document  # python-docx
        except ImportError:
            sys.exit("python-docx가 필요합니다: pip install python-docx")
        doc = Document(str(path))
        parts = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text for cell in row.cells))
        return "\n".join(parts)
    return path.read_text(encoding="utf-8", errors="replace")


def mask(text: str, names, terms):
    value_to_token: dict[str, str] = {}
    counters: dict[str, int] = {}

    def token_for(kind: str, value: str) -> str:
        if value not in value_to_token:
            counters[kind] = counters.get(kind, 0) + 1
            value_to_token[value] = TOKEN_FMT.format(kind=kind, n=counters[kind])
        return value_to_token[value]

    # 사용자가 지정한 이름·문구를 먼저(긴 것부터) 가린다
    for kind, items in (("NAME", names), ("TERM", terms)):
        for item in sorted({i.strip() for i in items if i.strip()}, key=len, reverse=True):
            text = text.replace(item, token_for(kind, item))

    for kind, pattern, group in PATTERNS:
        def _sub(m, kind=kind, group=group):
            whole, value = m.group(0), m.group(group)
            if TOKEN_RE.search(whole):
                return whole
            return whole.replace(value, token_for(kind, value))
        text = pattern.sub(_sub, text)

    mapping = {tok: val for val, tok in value_to_token.items()}
    return text, mapping, counters


def restore(text: str, mapping: dict):
    used, unknown = set(), set()

    def _sub(m):
        tok = m.group(0)
        if tok in mapping:
            used.add(tok)
            return mapping[tok]
        unknown.add(tok)
        return tok

    restored = TOKEN_RE.sub(_sub, text)
    missing = sorted(set(mapping) - used)
    return restored, missing, sorted(unknown)


def main():
    ap = argparse.ArgumentParser(description="법률문서 민감정보 로컬 마스킹/복원")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mask")
    m.add_argument("file")
    m.add_argument("--names", default="", help="쉼표로 구분한 이름·상호")
    m.add_argument("--terms", default="", help="쉼표로 구분한 추가 문구(주소 등)")
    r = sub.add_parser("restore")
    r.add_argument("file")
    r.add_argument("map")
    r.add_argument("-o", "--output")
    args = ap.parse_args()

    if args.cmd == "mask":
        src = Path(args.file)
        masked, mapping, counters = mask(read_text(src), args.names.split(","), args.terms.split(","))
        out = src.with_name(src.stem + ".masked.txt")
        map_path = src.with_name(src.stem + ".pii-map.json")
        out.write_text(masked, encoding="utf-8")
        map_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            os.chmod(map_path, 0o600)
        except OSError:
            pass
        summary = ", ".join(f"{k} {v}건" for k, v in sorted(counters.items())) or "가린 항목 없음"
        print(f"가린 사본: {out}")
        print(f"복원표(원래 값 포함, 공유 금지): {map_path}")
        print(f"요약: {summary}")
        print("주의: 정규식 기반이라 주소·이름은 --names/--terms로 지정해야 가려집니다.")
    else:
        src = Path(args.file)
        mapping = json.loads(Path(args.map).read_text(encoding="utf-8"))
        restored, missing, unknown = restore(src.read_text(encoding="utf-8"), mapping)
        out = Path(args.output) if args.output else src.with_name(src.stem.replace(".masked", "") + ".restored" + (src.suffix or ".txt"))
        out.write_text(restored, encoding="utf-8")
        print(f"복원본: {out}")
        if missing:
            print(f"원문에 있었지만 수정본에 없는 토큰 {len(missing)}개: {', '.join(missing)}")
        if unknown:
            print(f"복원표에 없는 토큰 {len(unknown)}개(그대로 둠): {', '.join(unknown)}")


if __name__ == "__main__":
    main()
