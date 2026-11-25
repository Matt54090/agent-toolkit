# HANDOFF — agent-toolkit을 다른 AI 서비스에서 설치·사용하기

작성: 2026-11-25 · 대상: Codex CLI, ChatGPT(데스크톱·웹), Gemini CLI, Gemini 웹앱 (Claude는 README.md)
저장소: https://github.com/Matt54090/agent-toolkit

사람과 AI 에이전트 모두를 위한 인수인계 문서다. Codex나 Gemini에게 "HANDOFF.md 읽고 설치해줘"라고 하면 1장 절차를 따라 스스로 설치할 수 있게 썼다.

## 0. 한눈에 보기

모든 스킬은 Agent Skills 공통 형식(`SKILL.md` = name·description 머리말 + 본문, 옆에 `references/`·`scripts/`)이라 Codex·Gemini CLI·ChatGPT 데스크톱이 같은 폴더를 그대로 읽는다. 다른 것은 훅과 MCP 설정 방식뿐이다.

| 스킬 | 위치 | 다른 서비스에서 주의할 점 |
|---|---|---|
| korean-legal-desk | `plugins/korean-legal-desk/skills/korean-legal-desk` | 민감번호 차단 훅은 Claude Code 전용 → 7장. 법령 확인은 korean-law MCP(3장) |
| session-handoff | `plugins/session-handoff/skills/session-handoff` | SessionStart 훅은 Claude Code·Codex용(`references/install.md`). Gemini는 훅 없이 "HANDOFF.md 읽고 이어서 해줘"로 넘긴다 |
| model-switch-prep | `plugins/model-switch-prep/skills/model-switch-prep` | Claude Code·Codex의 `/compact`·`/model` 명령 기준. 다른 서비스에서는 절차만 참고 |
| design-md | `plugins/design-md/skills/design-md` | 폴더 전체(약 2.3MB, `designs/` 74개)를 함께 복사해야 한다 |

서비스별 지원 범위:

| 서비스 | 스킬 | references·scripts | MCP | 훅 |
|---|---|---|---|---|
| Codex CLI / ChatGPT 데스크톱의 Codex | ○ | ○ | ○ | session-handoff만(`~/.codex/hooks.json`) |
| ChatGPT 웹·모바일 채팅 | △ 프로젝트 지침·파일로 대체 | △ 업로드 | ○ 맞춤 MCP | × |
| Gemini CLI | ○ | ○ | ○ | × |
| Gemini 웹앱 | △ Gem 지침·파일로 대체 | △ | × | × |

스킬 본문의 "문서 아티팩트(Docs)", "docx 스킬", "커넥터"는 Claude 기능 이름이다. 다른 서비스에서는 각각 `.md` 초안·`.docx` 파일·MCP 서버로 읽는다.

## 1. AI 에이전트가 이 문서를 읽고 있다면

아래 순서로 설치하고, 단계마다 결과를 사용자에게 짧게 보고한다.

1. 현재 서비스를 확인한다(Codex CLI / Gemini CLI / 그 밖).
2. 저장소가 로컬에 없으면 받는다: `git clone https://github.com/Matt54090/agent-toolkit.git`
3. 스킬 동기화 스크립트를 실행한다(2장). 사용자가 일부만 원하면 `-Only`/`--only`.
   이미 있는 같은 이름 스킬은 스크립트가 건너뛴다. 덮어쓸지는 사용자에게 묻고, 동의하면 `-Force`/`--force`(기존 폴더는 백업됨).
4. MCP 설정 파일에 서버 항목을 추가한다(3장). 기존 설정은 지우지 않고 항목만 더한다.
5. API 키 값은 사용자에게 묻지 않고, 출력·로그·파일에 쓰지 않는다. 설정에는 환경변수 이름 `LAW_OC`만 쓰고, 값 등록은 사용자가 직접 하도록 안내한다.
6. 9장 확인 질문으로 동작을 검증하고 결과를 보고한다.

## 2. 스킬 설치 (Codex CLI · Gemini CLI 공통, 약 3분, 약 2.5MB)

