# utils/logger.py
import json
import os
from typing import Dict, Any

class AuditLogger:
    """
    보안 감사(Audit) 및 주요 이벤트를 기록하는 로거입니다.
    메모리 폭증을 막기 위해 Delta Logging 방식을 취합니다.
    """
    def __init__(self, log_filepath: str = "logs/audit_log.json"):
        self.log_filepath = log_filepath
        self.event_history = []
        self._initialize_log_directory()

    def _initialize_log_directory(self) -> None:
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)

    def log_event(self, tick: int, event_type: str, details: Dict[str, Any]) -> None:
        """
        상태 전이, 위협 감지, 관리자 개입 등의 주요 이벤트를 기록합니다.
        추후 이 데이터들은 해싱되어 무결성 검증에 사용될 수 있습니다.
        """
        record = {
            "tick": tick,
            "type": event_type,
            "details": details
        }
        self.event_history.append(record)

    def flush_to_disk(self) -> None:
        """쌓인 로그를 디스크에 안전하게 저장합니다."""
        with open(self.log_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.event_history, f, indent=4, ensure_ascii=False)