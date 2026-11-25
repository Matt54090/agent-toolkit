---
name: session-handoff
description: 지금 세션을 압축하지 않고 새 세션에서 이어가기 위해 인수인계 파일 .handoff/HANDOFF.md를 만들고 새 세션에 자동으로 넘기는 절차. Claude Code와 Codex CLI 공용. "핸드오프", "인수인계 파일 만들어줘", "새 세션에서 이어서 하자", "HANDOFF.md", "handoff to a new session", 컨텍스트가 무거워 세션을 갈아타려 할 때 반드시 사용.
---

# Session Handoff — 새 세션으로 인수인계

압축(/compact) 대신 새 세션을 열고 작업을 이어가야 할 때 쓴다. 이 스킬이 하는 일은 두 가지다.
1. 지금 세션의 맥락을 `.handoff/HANDOFF.md`로 남긴다.
2. 새 세션이 그 파일을 자동으로 받게 한다. 훅이 설치되어 있으면 완전 자동이고, 없으면 시작 명령 한 줄로 넘긴다.

새 세션은 이 대화를 전혀 보지 못한다. HANDOFF.md만 읽고 바로 다음 행동을 할 수 있어야 한다. 그래서 "무엇을 했는지"보다 "다음에 무엇을 하면 되는지"와 "무엇을 다시 하면 안 되는지"가 더 중요하다.

## 1단계: 정보 모으기

대화 전체를 다시 훑으며 아래를 뽑는다. 기억에 의존하지 말고, 파일이나 명령 출력으로 확인할 수 있는 것은 확인한다.

- 목표와 완료 기준
- 끝난 것 / 진행 중인 것 / 남은 것
- 확정된 결정과 그 이유. 특히 사용자가 고치거나 거절한 것
- 실패한 시도와 원인. 새 세션이 같은 실수를 반복하지 않게 하기 위함
- 건드린 파일과 핵심 위치(파일:줄, 함수 이름)
- 이 세션에서 드러난 사용자의 작업 규칙과 선호
- 아직 결정되지 않은 질문
- 완료를 확인하는 방법(테스트 명령, 기대 출력)

작업 폴더가 git 저장소이면 아래 명령을 실행해서 실제 상태를 함께 기록한다. 대화 기억보다 이쪽이 정확하다.
```
git branch --show-current
git status --short
git log --oneline -5
```

## 2단계: HANDOFF.md 쓰기

경로는 작업 폴더(프로젝트 루트, git 저장소면 저장소 루트) 아래 `.handoff/HANDOFF.md`다. 이미 이 파일이 있으면 덮어쓰지 말고 `.handoff/archive/HANDOFF-<기존 created 값>.md`로 옮긴 뒤 새로 쓴다.

맨 위의 frontmatter 형식은 정확히 지켜야 한다. 훅 스크립트가 `status: pending` 줄과 `created:` 줄을 읽어서 주입 여부를 판단하기 때문이다.

```markdown
---
status: pending
created: 2026-11-18T19:40:00
from: Claude Code (claude-opus-5-5)   # 또는 Codex CLI (모델명)
project: C:/Users/newpa/projects/example
---
# HANDOFF — <작업 이름>

## 한 줄 요약
<무엇을 하던 중이고, 어디까지 왔는지>

## 목표와 완료 기준
- 목표:
- 완료 기준:

## 현재 상태
- 완료:
- 진행 중:
- 남은 것:

## 다음에 할 일 (순서대로)
1. <새 세션이 가장 먼저 할 구체적 행동. 파일·명령까지 적는다>
2.

## 확정된 결정
- <결정> — 이유: <...>

## 실패한 시도 (반복 금지)
- <시도> → <결과/원인>

## 관련 파일
- `path/to/file.py:120` — <역할>

## 사용자 규칙·선호 (이 세션에서 확인된 것)
-

## 미해결 질문
-

## 검증 방법
- `<명령>` → <기대 결과>

## 저장소 상태 (git인 경우)
- 브랜치: / 커밋되지 않은 변경: / 최근 커밋:
```

