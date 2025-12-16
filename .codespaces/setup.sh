#!/bin/bash
# Codespaces 자동 설정 스크립트

echo "🚀 세탁기 예약 시스템 설정 중..."

# 패키지 설치
echo "📦 패키지 설치 중..."
pip install -r requirements.txt

# 데이터베이스 초기화
echo "💾 데이터베이스 초기화 중..."
python -c "from database import Database; db = Database('washing_machine.db'); db.init_machines(3); print('✅ 데이터베이스 초기화 완료!')"

echo ""
echo "✅ 설정 완료!"
echo ""
echo "다음 명령어로 실행하세요:"
echo "  python app.py"
echo ""
echo "포트 5000이 자동으로 포워딩됩니다."

