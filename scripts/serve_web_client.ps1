$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$WebDir = Join-Path $ProjectRoot "clients\web"

Write-Host "Serving web client from: $WebDir"
Write-Host "Open http://localhost:8080 in your browser"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

Set-Location -LiteralPath $WebDir
python -m http.server 8080
