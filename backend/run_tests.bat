@echo off
REM Batch script to start the backend server and run signup tests

echo Starting backend server and running signup tests...

REM Start the backend server in a separate window
echo Starting backend server on port 8000...
start "Backend Server" cmd /c "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 10 /nobreak >nul

REM Run the signup tests
echo Running signup tests...
python test_signup.py

echo Tests completed.
echo Press any key to close this window...
pause >nul