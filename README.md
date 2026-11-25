# agent-toolkit

Matt의 AI 에이전트 스킬·훅·MCP 설정 모음. 한 저장소가 Claude Code 플러그인 마켓플레이스이면서, Codex CLI·Gemini CLI·ChatGPT에서도 같은 스킬 폴더(Agent Skills 형식의 `SKILL.md`)를 쓴다.

## 목록

| 이름 | 종류 | 하는 일 | Claude | Codex | Gemini CLI |
|---|---|---|---|---|---|
| [korean-legal-desk](plugins/korean-legal-desk) | 스킬 + 훅 | 한국법 계약서 검토·레드라인, 법률문서 작성, 법령·판례 확인. 프롬프트 민감번호 차단 훅 | ○ (훅은 Claude Code만) | ○ | ○ |
| [session-handoff](plugins/session-handoff) | 스킬 (+ 선택 훅) | 새 세션 인수인계 파일 생성·자동 전달 | ○ | ○ | ○ (훅 제외) |
| [model-switch-prep](plugins/model-switch-prep) | 스킬 | 새 모델 전환 전 확인 → 압축 → 변경 → 검증 | ○ | ○ | △ (Claude Code·Codex 명령 기준) |
| [design-md](plugins/design-md) | 스킬 | DESIGN.md 디자인 시스템 74종으로 UI 만들기 | ○ | ○ | ○ |
| [korean-law](mcp/korean-law) | MCP 설정 | 법제처 Open API 법령·판례 조회 서버 연결 방법 | ○ | ○ | ○ |

## 설치

### Claude Code (CLI, 데스크톱 Code 탭)
```
/plugin marketplace add Matt54090/agent-toolkit
/plugin install korean-legal-desk@agent-toolkit
/plugin install session-handoff@agent-toolkit
/plugin install model-switch-prep@agent-toolkit
/plugin install design-md@agent-toolkit
```
필요한 것만 설치하면 된다. 업데이트: `/plugin marketplace update agent-toolkit`.

### Claude 웹·데스크톱·모바일 채팅
스킬별로 계정 스킬에 저장한다(설정의 스킬 메뉴에서 스킬 폴더를 zip으로 업로드). MCP는 `mcp/<이름>/README.md`의 커넥터 안내를 따른다.

### Codex CLI · Gemini CLI
```powershell
git clone https://github.com/Matt54090/agent-toolkit.git
cd agent-toolkit
powershell -ExecutionPolicy Bypass -File scripts\sync-skills.ps1      # Windows
bash scripts/sync-skills.sh                                            # macOS/Linux
```
모든 스킬을 `~/.agents/skills`로 복사한다. Codex는 이 폴더를 읽고, Gemini CLI도 `~/.gemini/skills`와 함께 이 폴더를 읽는다. 이미 같은 이름 폴더가 있으면 건너뛴다(`-Force`/`--force`로 백업 후 덮어쓰기, `-Only`/`--only`로 일부만).

### ChatGPT 웹·Gemini 웹앱, 그 밖의 세부
[HANDOFF.md](HANDOFF.md)에 서비스별 설치·MCP 설정·확인 방법을 정리했다. 다른 AI에게 "HANDOFF.md 읽고 설치해줘"라고 시켜도 된다.

## 저장소 규칙
- 새 스킬은 `plugins/<이름>/.claude-plugin/plugin.json` + `plugins/<이름>/skills/<이름>/SKILL.md` 구조로 추가하고 `.claude-plugin/marketplace.json`에 한 줄 등록한다.
- MCP는 `mcp/<이름>/README.md`에 연결 방법만 둔다. API 키·토큰 값은 어떤 파일에도 쓰지 않고 환경변수 이름만 쓴다.
- 고친 플러그인은 plugin.json과 marketplace.json의 version을 함께 올린다.

라이선스: MIT(LICENSE). 외부 자료 출처와 라이선스는 NOTICE.md.
