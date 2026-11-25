# GEMINI.md

이 저장소(agent-toolkit)는 AI 에이전트용 스킬·훅·MCP 설정 모음이다.

- 스킬은 `plugins/<이름>/skills/<이름>/SKILL.md`에 있다. 사용자의 요청이 어떤 스킬의 description과 맞으면 그 SKILL.md를 읽고 따른다.
- 스킬 설치를 요청받으면 `HANDOFF.md` 1장 절차를 따른다.
- API 키·토큰 값은 묻거나 출력하거나 파일에 쓰지 않는다. 환경변수 이름(예: `LAW_OC`)만 쓴다.
- 새 스킬을 추가할 때는 README.md "저장소 규칙"을 따른다(plugin.json, marketplace.json 등록, version 올리기).
- `*.pii-map.json`, `*.masked.txt`, `.env`, `*.zip`은 커밋하지 않는다(.gitignore).
