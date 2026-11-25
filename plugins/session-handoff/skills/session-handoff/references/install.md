# 훅 설치 (Windows 기준, 1회)

새 세션이 시작될 때 `handoff_hook.py`가 자동으로 실행되도록 등록한다. Claude Code와 Codex가 같은 스크립트 하나를 함께 쓴다.

## 0. Python 확인
PowerShell에서 실행:
```powershell
python --version
```
`Python 3.x`가 나오면 된다. 명령을 찾을 수 없다는 오류가 나오면 `py --version`을 실행해 본다. 이게 되면 아래 명령의 `python`을 모두 `py`로 바꿔서 쓴다.

## 1. 스크립트를 고정 위치에 복사
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.handoff-hook"
Copy-Item "<받은 폴더>\session-handoff\scripts\handoff_hook.py" "$env:USERPROFILE\.handoff-hook\handoff_hook.py"
```
아래 설정에서는 스크립트 경로를 `C:/Users/<사용자명>/.handoff-hook/handoff_hook.py`처럼 슬래시(/)로 쓴다. 이렇게 쓰면 cmd, PowerShell, Git Bash 어디서 실행돼도 같은 경로로 인식된다.

## 2. Claude Code — `~/.claude/settings.json`
파일이 이미 있으면 다른 설정은 그대로 두고 `"hooks"` 항목만 추가한다. `"hooks"`가 이미 있으면 그 안에 `"SessionStart"`만 추가한다.
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear",
        "hooks": [
          { "type": "command", "command": "python C:/Users/<사용자명>/.handoff-hook/handoff_hook.py", "timeout": 10 }
        ]
      }
    ]
  }
}
```

## 3. Codex — `~/.codex/hooks.json`
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear",
        "hooks": [
          { "type": "command", "command": "python C:/Users/<사용자명>/.handoff-hook/handoff_hook.py", "timeout": 10 }
        ]
      }
    ]
  }
}
```
Codex를 다시 시작하면 새 훅을 검토하라는 경고가 뜬다. `/hooks`를 입력해 이 훅을 신뢰(trust)로 지정한다. 그래도 훅이 실행되지 않으면 버전이 오래된 것일 수 있다. `~/.codex/config.toml`에 아래를 추가하거나 Codex를 업데이트한다.
```toml
[features]
codex_hooks = true
```

## 4. 동작 확인
1. 아무 폴더에 `.handoff\HANDOFF.md`를 만든다. 첫 줄들을 `---` / `status: pending` / `created: <지금 시각>` / `---`로 쓴다.
2. 그 폴더에서 `claude` 또는 `codex`를 실행하고 "인수인계 받은 내용 있어?"라고 물어본다.
3. 내용을 알고 있고, 파일의 status가 `consumed`로 바뀌었으면 성공이다.
