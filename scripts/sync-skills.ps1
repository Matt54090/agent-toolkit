# agent-toolkit의 모든 스킬을 Codex·Gemini CLI 공용 스킬 폴더로 복사한다.
# 사용: 저장소 폴더에서  powershell -ExecutionPolicy Bypass -File scripts\sync-skills.ps1 [-Target <경로>] [-Force] [-Only 이름1,이름2]
# 기본 대상: $env:USERPROFILE\.agents\skills  (Codex는 이 폴더를, Gemini CLI는 ~/.gemini/skills와 함께 이 폴더도 읽는다)
# 같은 이름 폴더가 이미 있으면 건너뛴다. 덮어쓰려면 -Force (기존 폴더는 .backup-<시각>으로 옮겨 둔다).
param(
  [string]$Target = (Join-Path $env:USERPROFILE ".agents\skills"),
  [switch]$Force,
  [string[]]$Only
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$skills = Get-ChildItem -Path (Join-Path $repo "plugins\*\skills\*") -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }
if ($Only) { $skills = $skills | Where-Object { $Only -contains $_.Name } }
New-Item -ItemType Directory -Force $Target | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
foreach ($s in $skills) {
  $dest = Join-Path $Target $s.Name
  if (Test-Path $dest) {
    if (-not $Force) { Write-Host "건너뜀(이미 있음): $($s.Name)  -> 덮어쓰려면 -Force"; continue }
    $backup = Join-Path $Target ".backup-$stamp"
    New-Item -ItemType Directory -Force $backup | Out-Null
    Move-Item $dest (Join-Path $backup $s.Name)
    Write-Host "기존 폴더 백업: $backup\$($s.Name)"
  }
  Copy-Item -Recurse $s.FullName $dest
  Write-Host "복사: $($s.Name) -> $dest"
}
Write-Host "완료. Codex·Gemini CLI를 다시 시작하면 새 스킬이 잡힙니다."
