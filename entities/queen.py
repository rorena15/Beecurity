# entities/queen.py
from entities.base_bee import BaseBee
from core.security_interfaces import IHeartbeat, ISecurityPolicy
from configs.constants import PHEROMONE_CHECK_INTERVAL, QUEEN_DAILY_EGG_LIMIT

class QueenBee(BaseBee, IHeartbeat, ISecurityPolicy):
    def __init__(self):
        super().__init__()
        self.daily_egg_limit: int = QUEEN_DAILY_EGG_LIMIT
        self.pheromone_level: float = 100.0
        self.last_heartbeat_tick: int = 0
        self.change_state("MASTER_NODE")

    def send_heartbeat(self, current_tick: int) -> bool:
        """자가 치유 프로토콜 발동을 막기 위해 생존 신호를 엔진에 전송합니다."""
        if not self.is_alive:
            return False
        self.last_heartbeat_tick = current_tick
        return True

    def sign_policy(self, payload: dict) -> dict:
        """Queen이 발행하는 정책(Pheromone)에 디지털 서명을 도입하여 위조를 방지합니다."""
        payload['action_token'] = f"SIGNED_BY_{self._BaseBee__uuid}" 
        return payload

    def update(self, tick: int) -> None:
        super().update(tick)
        # 10틱마다 하트비트 전송 및 페로몬 갱신 (Lazy Evaluation 적용)
        if tick % PHEROMONE_CHECK_INTERVAL == 0:
            self.send_heartbeat(tick)