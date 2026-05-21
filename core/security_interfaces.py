# core/security_interfaces.py
from abc import ABC, abstractmethod

class IDataIntegrity(ABC):
    """중요 수치에 대한 주기적 Hash Validation을 수행하기 위한 인터페이스입니다."""
    @abstractmethod
    def generate_checksum(self) -> str:
        """변수 조작(Memory Tampering) 방지를 위한 체크섬을 생성합니다."""
        pass

class IHeartbeat(ABC):
    """분산 리더 선출 방식에서 노드의 생존을 증명하는 하트비트 인터페이스입니다."""
    @abstractmethod
    def send_heartbeat(self, current_tick: int) -> bool:
        pass

class ISecurityPolicy(ABC):
    """Queen이 발행하는 정책(Pheromone)에 디지털 서명을 도입합니다."""
    @abstractmethod
    def sign_policy(self, payload: dict) -> dict:
        """정책 위조(Policy Spoofing) 방지를 위해 Action_Token을 포함합니다."""
        pass