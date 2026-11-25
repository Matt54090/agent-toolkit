# korean-legal-desk

한국법 기준 법률 작업용 스킬·훅 묶음. 서명 전 계약서 검토와 레드라인(상대방 관점 재검토 포함), 계약서·내용증명·지급명령·합의서 등 법률문서 초안, 법령 조문·판례 확인을 같은 규칙으로 처리한다. 결론마다 `[검증] / [추론] / [미확인]` 라벨을 붙이고, 확인하지 않은 조문·수치는 쓰지 않으며, 초안만 만들고 발송하지 않는다.

> 법률 자문이 아니다. 서명·발송·제출 전에는 변호사·노무사 등 전문가 확인을 받는다.

## 구성

| 구성 요소 | 무엇 | 동작하는 곳 |
|---|---|---|
| 스킬 `korean-legal-desk` | 검토·레드라인 / 작성 / 조사 / 분쟁 대응 4모드 | 웹·데스크톱·모바일 채팅, Claude Code, Codex CLI |
| `references/` | 유형별 검토 프로토콜, 문서 템플릿, 내 표준 조항 양식, 연계 도구 | CLI 설치본(웹 업로드 zip에도 포함) |
| `scripts/pii_mask.py` | 계약서 민감번호를 로컬에서 가리고 되돌림 | 로컬 실행 가능한 곳(CLI, 데스크톱 Code 탭) |
| 훅 `UserPromptSubmit` | 프롬프트에 주민·외국인등록번호, 카드번호가 있으면 전송 차단 | Claude Code(CLI·데스크톱 Code 탭)만 |
| (연계) korean-law MCP | 법제처 Open API 조문·판례 조회 | 웹 커넥터 / Claude Code 플러그인 |

## 설치
모음 저장소(agent-toolkit) 기준이다. 서비스별 상세는 저장소 루트 HANDOFF.md.

- Claude 웹·데스크톱 채팅: 계정 스킬로 저장(스킬 카드 또는 zip 업로드). 법령 조회는 `mcp/korean-law/README.md`대로 커넥터 추가. 훅은 채팅에서 동작하지 않고, 같은 규칙이 스킬 본문에 있다.
- Claude Code:
  ```
  /plugin marketplace add Matt54090/agent-toolkit
  /plugin install korean-legal-desk@agent-toolkit
  ```
  훅 모드: `LEGAL_PII_GUARD=warn`(경고만) 또는 `off`. Windows에서 `python3`가 없으면 `hooks/hooks.json`의 명령을 `python`으로 바꾼다.
- Codex·Gemini CLI: 저장소 루트에서 `scripts/sync-skills.ps1 -Only korean-legal-desk`(또는 `.sh --only korean-legal-desk`).

## 사용 예

- "이 용역계약서 서명해도 돼? 나는 수급인이야" + 파일 첨부 → 7단 브리프(결론·돈·할 수 있는 것/없는 것·보호/노출·레드라인 표·상대방이 깔아둔 것·전문가 확인 관문)
- "깊게 봐줘" → 4관점 패널 검토 추가
- "우리가 보낼 계약서야, 뭘 내주고 있는지 봐줘" → outbound 점검
- "레드라인 반영한 워드 파일도 만들어줘" → 변경 추적 .docx(또는 대비표)
- "돈 빌려준 지 1년 됐는데 안 갚아" → 선택지 비교 → 내용증명 초안
- "근로기준법 해고예고 조문이랑 예외 알려줘" → 조문 인용 + 링크 + 라벨

### 내 표준 조항
`skills/korean-legal-desk/references/playbook-template.md`를 복사해 프로젝트 루트 `.legal/playbook.md`로 두면 검토 기준이 된다. 웹에서는 프로젝트 지식에 올린다.

### 민감번호 가리기(CLI)
```
python3 skills/korean-legal-desk/scripts/pii_mask.py mask 계약서.docx --names "홍길동,가나다 주식회사"
# → 계약서.masked.txt 만 Claude에게 읽힘
python3 skills/korean-legal-desk/scripts/pii_mask.py restore 계약서_수정.masked.txt 계약서.pii-map.json
```
`*.pii-map.json`에는 원래 값이 있으니 공유·커밋하지 않는다(.gitignore에 포함).

## 출처
저장소 루트 NOTICE.md. X 게시물(@BBBang9900)에 소개된 4개 링크를 검토해 반영했다.
