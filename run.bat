@echo off
echo Starting Anchor State Manager...
call .venv\Scripts\activate
python -m uvicorn anchor.server:app --reload
pause