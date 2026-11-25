---
name: design-md
description: 실제 웹사이트에서 추출한 DESIGN.md 디자인 시스템 74종(Stripe, Linear, Vercel, Notion, Claude, Apple, Tesla, Spotify 등 AI·개발도구·핀테크·자동차·미디어) 중 하나를 골라 UI·페이지·컴포넌트·랜딩·대시보드를 그 스타일로 만들 때 사용. "X 스타일로", "X처럼 보이게", "DESIGN.md 적용", "디자인 시스템 골라줘", "/design-md" 같은 요청이나, 분위기만 말하고 어울리는 디자인 시스템 추천을 원할 때 트리거. Use when building UI in the style of a known site's design language from the awesome-design-md collection.
---

# design-md — DESIGN.md 디자인 시스템 적용

이 스킬 폴더에는 다음이 있다.
- `catalog.md` — 74개 디자인 시스템 목록 (slug, 이름, 분류, 한 줄 설명, 형식)
- `designs/<slug>/DESIGN.md` — 각 디자인 시스템 원문 (출처: VoltAgent/awesome-design-md, MIT)

생성 시각과 원본 커밋: 2026-10-12, VoltAgent/awesome-design-md@13be5c0

## 절차

1. **catalog.md를 먼저 읽는다.** DESIGN.md 원문(파일당 125~850줄)은 고른 것만 연다.
2. **디자인 시스템 고르기**
   - 사용자가 브랜드를 지정했으면 catalog의 slug를 찾는다 (예: "리니어" → `linear.app`, "엑스에이아이" → `x.ai`).
   - 분위기만 말했으면 catalog의 설명을 근거로 2~3개를 추천하고 각각 한 줄 이유를 붙인다. 사용자가 고르게 하되, 사용자가 없거나 "알아서"라고 했으면 가장 맞는 하나로 진행하고 그 선택을 밝힌다.
   - catalog에 없는 브랜드면 없다고 말하고 가장 가까운 것을 제안한다.
3. **고른 `designs/<slug>/DESIGN.md`를 끝까지 읽는다.** 일부만 읽고 색·타이포를 추측하지 않는다.
4. **형식에 맞게 해석한다.**
   - `yaml` 형식(64개): frontmatter의 `colors / typography / rounded / spacing / components`가 정답 토큰이다. 본문의 `{colors.primary}` 같은 참조는 frontmatter 값으로 풀어서 쓴다. 본문 "Do's and Don'ts", "Iteration Guide", "Known Gaps"를 지킨다.
   - `9-section` 형식(10개): frontmatter가 없다. "2. Color Palette & Roles", "3. Typography Rules", "4. Component Stylings"의 표·목록에서 값을 뽑고, "9. Agent Prompt Guide"를 우선 참고한다.
5. **결과물에 적용한다.**
   - 토큰은 CSS 변수(`:root { --color-primary: ... }`)나 Tailwind theme로 한 번 정의하고 컴포넌트는 그 변수만 쓴다. 헥스 값을 컴포넌트마다 직접 쓰지 않는다.
   - 유료·전용 폰트(Copernicus, StyreneB, SF Pro 등)는 DESIGN.md가 적어 둔 대체 폰트(보통 Google Fonts에 있는 것)를 쓴다.
   - 프로젝트 폴더에서 작업 중이고 사용자가 원하면 원문을 프로젝트 루트에 `DESIGN.md`로 복사한다. 같은 이름 파일이 이미 있으면 덮어쓰지 말고 먼저 묻는다.

## 지켜야 할 선

- DESIGN.md는 **시각 언어(색·타이포·간격·컴포넌트 규칙)를 빌려 오는 용도**다. 해당 회사의 이름, 로고, 워드마크, 마스코트, 실제 문구를 그대로 넣은 페이지는 만들지 않는다. 결과물의 브랜드명·문구는 사용자 것 또는 새로 지은 것을 쓴다.
- 실제 회사의 로그인·결제 화면처럼 보여 진짜로 오인될 수 있는 페이지(피싱형 복제)는 만들지 않는다.
- 사용자가 "그 사이트를 똑같이 복제"를 원하면, 스타일을 적용한 독자 디자인으로 대신하겠다고 한 줄로 말하고 진행한다.

## 참고

- 원본 갱신: WSL에서 `cd ~/awesome-design-md && git pull && ~/design-md-setup/install.sh` (세 환경 사본을 다시 만든다)
- 원본 README가 말하는 `preview.html`은 이 저장소 클론에 없다. 미리보기가 필요하면 토큰으로 간단한 견본 페이지(색 견본·타입 스케일·버튼·카드)를 직접 만든다.
