"""
세탁기 예약 시스템의 데이터 모델 정의

이 모듈은 세탁기와 예약 정보를 관리하는 클래스들을 포함합니다.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class MachineStatus(Enum):
    """세탁기 상태를 나타내는 열거형"""
    AVAILABLE = "사용 가능"      # 사용 가능한 상태
    IN_USE = "사용 중"           # 현재 세탁 중
    COMPLETED = "완료"           # 세탁 완료 (옷을 가져가기 대기 중)


class Machine:
    """
    개별 세탁기를 나타내는 클래스
    
    각 세탁기는 고유한 ID와 상태, 사용자 정보를 가집니다.
    """
    
    def __init__(self, machine_id: int):
        """
        세탁기 초기화
        
        Args:
            machine_id: 세탁기 고유 번호 (1, 2, 3, ...)
        """
        self.machine_id = machine_id
        self.status = MachineStatus.AVAILABLE
        self.user_name: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration_minutes: int = 0  # 세탁 소요 시간 (분)
    
    def start_washing(self, user_name: str, duration_minutes: int = 30):
        """
        세탁 시작
        
        Args:
            user_name: 사용자 이름
            duration_minutes: 세탁 소요 시간 (기본 30분)
        """
        self.status = MachineStatus.IN_USE
        self.user_name = user_name
        self.start_time = datetime.now()
        self.duration_minutes = duration_minutes
        self.end_time = self.start_time + timedelta(minutes=duration_minutes)
    
    def complete_washing(self):
        """세탁 완료 처리"""
        self.status = MachineStatus.COMPLETED
    
    def reset(self):
        """세탁기를 초기 상태로 리셋"""
        self.status = MachineStatus.AVAILABLE
        self.user_name = None
        self.start_time = None
        self.end_time = None
        self.duration_minutes = 0
    
    def get_remaining_minutes(self) -> int:
        """
        남은 세탁 시간 계산 (분 단위)
        
        Returns:
            남은 시간(분). 세탁 중이 아니면 0 반환
        """
        if self.status != MachineStatus.IN_USE or self.end_time is None:
            return 0
        
        remaining = self.end_time - datetime.now()
        if remaining.total_seconds() <= 0:
            return 0
        return int(remaining.total_seconds() / 60)
    
    def to_dict(self) -> dict:
        """
        세탁기 정보를 딕셔너리로 변환 (API 응답용)
        
        Returns:
            세탁기 정보가 담긴 딕셔너리
        """
        return {
            "machine_id": self.machine_id,
            "status": self.status.value,
            "user_name": self.user_name,
            "remaining_minutes": self.get_remaining_minutes(),
            "end_time": self.end_time.isoformat() if self.end_time else None
        }


class Reservation:
    """
    세탁기 예약 정보를 나타내는 클래스
    
    모든 세탁기가 사용 중일 때 대기 예약을 관리합니다.
    """
    
    def __init__(self, user_name: str, reservation_time: datetime = None):
        """
        예약 초기화
        
        Args:
            user_name: 예약자 이름
            reservation_time: 예약 시간 (기본값: 현재 시간)
        """
        self.user_name = user_name
        self.reservation_time = reservation_time or datetime.now()
        self.expiry_time = self.reservation_time + timedelta(minutes=5)  # 5분 후 자동 취소
    
    def is_expired(self) -> bool:
        """
        예약이 만료되었는지 확인
        
        Returns:
            만료 여부 (True: 만료됨, False: 유효함)
        """
        return datetime.now() > self.expiry_time
    
    def to_dict(self) -> dict:
        """
        예약 정보를 딕셔너리로 변환 (API 응답용)
        
        Returns:
            예약 정보가 담긴 딕셔너리
        """
        return {
            "user_name": self.user_name,
            "reservation_time": self.reservation_time.isoformat(),
            "expiry_time": self.expiry_time.isoformat(),
            "is_expired": self.is_expired()
        }

