<#
PowerShell helper to set up local dev environment on Windows.
Usage: open PowerShell in repo root (Run As Administrator if needed) and execute:
  .\scripts\setup-dev.ps1
Options:
  -StartServer  : Start the uvicorn dev server at the end (default: $true)
  -ForceRestartDB: If a Docker container named 'saveabite-db' exists, remove and recreate it (default: $false)
#>
param(
    [switch]$StartServer = $true,
    [switch]$ForceRestartDB = $false
)

# Allow skipping server start with environment variable SKIP_SERVER=1 or SKIP_SERVER=true
if ($env:SKIP_SERVER -and ($env:SKIP_SERVER -eq '1' -or $env:SKIP_SERVER.ToLower() -eq 'true')){ $StartServer = $false }

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

Write-Info "Creating virtual environment..."
if (-Not (Test-Path -Path ".\.venv")){
    python -m venv .venv
} else {
    Write-Info ".venv already exists"
}

$pip = Join-Path -Path ".." -ChildPath '.venv\Scripts\pip.exe'
if (-Not (Test-Path -Path '.venv\Scripts\pip.exe')){
    $pip = '.venv\Scripts\pip.exe'
}
Write-Info "Installing Python dependencies..."
& .\.venv\Scripts\pip.exe install -r backend/requirements.txt

# Ensure .env exists
if (-Not (Test-Path -Path ".env")){
    if (Test-Path -Path ".env.example"){
        Copy-Item .env.example .env
        Write-Info "Copied .env.example -> .env"
    } else {
        Write-Err "No .env.example found. Please create a .env with DB settings."; exit 1
    }
}

# Start MySQL via Docker if Docker is available
$dockerAvailable = (Get-Command docker -ErrorAction SilentlyContinue) -ne $null
if ($dockerAvailable){
    Write-Info "Docker detected. Ensuring MySQL container is running..."
    $existing = docker ps -a --filter 'name=saveabite-db' -q
    if ($existing -and -not $ForceRestartDB){
        Write-Info "Container 'saveabite-db' already exists. Starting container if needed..."
        docker start saveabite-db | Out-Null
    } else {
        if ($existing -and $ForceRestartDB){
            Write-Info "Removing existing 'saveabite-db'..."
            docker rm -f saveabite-db | Out-Null
        }
        Write-Info "Creating new MySQL container 'saveabite-db' (password: password, DB: saveabite)..."
        docker run -d --name saveabite-db -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=saveabite -p 3306:3306 mysql:8.0 | Out-Null
    }
    Write-Info "Waiting for MySQL to accept connections (this may take ~20s)..."
    $tries = 0
    while ($tries -lt 30){
        try{
            python .\scripts\check_db.py
            if ($LASTEXITCODE -eq 0){
                Write-Info "MySQL appears ready"
                break
            } else {
                Start-Sleep -Seconds 2
                $tries++
            }
        } catch {
            Start-Sleep -Seconds 2
            $tries++
        }
    }
    if ($tries -ge 30){ Write-Err "Timed out waiting for MySQL"; exit 1 }
} else {
    Write-Info "Docker not found - skipping Docker DB setup. Ensure MySQL is running and .env is configured."
}

Write-Info "Creating database tables..."
python backend/create_db.py
if ($LASTEXITCODE -ne 0){ Write-Err "create_db.py failed. Check DB settings in .env"; exit 1 }

Write-Info "Seeding sample data..."
python backend/seed.py

if ($StartServer){
    Write-Info "Starting dev server (uvicorn) on http://localhost:8000 ..."
    uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
} else {
    Write-Info "Setup finished. Run 'uvicorn app.main:app --reload --port 8000 --host 0.0.0.0' to start the server"
}
