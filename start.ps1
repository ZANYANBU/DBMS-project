# School Management System - Startup Script
# Run this script to start the application

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " SCHOOL MANAGEMENT SYSTEM" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Green
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Python found: $(python --version)" -ForegroundColor Green
Write-Host ""

# Check if Flask is installed
Write-Host "Checking Flask installation..." -ForegroundColor Green
$flaskInstalled = python -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Flask not found. Installing required packages..." -ForegroundColor Yellow
    python -m pip install flask
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install Flask!" -ForegroundColor Red
        exit 1
    }
    Write-Host "Flask installed successfully!" -ForegroundColor Green
}

Write-Host "Flask is ready!" -ForegroundColor Green
Write-Host ""

# Initialize database if it doesn't exist
if (-not (Test-Path "school_management.db")) {
    Write-Host "Initializing database..." -ForegroundColor Green
    python init_db.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to initialize database!" -ForegroundColor Red
        exit 1
    }
    Write-Host "Database initialized successfully!" -ForegroundColor Green
    Write-Host ""
}

# Display login credentials
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " DEFAULT LOGIN CREDENTIALS" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Admin Login:" -ForegroundColor Magenta
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Staff Login (Examples):" -ForegroundColor Magenta
Write-Host "  Username: snape" -ForegroundColor White
Write-Host "  Password: staff123" -ForegroundColor White
Write-Host ""
Write-Host "Student Login (Examples):" -ForegroundColor Magenta
Write-Host "  Username: harry" -ForegroundColor White
Write-Host "  Password: student123" -ForegroundColor White
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Start the Flask application
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "Opening browser at http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

# Open browser after a short delay
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5000"

# Run Flask app
python app.py
