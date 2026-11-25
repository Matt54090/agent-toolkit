# korean-law MCP 연결 설정

법제처 Open API 기반 한국 법령·판례 조회 서버(chrisryugj/korean-law-mcp, MIT). `korean-legal-desk` 스킬이 조문·판례를 확인할 때 쓴다.

- 서버 주소: `https://mcp.gomdori.app/law`
- 키 전달: `apikey` 헤더(권장) 또는 주소 끝 `?oc=키`. 키 없이도 공용 한도로 동작한다.
- 키 발급: https://open.law.go.kr (무료) → 마이페이지 → API인증키관리에서 확인
- **이 폴더와 저장소 어디에도 키 값을 쓰지 않는다.** 설정 파일에는 환경변수 이름 `LAW_OC`만 쓴다.

## 키를 환경변수로 등록 (CLI 도구 공통, 1회)
- Windows: `setx LAW_OC "발급받은키"` → 터미널 새로 열기
- macOS/Linux: `~/.zshrc` 또는 `~/.bashrc`에 `export LAW_OC="발급받은키"`
- 값 출력 없이 확인: PowerShell `if ($env:LAW_OC) {"set"} else {"missing"}`

## Claude (웹·데스크톱·모바일 채팅)
설정 → Customize → Connectors → Add → Custom → Web → 이름 `korean-law`, 주소 `https://mcp.gomdori.app/law` → Authentication "No sign in" → Request headers에 `apikey` = 키 → Add.
(웹 화면은 환경변수를 못 쓰므로 키를 직접 넣는다. 화면에만 저장되고 저장소에는 남지 않는다.)

## Claude Code
```
/plugin marketplace add chrisryugj/korean-law-mcp
/plugin install korean-law@korean-law-marketplace
```
플러그인은 `LAW_OC` 환경변수를 `apikey` 헤더로 보낸다(원본 README 기준).

## Codex CLI / ChatGPT 데스크톱 — `~/.codex/config.toml`
```toml
[mcp_servers.korean-law]
url = "https://mcp.gomdori.app/law"
env_http_headers = { apikey = "LAW_OC" }
```
확인: Codex에서 `/mcp`

## Gemini CLI — `~/.gemini/settings.json` (기존 내용 유지, `mcpServers`에 추가)
```json
{
  "mcpServers": {
    "korean-law": {
      "httpUrl": "https://mcp.gomdori.app/law",
      "headers": { "apikey": "$LAW_OC" }
    }
  }
}
```
확인: Gemini CLI에서 `/mcp`

## ChatGPT 웹
「플러그인」→「추가」→「맞춤형 MCP 서버 만들기」, 주소 `https://mcp.gomdori.app/law?oc=본인키`, 인증 「인증 없음」(원본 README 기준, 메뉴 이름은 바뀔 수 있음). 이 주소는 공유하지 않는다.

## Gemini 웹앱
MCP 연결 기능이 없다. 스킬은 웹 검색(law.go.kr)으로 확인하고, 못 하면 `[미확인]`으로 남긴다.

## 동작 확인 질문
"근로기준법 제17조 확인해줘" → 조문 본문과 시행일이 나오면 성공.
