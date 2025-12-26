Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
  python -m pip install --upgrade pip
  python -m pip install pyinstaller
  pyinstaller --clean --onefile --name report-backend app.py `
    --noconsole `
    --exclude-module PyQt6 --exclude-module PySide6
} finally {
  Pop-Location
}
