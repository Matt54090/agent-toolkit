# session-handoff

세션을 압축하지 않고 새 세션으로 넘기는 인수인계 파일(.handoff/HANDOFF.md) 생성·자동 전달 스킬. Claude Code·Codex 공용

스킬 본문은 `skills/session-handoff/SKILL.md`에 있다. 설치는 저장소 루트 README.md(Claude Code: `/plugin install session-handoff@agent-toolkit`)와 HANDOFF.md(Codex·Gemini·ChatGPT)를 본다. Codex와 Gemini CLI에서는 `scripts/sync-skills`로 스킬 폴더를 `~/.agents/skills`에 복사해 쓴다.

출처와 라이선스는 저장소 루트 NOTICE.md와 LICENSE를 본다. 고친 뒤에는 plugin.json과 marketplace.json의 version을 함께 올린다.
