# QWCoder Test Script (PowerShell)
# Tests the QWCoder environment setup

param(
    [switch]$Verbose
)

# Colors for output
$RED = "Red"
$GREEN = "Green"
$YELLOW = "Yellow"
$BLUE = "Cyan"
$WHITE = "White"

# Logging functions
function Write-Info {
    param([string]$Message)
    Write-Host "[$BLUE[INFO]$WHITE] $Message" -ForegroundColor $BLUE
}

function Write-Success {
    param([string]$Message)
    Write-Host "[$GREEN[SUCCESS]$WHITE] $Message" -ForegroundColor $GREEN
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[$YELLOW[WARNING]$WHITE] $Message" -ForegroundColor $YELLOW
}

function Write-Error {
    param([string]$Message)
    Write-Host "[$RED[ERROR]$WHITE] $Message" -ForegroundColor $RED
}

# Test functions
function Test-FileExists {
    param([string]$FilePath)

    if (Test-Path $FilePath -PathType Leaf) {
        Write-Success "✓ $FilePath exists"
        return $true
    } else {
        Write-Error "✗ $FilePath missing"
        return $false
    }
}

function Test-DirectoryExists {
    param([string]$DirPath)

    if (Test-Path $DirPath -PathType Container) {
        Write-Success "✓ $DirPath directory exists"
        return $true
    } else {
        Write-Error "✗ $DirPath directory missing"
        return $false
    }
}

function Test-JsonSyntax {
    param([string]$FilePath)

    try {
        $json = Get-Content $FilePath -Raw | ConvertFrom-Json
        Write-Success "✓ $FilePath has valid JSON syntax"
        return $true
    } catch {
        Write-Error "✗ $FilePath has invalid JSON syntax"
        return $false
    }
}

# Main test function
function Main {
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor $WHITE
    Write-Host "║                     QWCoder Test Suite                       ║" -ForegroundColor $WHITE
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor $WHITE
    Write-Host ""

    $errors = 0
    $warnings = 0

    Write-Info "Starting QWCoder environment tests..."
    Write-Host ""

    # Test directory structure
    Write-Info "Testing directory structure..."

    $dirs = @("config", "scripts", "tools", "bin", "docs", "templates")
    foreach ($dir in $dirs) {
        if (-not (Test-DirectoryExists $dir)) {
            $errors++
        }
    }

    Write-Host ""

    # Test configuration files
    Write-Info "Testing configuration files..."

    $configFiles = @(
        "config\qwcoder.json",
        "config\environment.env",
        "config\aliases.sh",
        "config\bashrc"
    )

    foreach ($file in $configFiles) {
        if (-not (Test-FileExists $file)) {
            $errors++
        }
    }

    # Test JSON files
    if (-not (Test-JsonSyntax "config\qwcoder.json")) {
        $errors++
    }

    Write-Host ""

    # Test script files
    Write-Info "Testing script files..."

    $scriptFiles = @(
        "scripts\setup.sh",
        "scripts\update.sh",
        "scripts\help.sh",
        "scripts\functions.sh",
        "scripts\test.sh",
        "scripts\test.ps1"
    )

    foreach ($file in $scriptFiles) {
        if (-not (Test-FileExists $file)) {
            $errors++
        }
    }

    Write-Host ""

    # Test tool files
    Write-Info "Testing tool files..."

    $toolFiles = @(
        "tools\package-manager.sh",
        "tools\project-templates.sh"
    )

    foreach ($file in $toolFiles) {
        if (-not (Test-FileExists $file)) {
            $errors++
        }
    }

    Write-Host ""

    # Test documentation files
    Write-Info "Testing documentation files..."

    $docFiles = @(
        "README.md",
        "docs\INSTALL.md",
        "docs\USAGE.md"
    )

    foreach ($file in $docFiles) {
        if (-not (Test-FileExists $file)) {
            $errors++
        }
    }

    Write-Host ""

    # Summary
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor $WHITE
    Write-Host "║                        Test Summary                          ║" -ForegroundColor $WHITE
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor $WHITE
    Write-Host ""

    if ($errors -eq 0) {
        Write-Success "All tests passed! ✅"
        if ($warnings -gt 0) {
            Write-Warning "$warnings warnings found (non-critical)"
        }
        Write-Host ""
        Write-Host "🎉 QWCoder environment is ready!" -ForegroundColor $GREEN
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor $WHITE
        Write-Host "1. Run: .\scripts\setup.sh (requires bash/WSL)" -ForegroundColor $WHITE
        Write-Host "2. Or manually configure your shell" -ForegroundColor $WHITE
        Write-Host "3. Run: qwcoder help" -ForegroundColor $WHITE
        Write-Host ""
        return 0
    } else {
        Write-Error "$errors errors found"
        if ($warnings -gt 0) {
            Write-Warning "$warnings warnings found"
        }
        Write-Host ""
        Write-Error "Please fix the errors before proceeding."
        Write-Host ""
        Write-Host "Common fixes:" -ForegroundColor $WHITE
        Write-Host "- Check file permissions" -ForegroundColor $WHITE
        Write-Host "- Verify all files were created correctly" -ForegroundColor $WHITE
        Write-Host "- Ensure you're in the correct directory" -ForegroundColor $WHITE
        Write-Host ""
        return 1
    }
}

# Run main function
Main
