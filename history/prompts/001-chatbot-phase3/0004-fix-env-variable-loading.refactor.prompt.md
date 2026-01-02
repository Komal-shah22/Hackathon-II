---
id: 0004
title: Fix environment variable loading for OpenAI API key
stage: refactor
date: 2026-01-02
surface: agent
model: gemini
feature: 001-chatbot-phase3
branch: 001-chatbot-phase3
user: system
command: "Investigate and fix OPENAI_API_KEY loading issue."
labels: [bugfix, environment, backend]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/requirements.txt
 - backend/main.py
tests:
 - none
---

## Prompt

Please check and report on the following:

### 1. Check if .env file exists
```bash
# Check if .env file exists in backend directory
ls backend/.env

# If exists, show first few characters of OPENAI_API_KEY (for privacy)
# Expected: OPENAI_API_KEY=sk-proj-...
```

### 2. Check if python-dotenv is installed
```bash
# Check dependencies
grep -i "python-dotenv\|dotenv" backend/pyproject.toml

# Check if installed in environment
python -c "import dotenv; print('dotenv installed:', dotenv.__version__)"
```

### 3. Check main.py for load_dotenv()
```python
# Check if main.py loads environment variables
# Look for these lines at the top of backend/main.py:

from dotenv import load_dotenv
load_dotenv()
```

## Response snapshot

The `OPENAI_API_KEY` was not being loaded because the `python-dotenv` package was not installed and the `load_dotenv()` function was not being called. I added the package to `requirements.txt`, installed it, and added the necessary code to `main.py` to load the .env file. The server now starts correctly and loads the API key.

## Outcome

- ✅ Impact: The backend server can now correctly load the OPENAI_API_KEY from the .env file, enabling features that rely on the OpenAI API.
- 🧪 Tests: No new tests were added. Verification was done by observing the server startup logs.
- 📁 Files: Modified `backend/requirements.txt` to add `python-dotenv`. Modified `backend/main.py` to call `load_dotenv()`.
- 🔁 Next prompts: none
- 🧠 Reflection: The initial use of `uv sync` caused unexpected behavior (uninstalling packages). Switched to `pip install` for more reliable dependency installation.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempt to install dependencies with `uv sync` was unsuccessful.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
