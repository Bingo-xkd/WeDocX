@echo off
setlocal enabledelayedexpansion

echo [INFO] WeDocX End-to-End Test Script for Windows
echo [INFO] This script should be run from the project root directory.
echo [INFO] For example, execute: backend\run_e2e_test.bat

REM 1. 切换到脚本所在目录(backend)
cd /D "%~dp0"

REM 2. 激活conda环境
echo.
echo [1/6] Activating conda environment 'WeDocX'...
call conda activate WeDocX
if !errorlevel! neq 0 (
    echo [ERROR] Failed to activate conda environment.
    echo [ERROR] Please make sure conda is installed and the 'WeDocX' environment exists.
    goto cleanup
)

REM 3. 检查 Redis
echo.
echo [2/6] Checking for Redis...
echo [INFO] Please ensure Redis server is running on its default port.

REM 4. 启动 Celery worker 和 FastAPI (后台)
echo.
echo [3/6] Starting Celery worker in the background...
start "CeleryWorker" /b python -m celery -A app.celery_app worker -P gevent --loglevel=info > ../output/celery_worker.log 2>&1
echo [INFO] Celery worker started. Log: backend\celery_worker.log
timeout /t 5 >nul

echo.
echo [4/6] Starting FastAPI server in the background...
start "FastAPIServer" /b uvicorn main:app --host 127.0.0.1 --port 8000 --reload > ../output/uvicorn.log 2>&1
echo [INFO] FastAPI server started. Log: backend\uvicorn.log
timeout /t 5 >nul

REM 5. 运行 pytest
echo.
echo [5/6] Running E2E tests...
pytest tests/test_e2e_process_url.py
set PYTEST_EXIT_CODE=!ERRORLEVEL!

REM 6. 清理后台进程
:cleanup
echo.
echo [6/6] Cleaning up background processes...
echo [INFO] Attempting to stop FastAPI server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr "127.0.0.1:8000"') do (
    set "PID=%%a"
    if "!PID!" NEQ "0" (
        echo [INFO] Found FastAPI server with PID: !PID!. Terminating...
        taskkill /F /PID !PID! >nul
    )
)

echo [INFO] Attempting to stop Celery workers...
taskkill /F /FI "WINDOWTITLE eq CeleryWorker" /IM python.exe >nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] Celery worker process terminated.
) else (
    echo [WARN] Could not find or terminate Celery worker process by window title. It may need to be stopped manually.
)

echo [INFO] Cleanup complete.

endlocal
exit /b %PYTEST_EXIT_CODE% 