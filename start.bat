@echo off
REM Windows용 빠른 시작 스크립트

echo 🧺 세탁기 예약 시스템 시작 중...

REM 패키지 확인 및 설치
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 패키지 설치 중...
    pip install -r requirements.txt
)

REM 데이터베이스 초기화
if not exist "washing_machine.db" (
    echo 💾 데이터베이스 초기화 중...
    python -c "from database import Database; db = Database('washing_machine.db'); db.init_machines(3); print('✅ 데이터베이스 초기화 완료!')"
)

REM 애플리케이션 실행
echo 🚀 서버 시작 중...
python app.py

