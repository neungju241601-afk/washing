"""
데이터베이스 관리 모듈

SQLite를 사용하여 세탁기 상태, 예약, 알림 정보를 영구 저장합니다.
요금이 발생하지 않는 파일 기반 데이터베이스를 사용합니다.
"""

import sqlite3
import threading
from datetime import datetime
from typing import List, Optional, Dict
from contextlib import contextmanager


class Database:
    """
    SQLite 데이터베이스 관리 클래스
    
    스레드 안전성을 보장하기 위해 연결 풀을 사용합니다.
    """
    
    def __init__(self, db_path: str = "washing_machine.db"):
        """
        데이터베이스 초기화
        
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.local = threading.local()  # 스레드별 연결 저장
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        스레드별 데이터베이스 연결 가져오기
        
        Returns:
            SQLite 연결 객체
        """
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=10.0  # 동시 접근 시 대기 시간
            )
            self.local.connection.row_factory = sqlite3.Row  # 딕셔너리처럼 접근 가능
        return self.local.connection
    
    @contextmanager
    def get_cursor(self):
        """
        데이터베이스 커서 컨텍스트 매니저
        
        자동으로 커밋과 롤백을 처리합니다.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def _init_database(self):
        """데이터베이스 테이블 초기화"""
        with self.get_cursor() as cursor:
            # 세탁기 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS machines (
                    machine_id INTEGER PRIMARY KEY,
                    status TEXT NOT NULL,
                    user_name TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    duration_minutes INTEGER DEFAULT 0
                )
            """)
            
            # 예약 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    reservation_time TEXT NOT NULL,
                    expiry_time TEXT NOT NULL
                )
            """)
            
            # 알림 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    read INTEGER DEFAULT 0
                )
            """)
            
            # 시스템 설정 테이블 (세탁기 개수 등)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
    
    def init_machines(self, num_machines: int):
        """
        세탁기 초기화 (시스템 시작 시 호출)
        
        Args:
            num_machines: 세탁기 개수
        """
        with self.get_cursor() as cursor:
            # 기존 세탁기 확인
            cursor.execute("SELECT COUNT(*) as count FROM machines")
            existing_count = cursor.fetchone()['count']
            
            if existing_count == 0:
                # 세탁기 생성
                for i in range(1, num_machines + 1):
                    cursor.execute("""
                        INSERT INTO machines (machine_id, status, user_name, start_time, end_time, duration_minutes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (i, "사용 가능", None, None, None, 0))
            
            # 세탁기 개수 저장
            cursor.execute("""
                INSERT OR REPLACE INTO system_config (key, value)
                VALUES ('num_machines', ?)
            """, (str(num_machines),))
    
    def get_machines(self) -> List[Dict]:
        """
        모든 세탁기 정보 조회
        
        Returns:
            세탁기 정보 리스트
        """
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM machines ORDER BY machine_id")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def update_machine(self, machine_id: int, status: str, user_name: Optional[str] = None,
                      start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                      duration_minutes: int = 0):
        """
        세탁기 상태 업데이트
        
        Args:
            machine_id: 세탁기 번호
            status: 상태
            user_name: 사용자 이름
            start_time: 시작 시간
            end_time: 종료 시간
            duration_minutes: 소요 시간
        """
        with self.get_cursor() as cursor:
            cursor.execute("""
                UPDATE machines
                SET status = ?, user_name = ?, start_time = ?, end_time = ?, duration_minutes = ?
                WHERE machine_id = ?
            """, (
                status,
                user_name,
                start_time.isoformat() if start_time else None,
                end_time.isoformat() if end_time else None,
                duration_minutes,
                machine_id
            ))
    
    def reset_machine(self, machine_id: int):
        """세탁기 리셋"""
        self.update_machine(machine_id, "사용 가능", None, None, None, 0)
    
    def add_reservation(self, user_name: str, reservation_time: datetime, expiry_time: datetime) -> int:
        """
        예약 추가
        
        Returns:
            예약 ID
        """
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO reservations (user_name, reservation_time, expiry_time)
                VALUES (?, ?, ?)
            """, (
                user_name,
                reservation_time.isoformat(),
                expiry_time.isoformat()
            ))
            return cursor.lastrowid
    
    def get_reservations(self) -> List[Dict]:
        """모든 예약 조회"""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM reservations ORDER BY reservation_time")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def delete_reservation(self, reservation_id: int):
        """예약 삭제"""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    
    def delete_reservations_by_user(self, user_name: str):
        """사용자의 모든 예약 삭제"""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM reservations WHERE user_name = ?", (user_name,))
    
    def delete_expired_reservations(self):
        """만료된 예약 삭제"""
        with self.get_cursor() as cursor:
            current_time = datetime.now().isoformat()
            cursor.execute("DELETE FROM reservations WHERE expiry_time < ?", (current_time,))
    
    def get_first_reservation(self) -> Optional[Dict]:
        """가장 오래된 예약 조회"""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM reservations ORDER BY reservation_time LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_notification(self, user_name: str, message: str, timestamp: datetime):
        """알림 추가"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO notifications (user_name, message, timestamp, read)
                VALUES (?, ?, ?, 0)
            """, (user_name, message, timestamp.isoformat()))
    
    def get_notifications(self, user_name: str) -> List[Dict]:
        """사용자의 알림 조회"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM notifications
                WHERE user_name = ? AND read = 0
                ORDER BY timestamp DESC
            """, (user_name,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def clear_notifications(self, user_name: str):
        """사용자의 알림 삭제 (읽음 처리)"""
        with self.get_cursor() as cursor:
            cursor.execute("UPDATE notifications SET read = 1 WHERE user_name = ?", (user_name,))
    
    def close(self):
        """데이터베이스 연결 종료"""
        if hasattr(self.local, 'connection'):
            self.local.connection.close()
            delattr(self.local, 'connection')

