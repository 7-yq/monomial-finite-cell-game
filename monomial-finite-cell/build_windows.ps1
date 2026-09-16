param(
    [string]$BasePython = "python"
)

$ErrorActionPreference = "Stop"

$GameRoot = $PSScriptRoot
$BuildEnvironment = Join-Path $env:TEMP "monomial-finite-cell-windows-build-env"
$BuildDirectory = Join-Path $env:TEMP "monomial-finite-cell-windows-build"
$PyInstallerConfig = Join-Path $env:TEMP "monomial-finite-cell-pyinstaller"
$DistributionDirectory = Join-Path $GameRoot "dist"
$Executable = Join-Path $DistributionDirectory "Monomial Finite Cell Game.exe"
$Archive = Join-Path $DistributionDirectory "Monomial-Finite-Cell-Game-Windows-x64-v0.1.0.zip"

if (-not (Test-Path (Join-Path $BuildEnvironment "Scripts\python.exe"))) {
    & $BasePython -m venv $BuildEnvironment
}

$BuildPython = Join-Path $BuildEnvironment "Scripts\python.exe"
& $BuildPython -m pip install --disable-pip-version-check -r (Join-Path $GameRoot "requirements-windows-build.txt")

New-Item -ItemType Directory -Force -Path $BuildDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $DistributionDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $PyInstallerConfig | Out-Null
$env:PYINSTALLER_CONFIG_DIR = $PyInstallerConfig

& $BuildPython -m PyInstaller `
    --noconfirm `
    --clean `
    --workpath $BuildDirectory `
    --distpath $DistributionDirectory `
    (Join-Path $GameRoot "MonomialFiniteCellGameWindows.spec")

& $Executable --smoke-test
if ($LASTEXITCODE -ne 0) {
    throw "The packaged Windows application failed its smoke test."
}

Compress-Archive -Force -Path $Executable -DestinationPath $Archive

Write-Host "Built $Executable"
Write-Host "Built $Archive"
Get-FileHash -Algorithm SHA256 $Archive