작성 원칙:
- `created`는 로컬 시각을 `YYYY-MM-DDTHH:MM:SS` 형식으로 쓴다. 훅은 7일이 지난 파일을 무시한다.
- 해당 내용이 없는 섹션은 지우지 말고 "없음"이라고 쓴다. 비어 있으면 새 세션이 확인을 안 한 것인지 정말 없는 것인지 구분할 수 없다.
- 길이는 대략 150줄, 12,000자 이내로 맞춘다. 이보다 길면 훅이 뒷부분을 잘라서 넣는다. 긴 로그나 출력은 `.handoff/notes/`에 별도 파일로 두고 HANDOFF.md에는 경로만 적는다.
- 비밀값(API 키, 토큰, 비밀번호)은 값을 적지 않고 종류와 위치만 적는다. 예: "OpenAI 키 — `.env`의 OPENAI_API_KEY".
- 확인한 사실과 추정을 구분한다. 확인하지 않은 내용에는 `(미확인)`을 붙인다.

git 저장소에서 `.handoff/`가 `.gitignore`에 없으면, 커밋에 섞이지 않도록 추가할지 보고 때 한 줄로 제안한다. 직접 수정하지는 않는다.

## 3단계: 새 세션에 넘기기

훅이 설치되어 있는지 확인한다. 아래 두 파일 중 하나에 `handoff_hook.py`가 등록되어 있으면 설치된 것이다.
- Claude Code: `~/.claude/settings.json`
- Codex: `~/.codex/hooks.json`

읽을 수 없거나 확신이 서지 않으면, 아래 A와 B를 모두 안내한다.

**A. 훅이 설치된 경우 (완전 자동)**
같은 폴더에서 새 세션을 열기만 하면 된다. `claude` 또는 `codex`를 새로 실행하거나, 현재 창에서 `/clear`를 입력한다. 훅이 HANDOFF.md를 넣어 주고, 파일 상태를 `consumed`로 바꿔서 같은 내용이 두 번 들어가지 않게 한다. 다른 도구로 넘겨도 된다. 예를 들어 Claude에서 만든 인수인계를 Codex에서 받을 수 있다.

**B. 훅이 없는 경우 (시작 명령으로 넘기기)**
작업 폴더에서 아래 명령으로 새 세션을 시작한다.
```
claude "Read .handoff/HANDOFF.md, summarize goal, status and next step in 3 lines, then wait for my confirmation."
codex  "Read .handoff/HANDOFF.md, summarize goal, status and next step in 3 lines, then wait for my confirmation."
```
B 방식에서는 상태가 자동으로 `consumed`로 바뀌지 않는다. 새 세션이 파일을 읽은 뒤 첫 줄의 `status: pending`을 `status: consumed`로 직접 바꾸도록 안내한다.

훅 설치 방법은 이 스킬 폴더의 `references/install.md`에 있다. 사용자가 설치를 원하면 그 파일을 읽고 그대로 안내한다. 파일이 없으면(SKILL.md만 저장된 경우) 받은 session-handoff 묶음 안의 install.md를 참고하라고 알려준다.

## 4단계: 보고

짧게 알린다.
- HANDOFF.md 경로와 "다음에 할 일" 첫 항목
- 새 세션을 여는 방법 (A 또는 B)
- `.gitignore` 제안이 있으면 그것도 한 줄로

## 새 세션 쪽에서 할 일

HANDOFF가 주입되었거나 읽으라는 요청을 받았다면 이렇게 한다.
1. 목표, 현재 상태, 다음 할 일을 3줄로 요약하고 사용자에게 확인을 받는다.
2. "저장소 상태"와 "관련 파일"이 실제와 맞는지 빠르게 확인한다. 그 사이 다른 변경이 있었을 수 있다.
3. 확인이 끝나면 "다음에 할 일" 1번부터 진행한다. "실패한 시도"에 적힌 방법은 다시 쓰지 않는다.
