param(
  [string]$Output = "multi-agent-test-factory.zip"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ZipPath = Join-Path $ProjectRoot $Output

if (Test-Path $ZipPath) {
  Remove-Item -LiteralPath $ZipPath -Force
}

Compress-Archive -Path (Join-Path $ProjectRoot "*") -DestinationPath $ZipPath -Force
Write-Host "Packaged: $ZipPath"
