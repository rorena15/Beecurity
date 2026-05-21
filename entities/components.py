# entities/components.py
from typing import Optional

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