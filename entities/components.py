# entities/components.py
from typing import Optional
from configs.constants import PHEROMONE_AUTH_THRESHOLD

class BaseComponent:
    def update(self, tick: int) -> None:
        pass

class HealthComponent(BaseComponent):
    """벌의 체력 및 생존 상태를 관리하는 캡슐화된 컴포넌트입니다."""
    def __init__(self, initial_health: float = 100.0):
        self._health: float = initial_health
        self._is_alive: bool = True
        
    def apply_damage(self, amount: float) -> None:
        self._health -= amount
        if self._health <= 0:
            self._is_alive = False

class ForagingComponent(BaseComponent):
    """채집 역할(Forager)을 수행할 때만 주입되는 컴포넌트입니다."""
    def __init__(self):
        self.pollen_basket: float = 0.0
        self.honey_sac: float = 0.0
        

class LayingWorkerComponent(BaseComponent):
    """
    중앙 정책 서버(여왕) 부재 시, 일반 노드(Worker)가 권한을 임의 탈취하여 
    무정란(Drone)을 생성하는 권한 드리프트(Entropy) 컴포넌트입니다.
    """
    def __init__(self):
        self.drone_egg_count: int = 0
        self.is_active: bool = True
        
    def produce_dummy_node(self) -> str:
        """
        보안 매핑: 승인되지 않은 더미 노드(수컷벌)만 생성하여 시스템 자원을 고갈시킵니다.
        생물학적 매핑: 무정란 산란 -> 100% 수컷만 탄생
        """
        if self.is_active:
            self.drone_egg_count += 1
            return "UNAUTHORIZED_DRONE_NODE"
        return "NONE"

    def update(self, tick: int, current_pheromone: float) -> None:
        # 페로몬(정책 신호)이 다시 임계치 이상으로 회복되면 권한 드리프트 중단
        if current_pheromone >= PHEROMONE_AUTH_THRESHOLD:
            self.is_active = False