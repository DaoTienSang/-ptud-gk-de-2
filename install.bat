@echo off
echo Dang cai dat cac thu vien can thiet voi phien ban cu the...
echo -------------------------------------

:: Kiem tra neu pip da duoc cai dat
python -m pip --version
if %ERRORLEVEL% neq 0 (
    echo Loi: Pip khong duoc tim thay. Vui long cai dat Python va them no vao PATH.
    pause
    exit /b 1
)

:: Cai dat Flask 2.3.3
echo Cai dat Flask==2.3.3...
python -m pip install flask==2.3.3

:: Cai dat Flask-SQLAlchemy 3.1.1
echo Cai dat Flask-SQLAlchemy==3.1.1...
python -m pip install flask-sqlalchemy==3.1.1

:: Cai dat Werkzeug 2.3.7
echo Cai dat Werkzeug==2.3.7...
python -m pip install werkzeug==2.3.7

echo -------------------------------------
echo Cai dat hoan tat!
python app.py
pause