# entities/base_bee.py
import uuid
import hashlib
from typing import Dict
from core.security_interfaces import IDataIntegrity
from entities.components import BaseComponent

class BaseBee(IDataIntegrity):
    def __init__(self):
        # 외부 조작 방지를 위한 프라이빗 캡슐화
        self.__uuid: str = str(uuid.uuid4())
        self._state: str = "IDLE"
        self.age_days: int = 0
        self.experience: int = 0
        self.is_alive: bool = True
        self.components: Dict[str, BaseComponent] = {}

    def add_component(self, name: str, component: BaseComponent) -> None:
        self.components[name] = component

    def change_state(self, new_state: str) -> None:
        """상태 전이 시 명시적 호출을 통해 로깅 및 추적성을 확보합니다."""
        old_state = self._state
        self._state = new_state
        self._log_transition(old_state, new_state)

    def _log_transition(self, old: str, new: str) -> None:
        # 향후 Audit Logging 객체와 연동되어 보안 감사 로그로 활용됩니다.
        pass

    def promote_to_temporary_master(self) -> None:
        """중앙 제어기 장애 시 하위 노드 중 하나를 임시 제어기로 승격시킵니다."""
        self.change_state("TEMPORARY_MASTER")

    def generate_checksum(self) -> str:
        """선택적 무결성 검증을 위한 해시를 반환합니다."""
        data_to_hash = f"{self.__uuid}_{self._state}"
        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    def update(self, tick: int) -> None:
        """엔진의 틱 단위 신호에만 반응합니다. 개별 루프는 금지됩니다."""
        for comp in self.components.values():
            comp.update(tick)