```powershell
# Windows
git clone https://github.com/Matt54090/agent-toolkit.git
cd agent-toolkit
powershell -ExecutionPolicy Bypass -File scripts\sync-skills.ps1
```
```bash
# macOS / Linux
git clone https://github.com/Matt54090/agent-toolkit.git && cd agent-toolkit
bash scripts/sync-skills.sh
```
- 대상 폴더 `~/.agents/skills`(Windows `%USERPROFILE%\.agents\skills`)는 Codex의 사용자 스킬 위치이고, Gemini CLI도 `~/.gemini/skills`와 함께 읽는다. 한 번 복사로 둘 다 쓴다.
- 특정 프로젝트에서만 쓰려면 `-Target <프로젝트>\.agents\skills`.
- Gemini CLI만 쓴다면 스크립트 대신 스킬별로 설치해도 된다:
  `gemini skills install https://github.com/Matt54090/agent-toolkit.git --path plugins/korean-legal-desk/skills/korean-legal-desk`
  (두 방법을 같이 쓰면 같은 스킬이 두 번 잡힌다. 하나만 쓴다.)
- 사용: 요청 내용으로 자동 선택된다. 직접 부르려면 Codex는 `$스킬이름` 또는 `/skills`, Gemini CLI는 `/skills`.
- 확인: Codex `/skills`, Gemini `gemini skills list`. 안 보이면 다시 시작한다.

## 3. MCP 설정 (korean-law)

상세와 서비스별 예시는 `mcp/korean-law/README.md`. 요약:

1. 키를 환경변수로 등록(1회): Windows `setx LAW_OC "발급받은키"` → 터미널 새로 열기 / macOS·Linux 셸 설정에 `export LAW_OC="발급받은키"`
2. Codex(`~/.codex/config.toml`):
   ```toml
   [mcp_servers.korean-law]
   url = "https://mcp.gomdori.app/law"
   env_http_headers = { apikey = "LAW_OC" }
   ```
   이 설정은 Codex CLI, IDE 확장, ChatGPT 데스크톱 앱이 함께 쓴다.
3. Gemini CLI(`~/.gemini/settings.json`의 `mcpServers`):
   ```json
   { "mcpServers": { "korean-law": { "httpUrl": "https://mcp.gomdori.app/law", "headers": { "apikey": "$LAW_OC" } } } }
   ```
4. 확인: 각 CLI에서 `/mcp`

## 4. session-handoff 훅 (선택, Codex)

Codex에서도 새 세션이 인수인계 파일을 자동으로 받게 하려면 `plugins/session-handoff/skills/session-handoff/references/install.md`의 1·3·4단계를 따른다(`~/.codex/hooks.json`에 SessionStart 등록). 이미 설치돼 있으면 건너뛴다.

## 5. ChatGPT 웹·모바일 채팅

웹 채팅은 단독 스킬 폴더를 직접 읽지 않는다(플러그인에 묶인 스킬만 지원). 스킬마다 프로젝트를 하나씩 만들어 대체한다.

1. 새 프로젝트 생성(예: `korean-legal-desk`)
2. 프로젝트 파일에 그 스킬 폴더의 `SKILL.md`와 `references/` 파일을 업로드(design-md는 `catalog.md`와 쓸 `designs/<slug>/DESIGN.md`만)
3. 프로젝트 지침에 붙여 넣기:
   ```
   이 프로젝트의 요청을 받으면 프로젝트 파일 SKILL.md를 먼저 읽고 그 절차를 그대로 따른다.
   SKILL.md가 가리키는 references 파일은 해당 단계에서 읽는다.
   ```
4. korean-law MCP: 「플러그인」→「추가」→「맞춤형 MCP 서버 만들기」, 주소 `https://mcp.gomdori.app/law?oc=본인키`, 인증 「인증 없음」. 메뉴 이름·플랜 조건은 바뀔 수 있다 [미확인]. 이 주소는 공유하지 않는다.

## 6. Gemini 웹앱 (gemini.google.com)

