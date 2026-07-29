# Build mastrade_morning_report.exe on Windows.
#   powershell -ExecutionPolicy Bypass -File build.ps1
#
# Produces dist\mastrade_morning_report.exe — a single file you can copy to a
# machine with no Python installed.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "==> creating .venv" -ForegroundColor Cyan
    py -3.13 -m venv .venv
}

Write-Host "==> installing dependencies" -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "==> building" -ForegroundColor Cyan
.\.venv\Scripts\pyinstaller.exe mastrade_morning_report.spec --clean --noconfirm

Write-Host "==> smoke test" -ForegroundColor Cyan
.\dist\mastrade_morning_report.exe --help | Out-Null
if ($LASTEXITCODE -ne 0) { throw "smoke test failed" }

$exe = Get-Item .\dist\mastrade_morning_report.exe
Write-Host ("==> OK: {0} ({1:N1} MB)" -f $exe.FullName, ($exe.Length / 1MB)) -ForegroundColor Green
