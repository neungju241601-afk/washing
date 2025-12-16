"""
세탁기 예약 시스템 Flask 웹 애플리케이션

이 파일은 웹 인터페이스를 제공하는 메인 애플리케이션입니다.
"""

from flask import Flask, render_template, request, jsonify
from washing_system import WashingMachineSystem
import threading
import time

# Flask 애플리케이션 초기화
app = Flask(__name__)

# 세탁기 시스템 인스턴스 생성 (3대의 세탁기)
# 세탁기 개수는 여기서 변경 가능합니다
washing_system = WashingMachineSystem(num_machines=3)


def background_status_checker():
    """
    백그라운드에서 주기적으로 세탁기 상태를 확인하는 함수
    
    세탁 완료 여부를 체크하고 알림을 생성합니다.
    """
    while True:
        try:
            washing_system.check_and_update_status()
            time.sleep(10)  # 10초마다 상태 확인
        except Exception as e:
            print(f"상태 확인 중 오류 발생: {e}")
            time.sleep(10)


# 백그라운드 스레드 시작
background_thread = threading.Thread(target=background_status_checker, daemon=True)
background_thread.start()


@app.route('/')
def index():
    """
    메인 페이지 렌더링
    
    Returns:
        HTML 템플릿 렌더링 결과
    """
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """
    전체 시스템 상태 조회 API
    
    Returns:
        JSON 형식의 시스템 상태 정보
    """
    status = washing_system.get_status()
    return jsonify(status)


@app.route('/api/start', methods=['POST'])
def start_washing():
    """
    세탁 시작 API
    
    요청 데이터:
        - user_name: 사용자 이름
        - duration_minutes: 세탁 소요 시간 (선택, 기본 30분)
    
    Returns:
        JSON 형식의 결과 정보
    """
    data = request.get_json()
    user_name = data.get('user_name', '').strip()
    duration_minutes = data.get('duration_minutes', 30)
    
    if not user_name:
        return jsonify({
            "success": False,
            "message": "사용자 이름을 입력해주세요."
        }), 400
    
    if duration_minutes <= 0 or duration_minutes > 120:
        return jsonify({
            "success": False,
            "message": "세탁 시간은 1분 이상 120분 이하여야 합니다."
        }), 400
    
    result = washing_system.start_washing(user_name, duration_minutes)
    return jsonify(result)


@app.route('/api/complete', methods=['POST'])
def complete_washing():
    """
    세탁 완료 및 옷 가져가기 API
    
    요청 데이터:
        - machine_id: 세탁기 번호
        - user_name: 사용자 이름
    
    Returns:
        JSON 형식의 결과 정보
    """
    data = request.get_json()
    machine_id = data.get('machine_id')
    user_name = data.get('user_name', '').strip()
    
    if not machine_id:
        return jsonify({
            "success": False,
            "message": "세탁기 번호를 입력해주세요."
        }), 400
    
    if not user_name:
        return jsonify({
            "success": False,
            "message": "사용자 이름을 입력해주세요."
        }), 400
    
    result = washing_system.complete_washing(machine_id, user_name)
    return jsonify(result)


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """
    사용자 알림 조회 API
    
    쿼리 파라미터:
        - user_name: 사용자 이름
    
    Returns:
        JSON 형식의 알림 목록
    """
    user_name = request.args.get('user_name', '').strip()
    
    if not user_name:
        return jsonify({
            "success": False,
            "message": "사용자 이름을 입력해주세요."
        }), 400
    
    notifications = washing_system.get_notifications(user_name)
    return jsonify({
        "success": True,
        "notifications": notifications
    })


@app.route('/api/notifications/clear', methods=['POST'])
def clear_notifications():
    """
    사용자 알림 삭제 API
    
    요청 데이터:
        - user_name: 사용자 이름
    
    Returns:
        JSON 형식의 결과 정보
    """
    data = request.get_json()
    user_name = data.get('user_name', '').strip()
    
    if not user_name:
        return jsonify({
            "success": False,
            "message": "사용자 이름을 입력해주세요."
        }), 400
    
    washing_system.clear_notifications(user_name)
    return jsonify({
        "success": True,
        "message": "알림이 삭제되었습니다."
    })


@app.route('/api/reservation/cancel', methods=['POST'])
def cancel_reservation():
    """
    예약 취소 API
    
    요청 데이터:
        - user_name: 예약자 이름
    
    Returns:
        JSON 형식의 결과 정보
    """
    data = request.get_json()
    user_name = data.get('user_name', '').strip()
    
    if not user_name:
        return jsonify({
            "success": False,
            "message": "사용자 이름을 입력해주세요."
        }), 400
    
    result = washing_system.cancel_reservation(user_name)
    return jsonify(result)


if __name__ == '__main__':
    import os
    
    # 환경 변수에서 포트 가져오기 (호스팅 플랫폼용)
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("세탁기 예약 시스템이 시작되었습니다!")
    print("=" * 50)
    print(f"웹 브라우저에서 http://localhost:{port} 을 열어주세요.")
    print("=" * 50)
    print("데이터베이스: washing_machine.db (영구 저장)")
    print("=" * 50)
    
    # 프로덕션 환경에서는 debug=False로 설정
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