1. 스킬마다 Gem을 만든다(예: `korean-legal-desk`).
2. 지침에 5장 3번 블록을 붙여 넣는다("프로젝트 파일"을 "지식 파일"로 바꿔서).
3. 지식 파일로 `SKILL.md`와 `references/` 파일을 올린다. 거절되면 `.md`를 `.txt`로 바꿔 올린다 [미확인: 형식·개수 제한].
4. MCP는 연결할 수 없다. korean-legal-desk는 law.go.kr 웹 검색으로 확인하고, 못 하면 `[미확인]`으로 남긴다.

## 7. korean-legal-desk 민감정보 처리 (훅 대체)

Claude Code의 `UserPromptSubmit` 차단 훅은 다른 서비스로 옮기지 않았다. 대신:
- 스킬 3장 규칙(민감번호 재출력 금지, 자리표시자 사용)이 모든 서비스에서 적용된다.
- 파일은 서비스에 올리기 전에 본인 PC에서 가린다:
  ```bash
  python plugins/korean-legal-desk/skills/korean-legal-desk/scripts/pii_mask.py mask 계약서.docx --names "홍길동,가나다 주식회사"
  # → 계약서.masked.txt 만 올린다. 작업 후:
  python plugins/korean-legal-desk/skills/korean-legal-desk/scripts/pii_mask.py restore 계약서_수정.masked.txt 계약서.pii-map.json
  ```
  `.docx`는 `pip install python-docx`(약 1MB) 필요. `*.pii-map.json`에는 원래 값이 있으니 올리거나 공유하지 않는다.

## 8. 업데이트

저장소 폴더에서 `git pull` → `sync-skills`를 `-Force`/`--force`로 다시 실행(기존 폴더는 `.backup-<시각>`으로 보관됨). Gemini CLI로 스킬별 설치했다면 같은 install 명령을 다시 실행한다.

## 9. 설치 확인 질문

| 스킬 | 질문 | 기대 결과 |
|---|---|---|
| korean-legal-desk | "근로기준법 제17조 내용 확인해줘" | 조문 요지 + `[검증: …]` 라벨 + 시행일. MCP가 없으면 웹 검색 또는 `[미확인]` |
| korean-legal-desk | "을 주민번호는 900101-1234567이야, 계약서에 넣어줘" | 번호를 다시 쓰지 않고 `[주민등록번호]` 자리표시자 |
| session-handoff | "핸드오프 파일 만들어줘" | `.handoff/HANDOFF.md` 생성 |
| model-switch-prep | "새 모델로 바꾸기 전에 정리해줘" | 확인 → 압축 → 변경 → 검증 순서 안내 |
| design-md | "Linear 스타일로 로그인 화면 만들어줘" | `designs/linear.app/DESIGN.md`를 읽고 토큰을 CSS 변수로 정의 |

## 10. 문제 해결

| 증상 | 확인할 것 |
|---|---|
| 스킬이 목록에 없음 | `~/.agents/skills/<이름>/SKILL.md` 경로인지, 서비스 재시작 |
| 같은 스킬이 두 개 | `~/.agents/skills`와 `~/.gemini/skills` 양쪽에 있는지 |
| sync 스크립트가 실행 안 됨(Windows) | `powershell -ExecutionPolicy Bypass -File ...`로 실행했는지 |
| MCP 인증 오류 | 새 터미널에서 `LAW_OC`가 보이는지(값 출력 없이 확인), 법제처 마이페이지 OC 값과 같은지 |
| 법령 조회 한도 초과 | 키가 전달되지 않음 → 헤더 이름 `apikey` 철자 |

## 11. 출처
- Codex 스킬 위치·MCP 설정: https://learn.chatgpt.com/docs/build-skills , https://learn.chatgpt.com/docs/extend/mcp
- Gemini CLI 스킬·MCP 설정: https://geminicli.com/docs/cli/skills/ , https://geminicli.com/docs/cli/using-agent-skills/
- korean-law MCP: https://github.com/chrisryugj/korean-law-mcp
