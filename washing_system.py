"""
세탁기 예약 시스템의 핵심 로직

이 모듈은 세탁기 상태 관리, 예약 처리, 알림 기능을 담당합니다.
데이터베이스를 사용하여 영구 저장 및 다중 사용자 지원을 제공합니다.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from models import Machine, MachineStatus, Reservation
from database import Database


class WashingMachineSystem:
    """
    세탁기 예약 시스템의 메인 클래스
    
    여러 대의 세탁기를 관리하고, 예약 및 알림 기능을 제공합니다.
    SQLite 데이터베이스를 사용하여 데이터를 영구 저장합니다.
    """
    
    def __init__(self, num_machines: int = 3, db_path: str = "washing_machine.db"):
        """
        시스템 초기화
        
        Args:
            num_machines: 세탁기 개수 (기본값: 3대)
            db_path: 데이터베이스 파일 경로
        """
        self.db = Database(db_path)
        self.num_machines = num_machines
        self.db.init_machines(num_machines)  # 데이터베이스에 세탁기 초기화
    
    def _load_machine_from_db(self, machine_data: dict) -> Machine:
        """
        데이터베이스 데이터로 Machine 객체 생성
        
        Args:
            machine_data: 데이터베이스에서 가져온 세탁기 데이터
        
        Returns:
            Machine 객체
        """
        machine = Machine(machine_data['machine_id'])
        machine.status = MachineStatus(machine_data['status'])
        machine.user_name = machine_data['user_name']
        machine.duration_minutes = machine_data['duration_minutes'] or 0
        
        if machine_data['start_time']:
            machine.start_time = datetime.fromisoformat(machine_data['start_time'])
        if machine_data['end_time']:
            machine.end_time = datetime.fromisoformat(machine_data['end_time'])
        
        return machine
    
    def get_available_machine(self) -> Optional[int]:
        """
        사용 가능한 세탁기 찾기
        
        Returns:
            사용 가능한 세탁기 번호. 없으면 None
        """
        machines = self.db.get_machines()
        for machine_data in machines:
            if machine_data['status'] == '사용 가능':
                return machine_data['machine_id']
        return None
    
    def start_washing(self, user_name: str, duration_minutes: int = 30) -> dict:
        """
        세탁 시작
        
        사용 가능한 세탁기가 있으면 바로 시작하고,
        없으면 대기 예약을 생성합니다.
        
        Args:
            user_name: 사용자 이름
            duration_minutes: 세탁 소요 시간 (기본 30분)
        
        Returns:
            결과 정보가 담긴 딕셔너리
        """
        # 만료된 예약 제거
        self._clean_expired_reservations()
        
        # 사용 가능한 세탁기 찾기
        available_machine_id = self.get_available_machine()
        
        if available_machine_id:
            # 바로 세탁 시작
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            self.db.update_machine(
                available_machine_id,
                "사용 중",
                user_name,
                start_time,
                end_time,
                duration_minutes
            )
            
            return {
                "success": True,
                "message": f"세탁기 {available_machine_id}번이 시작되었습니다!",
                "machine_id": available_machine_id
            }
        else:
            # 대기 예약 생성
            reservation_time = datetime.now()
            expiry_time = reservation_time + timedelta(minutes=5)
            self.db.add_reservation(user_name, reservation_time, expiry_time)
            
            reservations = self.db.get_reservations()
            queue_position = len(reservations)
            
            return {
                "success": True,
                "message": f"모든 세탁기가 사용 중입니다. 대기 예약이 생성되었습니다. (대기 순서: {queue_position}번째)",
                "is_reservation": True,
                "queue_position": queue_position
            }
    
    def complete_washing(self, machine_id: int, user_name: str) -> dict:
        """
        세탁 완료 처리 및 옷 가져가기
        
        Args:
            machine_id: 세탁기 번호
            user_name: 사용자 이름 (본인 확인용)
        
        Returns:
            결과 정보가 담긴 딕셔너리
        """
        machines = self.db.get_machines()
        machine_data = next((m for m in machines if m['machine_id'] == machine_id), None)
        
        if not machine_data:
            return {
                "success": False,
                "message": "존재하지 않는 세탁기 번호입니다."
            }
        
        # 세탁 중이 아니면 오류
        if machine_data['status'] not in ['사용 중', '완료']:
            return {
                "success": False,
                "message": "이 세탁기는 현재 사용 중이 아닙니다."
            }
        
        # 사용자 확인
        if machine_data['user_name'] != user_name:
            return {
                "success": False,
                "message": "본인의 세탁물만 가져갈 수 있습니다."
            }
        
        # 대기 예약이 있으면 다음 사용자에게 세탁기 할당
        next_reservation = self.db.get_first_reservation()
        
        if next_reservation:
            # 다음 사용자에게 세탁기 할당
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=30)  # 기본 30분
            
            self.db.update_machine(
                machine_id,
                "사용 중",
                next_reservation['user_name'],
                start_time,
                end_time,
                30
            )
            
            # 예약 삭제
            self.db.delete_reservation(next_reservation['id'])
            
            # 다음 사용자에게 알림
            self._add_notification(
                next_reservation['user_name'],
                f"세탁기 {machine_id}번이 사용 가능합니다! 세탁이 자동으로 시작되었습니다."
            )
            
            return {
                "success": True,
                "message": "세탁물을 가져가셨습니다. 다음 대기자가 세탁을 시작했습니다.",
                "next_user": next_reservation['user_name']
            }
        else:
            # 세탁기 리셋
            self.db.reset_machine(machine_id)
            
            return {
                "success": True,
                "message": "세탁물을 가져가셨습니다."
            }
    
    def check_and_update_status(self):
        """
        세탁기 상태를 확인하고 업데이트
        
        시간이 지나서 완료된 세탁기를 찾아 상태를 업데이트하고,
        사용자에게 알림을 보냅니다.
        이 함수는 주기적으로 호출되어야 합니다.
        """
        current_time = datetime.now()
        machines = self.db.get_machines()
        
        for machine_data in machines:
            # 세탁 중이고 시간이 지났으면 완료 처리
            if machine_data['status'] == '사용 중' and machine_data['end_time']:
                end_time = datetime.fromisoformat(machine_data['end_time'])
                if current_time >= end_time:
                    # 완료 상태로 변경
                    self.db.update_machine(
                        machine_data['machine_id'],
                        "완료",
                        machine_data['user_name'],
                        datetime.fromisoformat(machine_data['start_time']) if machine_data['start_time'] else None,
                        end_time,
                        machine_data['duration_minutes']
                    )
                    # 사용자에게 알림
                    self._add_notification(
                        machine_data['user_name'],
                        f"세탁기 {machine_data['machine_id']}번 세탁이 완료되었습니다! 옷을 가져가주세요."
                    )
    
    def get_status(self) -> dict:
        """
        전체 시스템 상태 조회
        
        Returns:
            모든 세탁기 상태와 예약 목록이 담긴 딕셔너리
        """
        # 상태 업데이트
        self.check_and_update_status()
        
        # 만료된 예약 제거
        self._clean_expired_reservations()
        
        # 데이터베이스에서 세탁기 정보 가져오기
        machines_data = self.db.get_machines()
        machines = []
        
        for machine_data in machines_data:
            machine = self._load_machine_from_db(machine_data)
            machines.append(machine.to_dict())
        
        # 예약 정보 가져오기
        reservations_data = self.db.get_reservations()
        reservations = []
        for res_data in reservations_data:
            reservation_time = datetime.fromisoformat(res_data['reservation_time'])
            expiry_time = datetime.fromisoformat(res_data['expiry_time'])
            res = Reservation(res_data['user_name'], reservation_time)
            res.expiry_time = expiry_time
            reservations.append(res.to_dict())
        
        return {
            "machines": machines,
            "reservations": reservations,
            "total_machines": len(machines),
            "available_count": sum(1 for m in machines if m['status'] == '사용 가능'),
            "in_use_count": sum(1 for m in machines if m['status'] == '사용 중'),
            "completed_count": sum(1 for m in machines if m['status'] == '완료')
        }
    
    def get_notifications(self, user_name: str) -> List[dict]:
        """
        특정 사용자의 알림 조회
        
        Args:
            user_name: 사용자 이름
        
        Returns:
            해당 사용자의 알림 목록
        """
        notifications = self.db.get_notifications(user_name)
        return [
            {
                "user_name": notif['user_name'],
                "message": notif['message'],
                "timestamp": notif['timestamp']
            }
            for notif in notifications
        ]
    
    def clear_notifications(self, user_name: str):
        """
        특정 사용자의 알림 삭제
        
        Args:
            user_name: 사용자 이름
        """
        self.db.clear_notifications(user_name)
    
    def cancel_reservation(self, user_name: str) -> dict:
        """
        예약 취소
        
        Args:
            user_name: 예약자 이름
        
        Returns:
            결과 정보가 담긴 딕셔너리
        """
        reservations = self.db.get_reservations()
        user_reservations = [r for r in reservations if r['user_name'] == user_name]
        
        if user_reservations:
            self.db.delete_reservations_by_user(user_name)
            return {
                "success": True,
                "message": "예약이 취소되었습니다."
            }
        else:
            return {
                "success": False,
                "message": "취소할 예약이 없습니다."
            }
    
    def _clean_expired_reservations(self):
        """만료된 예약 자동 제거"""
        self.db.delete_expired_reservations()
    
    def _add_notification(self, user_name: str, message: str):
        """
        알림 추가
        
        Args:
            user_name: 사용자 이름
            message: 알림 메시지
        """
        self.db.add_notification(user_name, message, datetime.now())

