@echo off
echo Deactivating virtual environment and cleaning up Python cache...

:: Deactivate virtual environment if active
if defined VIRTUAL_ENV (
    call deactivate
    echo Virtual environment deactivated
)

:: Wait a moment to ensure deactivation is complete
timeout /t 2 /nobreak > nul

:: Delete all __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

:: Delete .pyc files
del /s /q *.pyc

:: Delete venv directory if it exists
if exist venv\ (
    rmdir /s /q venv
    echo Deleted venv directory
)

:: Delete .pytest_cache if it exists
if exist .pytest_cache\ (
    rmdir /s /q .pytest_cache
    echo Deleted .pytest_cache directory
)

echo Cleanup completed!
pause