@echo off
REM Navigate to the project directory
cd /d D:\bhupal\projects\work_cms

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Start the Django development server
python manage.py runserver 127.0.0.1:8080
