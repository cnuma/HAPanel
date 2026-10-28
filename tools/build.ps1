# HAPanel : lance ESPHome avec la version et le SHA Git injectes (invariant G5).
#
# Exemples, depuis la racine du depot, environnement .venv active :
#   .\tools\build.ps1 config
#   .\tools\build.ps1 compile -Config hapanel.yaml
#   .\tools\build.ps1 run -Device <PORT_COM ou IP_PANNEAU>
#   .\tools\build.ps1 logs -Device <PORT_COM ou IP_PANNEAU>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('config', 'compile', 'run', 'upload', 'logs')]
    [string]$Action,

    [string]$Config = 'hapanel_banc.yaml',

    [string]$Device
)

$ErrorActionPreference = 'Stop'
$racine = Split-Path -Parent $PSScriptRoot
Set-Location $racine

$version = (Get-Content -Path (Join-Path $racine 'VERSION') -TotalCount 1).Trim()
if (-not $version) { throw 'Fichier VERSION vide.' }

$sha = (git rev-parse --short HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'SHA Git introuvable.' }
# Un SHA suffixe +modif signale des fichiers non commites : il ne vaut pas validation.
if (git status --porcelain) { $sha = "$sha+modif" }

Write-Host "HAPanel $version ($sha) : esphome $Action $Config"

$arguments = @('-s', 'version', $version, '-s', 'git_sha', $sha, $Action, $Config)
if ($Device) {
    if ($Action -in @('config', 'compile')) { throw "-Device est inutile pour $Action." }
    $arguments += @('--device', $Device)
}

# ESPHome journalise sur stderr : sous PowerShell 5.1, 'Stop' en ferait une
# erreur fatale. Le code de sortie d'esphome fait foi.
$ErrorActionPreference = 'Continue'
& esphome @arguments
exit $LASTEXITCODE
