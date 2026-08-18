$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Test-Path -LiteralPath ".\.env")) {
  Write-Host "No existe .env. Copia .env.example a .env y completa la configuracion."
  exit 1
}

Get-Content .\.env | ForEach-Object {
  $line = $_.Trim()
  if ($line -and -not $line.StartsWith("#")) {
    $name, $value = $line.Split("=", 2)
    [Environment]::SetEnvironmentVariable($name, $value, "Process")
  }
}

if ($env:SMTP_PASS -eq "PEGA_TU_APP_PASSWORD_DE_16_CARACTERES_ACA") {
  Write-Host "Falta configurar SMTP_PASS en .env con la app password de Google."
  exit 1
}

$env:SMTP_PASS = $env:SMTP_PASS -replace "\s", ""

$bundledPython = "C:\Users\Noxi-PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path -LiteralPath $bundledPython) {
  & $bundledPython .\mail_service.py
} else {
  python .\mail_service.py
}
